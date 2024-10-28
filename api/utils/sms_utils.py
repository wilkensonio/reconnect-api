import os
import requests
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..crud.crud_user import UserCrud
from ..models import User

load_dotenv()

IFTTT_KEY = os.getenv("IFTTT_KEY")

user_crud = UserCrud()


async def send_sms(message: str):
    """Send SMS notification to a user via IFTTT. 
    """

    webhook_url = f"https://maker.ifttt.com/trigger/ReConnect_updates/with/key/{
        IFTTT_KEY}"
    requests.post(webhook_url, json={
        "value1": message,
    })


async def otp_sms(phone_number: str, otp: str):
    """Send OTP SMS notification to a user via IFTTT."""
    valid_user = await _get_user_phone_number(phone_number=phone_number)
    if not valid_user:
        raise Exception("User not found")

    # Send OTP SMS via IFTTT webhook
    webhook_url = f"https://maker.ifttt.com/trigger/OTP/with/key/{IFTTT_KEY}"
    response = requests.post(webhook_url, json={
        "value1": otp
    })

    if not response.ok:
        raise Exception("Failed to send OTP SMS notification")


async def _get_user_phone_number(db: Session = None, phone_number: str = None):
    """Get user phone number from the database."""
    user = user_crud.get_user_by_phone_number(db, phone_number)
    return user if user else None
