import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

subject = "Hey! See Barida's location"
body = "This is a test alert sent from your Barida."
receiver_email = "subhranshu.1972@gmail.com"

def send_email(receiver_email, subject, body):
    load_dotenv()

    # Email content

    sender_email = "abarpanda05@gmail.com"
    app_password = f"{os.getenv('app_password')}"

    # Prepare the email
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send the email via Gmail SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)
