from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Initialize the Groq client with your API key
api_key = "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"  # Replace with your actual API key
client = Groq(api_key=api_key)

def get_chatbot_response(user_message, conversation_history):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=conversation_history + [{"role": "user", "content": user_message}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        
        return response_text
    except Exception as e:
        # Log the error and return a user-friendly message
        print(f"Error in get_chatbot_response: {e}")
        return "Sorry, something went wrong. Please try again later."

# Chatbot state
conversation_history = []

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message', '')
    language = data.get('language', 'en')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})
    
    # Get chatbot response
    bot_response = get_chatbot_response(user_message, conversation_history)
    
    # Add chatbot response to conversation history
    conversation_history.append({"role": "assistant", "content": bot_response})
    
    # Respond with the chatbot's reply
    return jsonify({"response": bot_response})

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    data = request.json
    visitor_name = data.get('visitor_name')
    ticket_type = data.get('ticket_type')  # e.g., 'general', 'vip'
    show_time = data.get('show_time')  # e.g., '2024-08-15T20:00:00'

    if not visitor_name or not ticket_type or not show_time:
        return jsonify({"error": "All fields are required"}), 400

    # Here, add your logic to process the booking (e.g., storing in a database)
    # For demonstration purposes, we'll just return the provided details
    return jsonify({
        "message": "Booking confirmed!",
        "visitor_name": visitor_name,
        "ticket_type": ticket_type,
        "show_time": show_time
    })

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the chatbot API!"})

if __name__ == '__main__':
    app.run(debug=True)
