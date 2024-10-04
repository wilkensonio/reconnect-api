# This file contains user's crud operations for the api

from .schemas import user_schema
from . import models
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional


# start of user (faculty) crud operations

def create_user(db: Session, user: user_schema.UserCreate):
    """Create a new user

    Args:
        db (Session): Database session
        user (faculty_schema.UserCreate): User details

    return: user_schema.UserResponse: User details"""

    try:
        existing_user = db.query(models.User).filter(
            models.User.email == user.email).first()

        new_user = models.User(**user.model_dump())
        new_user.hash_password(user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception as e:
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        raise HTTPException(
            status_code=400,
            detail="An error occurred while attempting to signup"
        )

    response = user_schema.UserResponse(
        id=new_user.id,
        user_id=new_user.user_id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        phone_number=new_user.phone_number,
        created_at=new_user.created_at
    )

    return response


def get_user_by_email(db: Session, email: str):
    """Get a user by email

    Args:
        db (Session): Database session
        email (str): User email

    Returns:
        User: User details"""

    existing_user = db.query(models.User).filter(
        models.User.email == email).first()

    return existing_user


def get_users(db: Session):
    """Get all users

    Args:
        db (Session): Database session

    Returns:
        List[User]: List of all users"""

    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: str):
    """Get a user by id (user_id) the hootloop id

    Args:
        db (Session): Database session
        user_id (int): User id

        Returns:
        User: User details
    """

    existing_user = db.query(models.User).filter(
        models.User.user_id == user_id).first()

    return existing_user


def delete_user(db: Session, user_id: Optional[str] = None, email: Optional[str] = None):
    """Delete a user

    Args:
        db (Session): Database session
        user_id (int): User id

        Returns:
        bool: True if user was deleted, False otherwise 
    """
    if not user_id and not email:
        return False

    if user_id:
        existing_user = db.query(models.User).filter(
            models.User.user_id == user_id).first()
    else:
        existing_user = db.query(models.User).filter(
            models.User.email == email).first()

    if existing_user:
        db.delete(existing_user)
        db.commit()
        return True

    return False


# end of user (faculty) crud operations

# start of student crud operations
def get_student_by_id(db: Session, student_id: str):
    """Get a user by last 4 digits of  their id (HootLoot ID) or full ID

    Args:

        user_id (str): Last 4 digits or full ID

    Returns:

        Object: User details    
    """

    if len(student_id) == 4:
        # Query to check if the last 4 digits match the given ID
        existing_user = db.query(models.Student).filter(
            models.Student.student_id.like(f"%{student_id}")
        ).first()
    else:
        existing_user = db.query(models.Student).filter(
            models.Student.student_id == student_id).first()

    return existing_user
