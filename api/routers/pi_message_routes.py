import os
import logging
import pandas as pd
from api.crud import crud_user, crud_pi_message
from .. import database
from ..schemas import response_schema, user_schema, pi_message_schema
from api.utils import jwt_utils
from api.utils.mail_utils import EmailVerification
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from dotenv import load_dotenv


load_dotenv()

EXPRIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


router = APIRouter()

verifier = EmailVerification()
user_crud = crud_user.UserCrud()
pi_msg = crud_pi_message.PiMessage()


@router.put("/pi-message/update/{hootloot_id}", response_model=response_schema.PiMessageResponse)
async def update_user(hootloot_id: str,
                      message_update: pi_message_schema.PiMessage,
                      db: Session = Depends(database.get_db),
                      token: str = Depends(jwt_utils.oauth2_scheme)):
    """Update the message to be displayed on the pi

    Args:

        hootloot_id (str): User id, this the id of the faculty
        message_update (pi_message_schema.PiMessage): Message details to be updated
    """

    jwt_utils.verify_token(token)

    valid_duration_units = ["seconds", "minutes",
                            "hours", "days", "weeks", "months"]

    if message_update.duration_unit not in valid_duration_units:
        raise HTTPException(
            status_code=400,
            detail="Duration unit must be one of seconds, minutes, hours, days, weeks, months"
        )

    if message_update.duration <= 0:
        raise HTTPException(
            status_code=400,
            detail="Duration must be greater than 0"
        )

    try:
        int(hootloot_id)
        int(message_update.user_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="hootloot_id must be an gigit only 0-9"
        )

    try:
        is_updated = pi_msg.update_message(
            db, user_id=hootloot_id, message=message_update)
        if is_updated:

            return response_schema.PiMessageResponse(
                user_id=hootloot_id,
                message=message_update.message,
                duration=message_update.duration,
                duration_unit=message_update.duration_unit
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="User not found"
            )
    except Exception as e:
        logging.error(e)
        print(e)
        raise HTTPException(
            status_code=400,
            detail="An error occurred while attempting to update user"
        )
