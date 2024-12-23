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
async def update_message(hootloot_id: str,
                         message_update: pi_message_schema.PiMessage,
                         db: Session = Depends(database.get_db)):
    """Update the message to be displayed on the pi

    Args:

        hootloot_id (str): User id, this the id of the faculty
        message_update (pi_message_schema.PiMessage): Message details to be updated
    """

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


@router.delete("/pi-message/delete/{hootloot_id}", response_model=response_schema.PiMessageResponse)
def delete_message(hootloot_id: str,
                   db: Session = Depends(database.get_db)):
    """Delete the message to be displayed on the pi

    Args:

        hootloot_id (str): User id, this the id of the faculty
    """

    try:
        int(hootloot_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="hootloot_id must be an gigit only 0-9"
        )

    try:
        is_deleted = pi_msg.delete_message(db, user_id=hootloot_id)
        if is_deleted:
            return response_schema.PiMessageResponse(
                user_id=hootloot_id,
                message="",
                duration=0,
                duration_unit=""
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
            detail="An error occurred while attempting to delete user"
        )


@router.get("/pi-message/get/{hootloot_id}", response_model=response_schema.PiMessageResponse)
def get_message(hootloot_id: str,
                db: Session = Depends(database.get_db)):
    """Get the message to be displayed on the pi

    Args:

        hootloot_id (str): User id, this the id of the faculty
    """

    try:
        int(hootloot_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="hootloot_id must be an gigit only 0-9"
        )

    try:
        message = pi_msg.get_message(db, user_id=hootloot_id)
        if message:
            return response_schema.PiMessageResponse(
                user_id=hootloot_id,
                message=message.message,
                duration=message.duration,
                duration_unit=message.duration_unit
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
    except Exception as e:
        logging.error(e)
        print(e)
        raise HTTPException(
            status_code=400,
            detail="An error occurred while attempting to get user"
        )


@router.get("/pi-message/get-all", response_model=List[response_schema.PiMessageResponseWithUserInfo])
def get_all_messages(db: Session = Depends(database.get_db)):
    """Get all messages to be displayed on the pi

    Args:

        None
    """
    messag_results = []

    try:
        messages = pi_msg.get_all_messages(db)
        if messages:
            for message in messages:
                user = user_crud.get_user_by_id(db, user_id=message.user_id)
                messag_results.append(response_schema.PiMessageResponseWithUserInfo(
                    first_name=user.first_name,
                    last_name=user.last_name,
                    user_id=message.user_id,
                    message=message.message,
                    duration=message.duration,
                    duration_unit=message.duration_unit
                ))
            return messag_results
        else:
            raise HTTPException(
                status_code=404,
                detail="No messages found"
            )
    except Exception as e:
        logging.error(e)
        print(e)
        raise HTTPException(
            status_code=400,
            detail="An error occurred while attempting to get users"
        )
