from .schemas import available_schema
from . import models
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional


class AvailableCrud:
    """Available crud operations"""
    @staticmethod
    def create_availability(db: Session, available: available_schema.CreateAvailability) -> models.Available:
        """Create a new available

        Args:
            db (Session): Database session
            available (faculty_schema.AvailableCreate): Available details

        return: user_schema.AvailableResponse: Available details"""

        try:
            new_available = models.Available(**available.model_dump())
            db.add(new_available)
            db.commit()
            db.refresh(new_available)
            return new_available

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"An error occurred while attempting to create available {
                    e}"
            )

    @staticmethod
    def get_availability_by_id(db: Session, available_id: int) -> Optional[models.Available]:
        """Get a available by id

        Args:
            db (Session): Database session
            available_id (int): Available id

        Returns:
            Available: Available details"""

        existing_available = db.query(models.Available).filter(
            models.Available.id == available_id).first()

        return existing_available

    @staticmethod
    def get_availabilities(db: Session) -> list[models.Available]:
        """Get all availables

        Args:
            db (Session): Database session

        Returns:
            List[Available]: List of all availables"""

        return db.query(models.Available).all()

    @staticmethod
    def delete_availability(db: Session, available_id: Optional[str] = None) -> bool:
        """Delete a available

        Args:
            db (Session): Database session
            available_id (int): Available id

            Returns:
            bool: True if available was deleted, False otherwise 
        """
        if not available_id:
            return False

        existing_available = db.query(models.Available).filter(
            models.Available.id == available_id).first()

        if existing_available:
            db.delete(existing_available)
            db.commit()
            return True

        return False

    @staticmethod
    def update_availability(db: Session, available_id: str,
                            available: available_schema.AvailableUpdate) -> Optional[models.Available]:
        """Update an availability

        Args:
            db (Session): Database session
            available_id (str): Available ID
            available (available_schema.AvailableUpdate): New availability details

        Returns:
            Available: Updated availability details or raises HTTPException if not found
        """
        existing_available = db.query(models.Available).filter(
            models.Available.id == available_id).first()

        if existing_available:
            # Update fields based on available model
            for key, value in available.model_dump().items():
                setattr(existing_available, key, value)

            db.commit()
            db.refresh(existing_available)
            return existing_available

        raise HTTPException(status_code=404, detail="Availability not found")
