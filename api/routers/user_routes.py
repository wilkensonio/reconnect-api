# Description: API routes for the application
import os
import logging
from .. import crud, database
from ..schemas import user_schema
from api import jwt_utils
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
EXPRIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


router = APIRouter(prefix="/api/v1")


@router.post("/signup/", response_model=user_schema.UserResponse)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(database.get_db)):
    """Create a new user

    Attributes
    ----------
    user : user_schema.UserCreate
        User details
    db : Session
        Database session

    Raises
    ------
    HTTPException
        Email already registered
        An error occurred while attempting to signup

    Returns
    -------
    user_schema.UserResponse
        User details

    """
    return crud.create_user(db=db, user=user)


@router.post("/signin/", response_model=user_schema.TokenResponse)
async def login_user(
    login_request: user_schema.LoginRequest,
    db: Session = Depends(database.get_db),
):
    """Login a user

    Attributes
    ----------
    login_request : user_schema.LoginRequest
        User login details
    db : Session
        Database session

    Raises
    ------
    HTTPException
        code : 400
        User not found
        Invalid email or password

    Returns
    -------
    user_schema.TokenResponse
        User details with access token 
    """

    user = crud.get_user_by_email(db, email=login_request.email)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    if not user.check_password(login_request.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    #  create access token (JWT) for the user
    access_token_expires = timedelta(minutes=int(EXPRIRES_MINUTES))
    access_token = jwt_utils.create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )

    response = user_schema.TokenResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        access_token=access_token,
        token_type="bearer"
    )

    return response


@router.get("/users/", response_model=list[user_schema.UserResponse])
async def get_users(db: Session = Depends(database.get_db)):
    """Retrieve all users.

    Attributes
    ----------
    db : Session
        Database session

    Raises
    ------
    HTTPException
        code : 400
        An error occurred while attempting to retrieve users

    Returns
    -------
    list[user_schema.UserResponse]
        List of all users"""

    try:
        users = crud.get_users(db)
        return users
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=400,
            detail="An error occurred while attempting to retrieve users"
        )


@router.get("/user/email/{email}", response_model=user_schema.UserResponse)
async def get_user_by_email(email: str, db: Session = Depends(database.get_db)):
    """Retrieve a user by email.

    Attributes
    ----------

    email : str
        User email
    db : Session
        Database session

    Raises
    ------
    HTTPException
        code : 400
        User not found

    Returns
    -------
    user_schema.UserResponse
        User details"""
    try:
        user = crud.get_user_by_email(db, email)
        return user
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )


@router.get("/user/id/{user_id}", response_model=user_schema.UserResponse)
def get_user_by_id(user_id: str, db: Session = Depends(database.get_db)):
    """Retrieve a user by id.

    Attributes
    ----------

    user_id : str
        User id
    db : Session
        Database session

    Raises
    ------
    HTTPException
        code : 404
        User not found

    Returns
    -------
    user_schema.UserResponse
        User details"""

    user = crud.get_user_by_id(db, user_id)
    return user


@router.delete("/user/delete/{email_or_id}", response_model=dict)
def delete_by_email_or_id(email_or_id: str, db: Session = Depends(database.get_db)):
    """Delete a user by id or by email

    Attributes
    ----------
        email_or_id : str
            User email or user_id
        db : Session
            Database session

    Raises
    ------
    HTTPException
        code : 400
        User not found
        An error occurred while attempting to delete user

    Returns
    -------
    dict
        Response message
         """
    try:
        if crud.delete_user(db, email=email_or_id):
            return {"message": "User deleted successfully"}
        elif crud.delete_user(db, user_id=email_or_id):
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(
                status_code=400,
                detail="User not found"
            )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=400,
            detail="An error occurred while attempting to delete user"
        )


# Kiosk sign-in

@router.post("/kiosk-signin/", response_model=user_schema.TokenResponse)
async def kiosk_login(
    login_request: user_schema.KioskLoginRequest,
    db: Session = Depends(database.get_db),
):
    """Login a user via kiosk (using last 4 digits of ID or full barcode)"""
    user = crud.get_student_by_id(db, login_request.user_id)
    print(user)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    #  create access token (JWT) for the user
    access_token_expires = timedelta(minutes=int(EXPRIRES_MINUTES))
    access_token = jwt_utils.create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )

    return user_schema.TokenResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        access_token=access_token,
        token_type="bearer"
    )
