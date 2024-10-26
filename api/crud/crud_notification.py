# This file contains user's crud operations for the api


from ..schemas import notification_schema
from .. import models
from sqlalchemy.orm import Session


class NotificationCrud:
    """Update the the message to be displayed on the pi"""

    @staticmethod
    def create_notification(db: Session, user_id: str, notification: notification_schema.NotificationSchema):
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
            return False, "User not found"

        try:
            new_notification = models.Notification(**notification.model_dump())
            db.add(new_notification)
            db.commit()
            db.refresh(new_notification)
            return True, "Notification created"
        except Exception as e:
            print(e)
            return False, e

    @staticmethod
    def get_notifications(db: Session):
        """Get all notifications for a user

        Args:
            db (Session): Database session

        Returns:
            list: List of notifications
        """
        notifications = db.query(models.Notification).filter(
            models.Notification).all()

        return notifications

    @staticmethod
    def get_notification_by_user(db: Session, user_id: str):
        """Get all notifications for a user

        Args:
            db (Session): Database session
            user_id (str): User id
            notification_id (int): Notification id

        Returns:
            Notification: Notification object
        """

        notifications = db.query(models.Notification).filter(
            models.Notification.user_id == user_id
        ).all()

        return notifications

    @staticmethod
    def delete_notification_by_id(db: Session, notification_id: int):
        """Delete a notification by id

        Args:
            db (Session): Database session
            user_id (str): User id
            notification_id (int): Notification id

        Returns:
            bool: True if notification was deleted, False otherwise
        """

        notification = db.query(models.Notification).filter(
            models.Notification.id == notification_id
        ).first()

        if notification:
            db.delete(notification)
            db.commit()
            return True, "Notification deleted"

        return False, "Notification not found"

    @staticmethod
    def delete_notification_by_user(db: Session, user_id: str):
        """Delete all notifications for a user

        Args:
            db (Session): Database session
            user_id (str): User id

        Returns:
            bool: True if notification was deleted, False otherwise
        """

        notifications = db.query(models.Notification).filter(
            models.Notification.user_id == user_id
        ).all()

        if notifications:
            for notification in notifications:
                db.delete(notification)
            db.commit()
            return True, "Notifications deleted"

        return False, "Notifications not found"
