# Description: API routes for the application
import os
from .. import database
from ..crud import crud_user
from ..utils import jwt_utils
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm


user_crud = crud_user.UserCrud()


router = APIRouter()


def authenticate_user(db, username: str, password: str):
    user = user_crud.get_user_by_email(
        db, email=username)
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user


@router.post("/token")
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(database.get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(
        minutes=jwt_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_utils.create_access_token(
        data={
            'sub': user.email,
        },
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "Bearer"}
