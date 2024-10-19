# This file contains user's crud operations for the api

from ..schemas import user_schema
from .. import models
from sqlalchemy.orm import Session
from sqlalchemy import select
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
                detail=f"An error occurred while attempting to signup {e}"
            )

        return new_user

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

    # start of student crud operations
    @staticmethod
    def get_student_by_id(db: Session, student_id: str):
        """Get a user by last 4 digits of  their id (HootLoot ID) or full ID

        Args:

            user_id (str): Last 4 digits or full ID or full ID of the student

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

    @staticmethod
    def get_students(db: Session):
        """Get all students

        Args:
            db (Session): Database session

        Returns:
            List[Student]: List of all students"""

        backlisted_ids = select(models.Blacklist.user_id)
        students = db.query(models.Student).filter(
            ~models.Student.student_id.in_(
                db.execute(backlisted_ids).scalars())
        ).all()
        return students

    @staticmethod
    def get_student_by_email(db: Session, email: str):
        """Get a student by email

        Args:
            db (Session): Database session
            email (str): Student email

        Returns:
            Student: Student details"""

        existing_student = db.query(models.Student).filter(
            models.Student.email == email).first()

        return existing_student

    @staticmethod
    def create_student(db: Session, student: user_schema.StudentCreate):
        """Create a new student

        Args:
            db (Session): Database session
            student (faculty_schema.StudentCreate): Student details

        return: user_schema.StudentResponse: Student details"""

        existing_student = db.query(models.Student).filter(
            models.Student.email == student.email).first()

        existing_student_id = db.query(models.Student).filter(
            models.Student.student_id == student.student_id).first()

        if existing_student:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        elif existing_student_id:
            raise HTTPException(
                status_code=400,
                detail="Student ID already registered"
            )

        try:
            new_student = models.Student(**student.model_dump())
            db.add(new_student)
            db.commit()
            db.refresh(new_student)

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"An error occurred while attempting to signup student {
                    e}"
            )

        return new_student

    @staticmethod
    def blacklist_user(db: Session, student_id: Optional[str] = None, email: Optional[str] = None):
        """Delete a student

        Args:
            db (Session): Database session
            student_id (int): Student id

        Returns:
            bool: True if student was deleted, False otherwise 
        """
        if not student_id and not email:
            return False

        if student_id:
            existing_student = db.query(models.Student).filter(
                models.Student.student_id == student_id).first()
        else:
            existing_student = db.query(models.Student).filter(
                models.Student.email == email).first()

        if existing_student:
            # Add to blacklist
            db.add(models.Blacklist(user_id=existing_student.student_id))
            db.commit()
            db.refresh(existing_student)
            return True

        return False

    @staticmethod
    def get_blacklisted_students(db: Session):
        """Get all blacklisted students

        Args:
            db (Session): Database session

        Returns:
            List[Student]: List of all blacklisted students"""

        return db.query(models.Blacklist).all()

    @staticmethod
    def reset_password(db: Session, email: str, new_password: str):
        """Reset a user's password

        Args:
            db (Session): Database session
            email (str): User email
            new_password (str): New password

        Returns:
            bool: True if password was reset, False otherwise"""

        existing_user = db.query(models.User).filter(
            models.User.email == email).first()

        if existing_user:
            existing_user.hash_password(new_password)
            db.commit()
            return True

        return False
