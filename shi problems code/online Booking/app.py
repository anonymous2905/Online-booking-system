from flask import Flask, request, jsonify, render_template
import os
import mysql.connector
import uuid
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL database connection configuration
db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def generate_booking_number():
    return str(uuid.uuid4())

def get_chatbot_response(user_message, context):
    client = Groq()
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": context}
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        return response.strip()
    except Exception as e:
        print(f"Error in get_chatbot_response: {e}")
        return "Sorry, something went wrong. Please try again later."

def validate_ticket_data(data):
    required_fields = ['visitor_name', 'ticket_type', 'show_time', 'num_tickets']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"
    return True, ""

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    data = request.json
    visitor_name = data.get('visitor_name', '')
    ticket_type = data.get('ticket_type', '')
    show_time = data.get('show_time', '')
    num_tickets = data.get('num_tickets', 1)
    
    is_valid, error_message = validate_ticket_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        booking_number = generate_booking_number()
        query = """
        INSERT INTO bookings (booking_number, visitor_name, ticket_type, show_time, num_tickets)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (booking_number, visitor_name, ticket_type, show_time, num_tickets))
        connection.commit()
        return jsonify({"message": "Ticket booked successfully!", "booking_number": booking_number})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/get_booking/<booking_number>', methods=['GET'])
def get_booking(booking_number):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM bookings WHERE booking_number = %s"
        cursor.execute(query, (booking_number,))
        booking = cursor.fetchone()
        if booking:
            return jsonify(booking)
        else:
            return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    data = request.json
    booking_number = data.get('booking_number', '')
    
    if not booking_number:
        return jsonify({"error": "Booking number is required"}), 400

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "DELETE FROM bookings WHERE booking_number = %s"
        cursor.execute(query, (booking_number,))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "Booking canceled successfully"})
        else:
            return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message', '')
    context = data.get('context', {})
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Check if the chatbot is in the middle of a booking process
    if context.get('booking_in_progress', False):
        step = context.get('step', 'start')

        if step == 'start' and "book" in user_message.lower() and "ticket" in user_message.lower():
            context['step'] = 'name'
            bot_response = "Please provide your name."
        elif step == 'name':
            context['visitor_name'] = user_message
            context['step'] = 'ticket_type'
            bot_response = "What type of ticket would you like? (Regular/VIP)"
        elif step == 'ticket_type':
            context['ticket_type'] = user_message
            context['step'] = 'show_time'
            bot_response = "When would you like to book the show for? (Please provide date and time)"
        elif step == 'show_time':
            context['show_time'] = user_message
            context['step'] = 'num_tickets'
            bot_response = "How many tickets would you like to book?"
        elif step == 'num_tickets':
            try:
                num_tickets = int(user_message)
                context['num_tickets'] = num_tickets
                # Book the ticket
                booking_details = {
                    "visitor_name": context.get('visitor_name', ''),
                    "ticket_type": context.get('ticket_type', ''),
                    "show_time": context.get('show_time', ''),
                    "num_tickets": context.get('num_tickets', 1)
                }

                booking_number = generate_booking_number()
                connection = get_db_connection()
                cursor = connection.cursor()
                query = """
                INSERT INTO bookings (booking_number, visitor_name, ticket_type, show_time, num_tickets)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (booking_number, booking_details['visitor_name'], booking_details['ticket_type'], booking_details['show_time'], booking_details['num_tickets']))
                connection.commit()

                bot_response = f"Your ticket has been booked successfully! Booking Number: {booking_number}"
                context.clear()  # Clear context after successful booking
                context['booking_in_progress'] = False
            except ValueError:
                bot_response = "Please provide a valid number for the tickets."
            except Exception as e:
                bot_response = f"Failed to book ticket: {str(e)}"
                context.clear()  # Clear context after failure
                context['booking_in_progress'] = False
        else:
            bot_response = "I'm sorry, I didn't understand that. Can you please clarify?"
            context['step'] = 'start'
        
    else:
        # Handle user input when not in booking process
        if "book" in user_message.lower() and "ticket" in user_message.lower():
            context['step'] = 'name'
            context['booking_in_progress'] = True
            bot_response = "Please provide your name."
        else:
            bot_response = get_chatbot_response(user_message, context)

    return jsonify({"response": bot_response, "context": context})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
