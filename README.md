# Municipal Issue Reporting Web App

This Flask web application allows users to report municipal issues, such as broken streetlights and other public infrastructure problems. Users can easily submit issues, providing essential details and location information.

Additional Features:
Google Maps Integration: Utilizes Google Maps API to display the location of reported issues on a map interface. This enhances visualization and helps municipal authorities pinpoint the exact locations of problems.

Twilio Integration for SMS Notifications: Integration with Twilio API allows the system to send SMS notifications to municipal authorities when a new issue is reported. This ensures timely awareness and response to reported problems.

Email Notifications: The application can send email notifications to municipal authorities when a new issue is reported or when there are updates on existing issues. This ensures multiple channels of communication for effective issue resolution.

User Authentication: Implement user authentication functionality to allow users to create accounts and log in. This adds security and allows for tracking of issue reports by individual users.

Admin Dashboard: Create an admin dashboard where municipal authorities can view all reported issues, mark them as resolved, and communicate with users if necessary. This dashboard provides centralized management of reported issues.

How to Run:
Ensure you have Python installed on your system.
Install the required dependencies listed in requirements.txt.
pip install -r requirements.txt
Set up API keys for Google Maps, Twilio, and SMTP as environment variables.
Run the main.py file to start the Flask application.
python main.py
Access the application through a web browser at the specified

https://github.com/Dlaminisiphi/Umndoni/assets/119821264/7a3c13a0-d9c1-472e-91c9-95a604fa4cb6

 address (usually http://localhost:5000).
Users can report issues by filling out the provided form, and municipal authorities can manage these issues through the admin dashboard.
