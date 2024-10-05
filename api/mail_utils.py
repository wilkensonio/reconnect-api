import os
import logging
import random
import string
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Configure logging
logging.basicConfig(level=logging.INFO)


load_dotenv()


class EmailVerification:
    """Handle sending and verification of email codes."""

    def __init__(self):

        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = os.getenv("SMTP_PORT")
        self.SENDER_EMAIL = os.getenv("SENDER_EMAIL")
        self.SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

    def _generate_verification_code(self, length=6) -> str:
        """Generate a random verification code of specified length."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def _send_email(self, email: str, subject: str, message: str) -> bool:
        """Send an email message.

        Args:
            email (str): Email address to send the message
            subject (str): Email subject
            message (str): Email message

        Returns:
            bool: Email sent status
        """
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = self.SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))  # Attach the HTML message

        try:
            # Connect to the SMTP server
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()  # Use TLS for security
                server.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)  # Login
                server.sendmail(self.SENDER_EMAIL, email,
                                msg.as_string())  # Send email

            print("Email sent successfully.")
            logging.info(f"Email sent to {email}")
            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def verification(self, email: str) -> dict:
        """Send an email verification message.

        Args:
            email (str): Email address

        Returns:
            dict: Verification code details
        """
        verification_code = self._generate_verification_code()
        subject = "Email Verification"
        message = f"""
        <div style="max-width: 400px; margin: auto; border: 1px solid #ccc; border-radius: 8px;
        overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-family: Arial, sans-serif;">
            <div style="padding: 2rem;">
                <h2 style="color: #333;">Email Verification</h2>
                <p style="font-size: 16px; color: #555;">Your email verification code is:</p>
                <h3 style="color: #007bff;">{verification_code}</h3>
                <p style="color: #777;">Please use this code to verify your email address.</p>
                <p style="font-size: 14px; color: #999;">If you did not request this, please ignore this email.</p>
                <div style="margin-top: 2rem; padding: 1rem; background-color: #474b46; border: 1px solid #f5c6cb;>
                <p style="font-size: 14px; font-weight:bold; color: red;">This email is not being monitored please do not reply to it.</p>
                </div>
            </div>
        </div>
        """

        if self._send_email(email, subject, message):
            return {
                "verification_code": verification_code
            }
        return {
            "verification_code": ""
        }

    @staticmethod
    def verify_email_code(user_code: str, secret_code: str) -> dict:
        """Verify email address using verification code.

        Args:
            user_code (str): User's verification code
            secret_code (str): Secret verification code sent via email

        Returns:
            dict: Verification result
        """
        print(user_code, secret_code)
        return {"details": user_code == secret_code}
