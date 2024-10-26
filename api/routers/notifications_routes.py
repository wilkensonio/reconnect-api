
from api.crud import crud_notification
from .. import database
from ..schemas import response_schema, notification_schema
from api.utils import jwt_utils
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter()

notify = crud_notification.NotificationCrud()


@router.post("/new/notification/{hootloot_id}", response_model=response_schema.NotificationResponse)
async def update_user(hootloot_id: str,
                      notification: notification_schema.NotificationSchema,
                      db: Session = Depends(database.get_db),
                      token: str = Depends(jwt_utils.oauth2_scheme)):
    """ show notification to faculty dashboard
    Args:

        hootloot_id (str): user id
        enven_type (str): event type of the notification, (e.g. "appointment scheduled or appointment cancelled")
        message (str): the notification message


    Returns:

        response_schema.NotificationResponse: notification details
    """

    jwt_utils.verify_token(token)

    try:
        int(notification.user_id)
        int(hootloot_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="hootloot_id must be  digits only 0-9"
        )

    is_created, msg = notify.create_notification(
        db, user_id=notification.user_id, notification=notification)

    if not is_created:
        raise HTTPException(
            status_code=400,
            detail=msg
        )

    try:
        if is_created:
            return response_schema.NotificationResponse(
                user_id=notification.user_id,
                event_type=notification.event_type,
                message=notification.message
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="User not found"
            )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=msg
        )


@router.get("/notifications_by_user/{hootloot_id}", response_model=List[response_schema.NotificationResponse])
async def get_notification_by_user(hootloot_id: str, db: Session = Depends(database.get_db),
                                   token: str = Depends(jwt_utils.oauth2_scheme)):
    """Get all notifications for a user

    Args:

        hootloot_id (str): User id

    Returns:

        list: List of notifications
    """
    jwt_utils.verify_token(token)

    try:
        int(hootloot_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="hootloot_id must be  digits only 0-9"
        )

    notifications = notify.get_notification_by_user(db, user_id=hootloot_id)

    return notifications


@router.delete("/delete/notification/{notification_id}", response_model=dict)
async def delete_notification_by_id(notification_id: int, db: Session = Depends(database.get_db),
                                    token: str = Depends(jwt_utils.oauth2_scheme)):
    """Delete a notification by id

    Args:

        notification_id (int): Notification id

    Returns:

        bool: True if notification was deleted, False otherwise
    """
    jwt_utils.verify_token(token)

    try:
        int(notification_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="notification_id must be  digits only 0-9"
        )

    is_deleted, msg = notify.delete_notification_by_id(
        db, notification_id=notification_id)

    if not is_deleted:
        raise HTTPException(
            status_code=400,
            detail=msg
        )

    else:
        return {"details": "notification deleted"}


@router.delete("/delete/notifications/{hootloot_id}", response_model=dict)
async def delete_notification_by_user(hootloot_id: str, db: Session = Depends(database.get_db),
                                      token: str = Depends(jwt_utils.oauth2_scheme)):
    """Delete all notifications for a user

    Args:

        hootloot_id (str): User id

    Returns:

        bool: True if notification was deleted, False otherwise
    """
    jwt_utils.verify_token(token)

    try:
        int(hootloot_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="hootloot_id must be  digits only 0-9"
        )

    is_deleted, msg = notify.delete_notification_by_user(
        db, user_id=hootloot_id)

    if not is_deleted:
        raise HTTPException(
            status_code=400,
            detail=msg
        )

    else:
        return {"details": "notifications deleted"}
