# This file contains user's crud operations for the api


from ..schemas import pi_message_schema
from .. import models
from sqlalchemy.orm import Session


# start of user (faculty) crud operations
class PiMessage:
    """Update the the message to be displayed on the pi"""

    @staticmethod
    def update_message(db: Session, user_id: str, message: pi_message_schema.PiMessage):
        """Update a user's details

        Args:
            db (Session): Database session
            user_id (str): User id
            user (faculty_schema.UserUpdate): User details

        Returns:
            bool: True if user was updated, False otherwise"""

        existing_user = db.query(models.User).filter(
            models.User.user_id == user_id).first()

        if not existing_user:
            return False

        pi_message = db.query(models.PiMessage).filter(
            models.PiMessage.user_id == user_id).first()

        if pi_message:
            pi_message.update_message(**message.model_dump())
            db.commit()
            return True

        elif not pi_message:
            new_pi_message = models.PiMessage(**message.model_dump())
            db.add(new_pi_message)
            db.commit()
            return True

        return False

    @staticmethod
    def delete_message(db: Session, user_id: str):
        """Delete a user's message

        Args:
            db (Session): Database session
            user_id (str): User id

        Returns:
            bool: True if user was deleted, False otherwise"""

        pi_message = db.query(models.PiMessage).filter(
            models.PiMessage.user_id == user_id).first()

        if pi_message:
            db.delete(pi_message)
            db.commit()
            return True

        return False

    @staticmethod
    def get_message(db: Session, user_id: str):
        """Get a user's message

        Args:
            db (Session): Database session
            user_id (str): User id

        Returns:
            models.PiMessage: User's message"""

        return db.query(models.PiMessage).filter(models.PiMessage.user_id == user_id).first()

    @staticmethod
    def get_all_messages(db: Session):
        """Get all messages

        Args:
            db (Session): Database session

        Returns:
            List[models.PiMessage]: List of all messages"""

        return db.query(models.PiMessage).all()
