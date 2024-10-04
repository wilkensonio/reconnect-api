import os
import logging
import random
import string

from mailjet_rest import Client
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

    #
    api_key = os.getenv("MAILJET_API_KEY")
    api_secret = os.getenv("MAILJET_SECRET_KEY")
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    data = {
        "Messages": [
            {

                'From': {
                    'Email': os.getenv("SENDER_EMAIL"),
                    'Name': 'Reconnect'
                },
                "TO": [
                    {"Email": email}
                ],
                'Subject': subject,
                'TextPart': message,
                'HtmlPart': f'<p>{message}</p>'
            }
        ]
    }
    try:
        # Send the email
        result = mailjet.send.create(data=data)

        # Check the response status
        if result.status_code == 200:
            print("Email sent successfully.")
            return True
        else:
            print(f"Failed to send email: {
                  result.status_code}, {result.json()})")
            return False

    except Exception as e:
        print(f"Mailjet API Error: {e.status_code}, {e.message}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
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
    message = f"""
    <div style="max-width: 400px; margin: auto; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-family: Arial, sans-serif;">
        <img src="https://drive.google.com/uc?export=view&id=1EnVBFhU4SrfOTeiwO_CJt0XTblmVktQP"
          alt="Logo" style="width: 80%; height: 150px; max-width: 200px; margin: 0 auto; display: block;">
        <div style="padding: 2rem;">
            <h2 style="color: #333;">Email Verification</h2>
            <p style="font-size: 16px; color: #555;">Your email verification code is:</p>
            <h3 style="color: #007bff;">{verification_code}</h3>
            <p style="color: #777;">Please use this code to verify your email address.</p>
            <p style="font-size: 14px; color: #999;">If you did not request this, please ignore this email.</p>
        </div>
    </div>
    """

    if _send_email(email, subject, message):
        return {
            "verification_code": verification_code
        }
    return {
        "verification_code": ""
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
