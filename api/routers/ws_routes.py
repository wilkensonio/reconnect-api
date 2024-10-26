from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from ..utils.web_socket import handle_create_notification, handle_websocket_connection
from ..database import get_db
from ..schemas.notification_schema import NotificationSchema

router = APIRouter()


@router.post("/ws_create_notifications/{user_id}")
async def create_notification_route(user_id: str, notification_data: NotificationSchema,
                                    db: Session = Depends(get_db)):
    """HTTP route to create a notification.

    Args: 

        user_id (str): User id
        notification_data (NotificationSchema): Notification details

        Returns:

            dict: Success status and message"""
    success, message = await handle_create_notification(db, user_id, notification_data)
    return {"success": success, "message": message}


@router.websocket("/ws/notifications/{user_id}")
async def notifications_websocket_route(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time notifications."""
    await handle_websocket_connection(websocket, user_id)
