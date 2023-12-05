import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import twilio
from twilio.rest import Client
from dotenv import dotenv_values

# Load environment variables from the .env file using dotenv_values
secrets = dotenv_values(".env")

def send_email(receiver_email, subject, message):
    # Get  email and password from the secrets dictionary
    sender_email = secrets.get("SEND_EMAIL")
    password = secrets.get("PASSWORD")

    try:
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        body = MIMEText(message)
        msg.attach(body)

        # Use SSL context for secure connection
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            # Login and send email
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

#converts the user phone number to corrct formatt
def convert_number(phone_number):
    
    if phone_number.startswith('0'):
      
        return '+27' + phone_number[1:]
    else:
     
        return phone_number


def send_sms(to_number, message_body):
    try:
        # Twilio Account SID and Auth Token
        account_sid = secrets.get("ACCOUNT_SID")
        auth_token = secrets.get("AUTH_TOKEN")
        
        # Twilio phone number
        from_number =  secrets.get("FROM_NUMBER")

        # Create a Twilio client
        client = Client(account_sid, auth_token)


        # Send an SMS
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"SMS sent successfully. SID: {message.sid}")
    except Exception as e:
        print(f"An error occurred while sending SMS: {e}")
