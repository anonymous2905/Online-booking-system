document.addEventListener('DOMContentLoaded', () => {
    // Handle booking ticket form submission
    document.getElementById('book-ticket-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        const data = {
            visitor_name: formData.get('visitor_name'),
            ticket_type: formData.get('ticket_type'),
            show_time: formData.get('show_time'),
            num_tickets: formData.get('num_tickets'),
            language: formData.get('language') || 'en' // Default to English if not specified
        };
        fetch('/book_ticket', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('booking-message').innerText = data.message || data.error;
            document.getElementById('booking-number').innerText = data.booking_number ? `Booking Number: ${data.booking_number}` : '';
        })
        .catch(error => {
            document.getElementById('booking-message').innerText = `Error: ${error.message}`;
            document.getElementById('booking-number').innerText = '';
        });
    });

    // Handle get booking form submission
    document.getElementById('get-booking-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const bookingNumber = document.getElementById('booking_number_input').value.trim();
        if (!bookingNumber) {
            document.getElementById('booking-details').innerText = 'Booking number is required.';
            return;
        }
        fetch(`/get_booking/${bookingNumber}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('booking-details').innerText = data.error;
            } else {
                document.getElementById('booking-details').innerText = 
                    `Booking Number: ${data.booking_number}\nName: ${data.visitor_name}\nTicket Type: ${data.ticket_type}\nShow Time: ${data.show_time}\nNumber of Tickets: ${data.num_tickets}`;
            }
        })
        .catch(error => {
            document.getElementById('booking-details').innerText = `Error: ${error.message}`;
        });
    });

    // Handle cancel booking form submission
    document.getElementById('cancel-booking-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const bookingNumber = document.getElementById('cancel_booking_number').value.trim();
        if (!bookingNumber) {
            document.getElementById('cancel-message').innerText = 'Booking number is required.';
            return;
        }
        fetch('/cancel_booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ booking_number: bookingNumber })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('cancel-message').innerText = data.message || data.error;
        })
        .catch(error => {
            document.getElementById('cancel-message').innerText = `Error: ${error.message}`;
        });
    });

    // Handle chatbot interactions
    document.getElementById('chat-submit').addEventListener('click', function() {
        const userMessage = document.getElementById('chat-input').value.trim();
        const language = document.getElementById('language').value || 'en';
        if (!userMessage) {
            document.getElementById('chat-output').innerText = 'Please enter a message.';
            return;
        }
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage, language: language })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('chat-output').innerText = data.response || 'No response from bot.';
            document.getElementById('chat-input').value = '';  // Clear input after sending
        })
        .catch(error => {
            document.getElementById('chat-output').innerText = `Error: ${error.message}`;
        });
    });
});
