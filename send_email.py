# send_email.py

import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(to_email, subject, content):
    """Sends an email using SMTP."""
    try:
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        st.error(f"Error sending email: {e}")
        # Optionally, log the error or handle it as needed
