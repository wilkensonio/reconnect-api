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
    """Send SMS notification to a user via IFTTT."""

    webhook_url = f"https://maker.ifttt.com/trigger/ReConnect_updates/with/key/{
        IFTTT_KEY}"
    requests.post(webhook_url, json={
        "value1": message,
    })
