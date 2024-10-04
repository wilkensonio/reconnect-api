import os
import logging
import random
import smtplib
import string
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


logging.basicConfig(level=logging.INFO)


def _generate_verification_code(length=6) -> str:
    """Generate a random verification code of specified length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def _send_email(email: str, subject: str, message: str) -> bool:
    """Send an email message.

    Args:
        email (str): Email address to send the message
        subject (str): Email subject
        message (str): Email message

    Returns:
        bool: Email sent status
    """
    # SMTP configuration for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("SENDER_EMAIL")
    # use app password
    sender_password = os.getenv("SENDER_PASSWORD")

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = email

    try:
        # Establish connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Email sent to {email}")
        logging.info(f"Email sent to {email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False


def verification(email: str) -> dict:
    """Send an email verification message.

    Args:
        email (str): Email address

    Returns:
        bool: Email sent status
    """
    verification_code = _generate_verification_code()
    subject = "Email Verification"
    message = f"Your email verification code is: {verification_code}"

    if _send_email(email, subject, message):
        return {
            "verification_code": verification_code
        }
    return {
        "verification_code": "failed"
    }


def verify_email_code(user_code: str, secret_code: str) -> dict:
    """Verify email address using verification code.

    Args:
        email (str): Email address
        code (str): Verification code

    Returns:
        bool: Email verification status
    """
    print(user_code, secret_code)
    return {"details": user_code == secret_code}
