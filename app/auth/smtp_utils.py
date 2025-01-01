from email.mime.multipart import MIMEMultipart

import smtplib

import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = os.getenv('SMTP_PORT', 587)

ENDPOINT = os.getenv('EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')

def send_email(msg: MIMEMultipart):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        try:
            server.login(ENDPOINT, APP_PASSWORD)
        except smtplib.SMTPAuthenticationError:
            raise Exception('Invalid email or app password. Make sure you\'re using an App Password, not your regular password.')
        
        server.send_message(msg)
