import os
from flask import current_app, jsonify
import sendgrid
from sendgrid.helpers.mail import *

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")


def send_verification_email(recipient, pin, token, type):
    
    current_env = os.getenv("ENV")
    
    if current_env == 'development':
        print("development env")
        recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
        from_email= os.getenv("SENDGRID_TEST_SENDER")
        url = os.getenv("DEV_URL")
    else:
        from_email=os.getenv("SENDGRID_FROM_EMAIL")
        url = os.getenv("PROD_URL")
   
    if type == 'verification':
        verification_link = f"{url}/verify?token={token}"
        content = Content("text/html", f"""
        <p>Your verification PIN is: <strong>{pin}</strong></p>
        <p>Please confirm your account by clicking the link below:</p>
        <p><a href="{verification_link}"> Click here to verify </a></p>
        """)
        subject=f'Your verification pin: {pin}'
    
    if type == 'forgotten-password':
        verification_link = f"{url}/password-reset?token={token}"
        content = Content("text/html", f"""
        <p"Your password reset PIN is: <strong>{pin}</strong></p>
        <p>Please follow the password reset link below:</p>
        <p><a href="{verification_link}"> Click here to reset your password </a></p>
        """)
        subject='Reset your password'

    mail = Mail(
        from_email=Email(from_email),
        to_emails=To(recipient),
        subject=subject,
        html_content=content
        )

    try:
        print("attempting to send email")
        sg=sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(f'finished sending email: {response.status_code}')
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {e}")
        raise