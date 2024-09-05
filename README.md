# Ticketing System

 Create a branch file by forking and then code on that rather than directly pushing code on the main branch and then push your updates when done.(Also use chatgpt if any confusion)

## Overview

This project is a ticket booking system designed to offer an enhanced user experience with various features such as a chatbot, payment gateway integration, dynamic ticket pricing, and more. The system supports voice commands and text-to-speech for visitors with disabilities, ensuring accessibility for all users.

## Getting Started

### Prerequisites

1. **MySQL** - Ensure you have MySQL installed on your system.
2. **Flask** - Python web framework.
3. **Groq API Key** - For chatbot integration.

### Database Setup

1. **Create Schema and Table**

    ```sql
    CREATE SCHEMA ticketing;
    USE ticketing;
    CREATE TABLE bookings (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        booking_number VARCHAR(36) NOT NULL UNIQUE,
        visitor_name VARCHAR(255) NOT NULL,
        ticket_type VARCHAR(50) NOT NULL,
        show_time DATETIME NOT NULL,
        num_tickets INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

### Environment Variables

Create a `.env` file with the following content:

    ```dotenv
    GROQ_API_KEY="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"
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD="YOUR PASSWORD"
    DB_NAME=ticketing
    ```

Replace `"YOUR PASSWORD"` with your MySQL root password.Save with ENV File Extension in the Online Booking Folder.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/anonymous2905/Online-booking-system.git
    ```

2. Navigate to the project directory:

    ```sh
    cd "online Booking"
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Flask application:

    ```sh
    python app.py
    ```

2. Access the application at `http://localhost:5000`.

## Features(To Do)

1. **Payment Gateway** - Integration with a payment gateway for secure transactions.
2. **Chatbot** - Accessible chatbot with voice commands and text-to-speech.
3. **Login/Signup** - User authentication and account management.
4. **UI/UX Improvements** - Enhanced user interface and user experience.
5. **Search for Locations** - State, city, and monument search functionality.
6. **Dynamic Ticket Pricing** - Pricing adjustments based on demand and other factors.
7. **Photos** - Visual representations of monuments.
8. **Monument Credential Details** - Comprehensive details about each monument.
9. **Multilingual Support** - Support for multiple languages.
10. **Personalized Recommendations** - Tailored suggestions based on user preferences.
11. **Automated Confirmation and Reminders** - Notifications for bookings and events.
12. **Enhanced Security** - Robust security measures.
13. **Feedback and Surveys** - Collect user feedback to improve the service.
14. **Integration with Museum Systems** - Planned for future updates.
15. **Group Bookings** - Book tickets for groups.
16. **Special Needs Assistance** - Planned for future updates.
17. **Calendar Integration** - Sync with calendars for event reminders.


