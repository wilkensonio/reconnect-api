# This file contains user's crud operations for the api

from .schemas import user_schema
from . import models
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional


# start of user (faculty) crud operations
class UserCrud:
    """User crud operations"""
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_users(db: Session):
        """Get all users

        Args:
            db (Session): Database session

        Returns:
            List[User]: List of all users"""

        return db.query(models.User).all()

    @staticmethod
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

    @staticmethod
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
