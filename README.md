mysql code to create the table 
if using for first time see a youtube video 


create schema ticketing;
CREATE TABLE bookings (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    booking_number VARCHAR(36) NOT NULL UNIQUE,
    visitor_name VARCHAR(255) NOT NULL,
    ticket_type VARCHAR(50) NOT NULL,
    show_time DATETIME NOT NULL,
    num_tickets INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


GROQ_API_KEY="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" //api for groq (chatbot)


DB_HOST=localhost


DB_USER=root


DB_PASSWORD="YOUR PASSWORD"


DB_NAME=ticketing


To be done:-


1.Payment gateway


2.Chatbot correction(The chatbot will be designed with accessibility in mind, offering features like voice commands and text-to-speech for visitors with disabilities.)


3.login/singup-(Account Details)


4.UI/UX to be improved


5.Search for the locations tab (State,city,monument name)


6.Pricing(Dynamic Ticket Pricing)


7.Photos


8.Monument credential details


9.Multilingual Support


10.Personalized Recommendations


11.Automated Confirmation and Reminders


12.Enhanced Security


13.Feedback and Surveys


14.Integration with Museum Systems(Later)


15.Group Bookings


16.Special Needs Assistance(Later)


17.Calendar Integration
