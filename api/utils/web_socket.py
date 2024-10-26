from sqlalchemy.orm import Session
from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect
from ..crud import crud_notification
from ..schemas.notification_schema import NotificationSchema

notification_create = crud_notification.NotificationCrud()


async def handle_create_notification(db: Session, user_id: str, notification_data: NotificationSchema):
    """Save notification and send a real-time update."""
    success, message = notification_create.create_notification(
        db, user_id, notification_data)
    if success:
        await _notify_user(user_id, notification_data)
    return success, message


async def handle_websocket_connection(websocket: WebSocket, user_id: str):
    """Manage WebSocket lifecycle."""
    await _add_websocket_connection(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        await _remove_websocket_connection(user_id)


# In-memory storage for active WebSocket connections, mapped by user_id
_active_connections: Dict[str, WebSocket] = {}


async def _notify_user(user_id: str, message: str):
    """Send notification message to a specific user via WebSocket."""
    websocket = _active_connections.get(user_id)
    if websocket:
        await websocket.send_text(message)


async def _add_websocket_connection(user_id: str, websocket: WebSocket):
    """Add a new WebSocket connection for a specific user."""
    _active_connections[user_id] = websocket


async def _remove_websocket_connection(user_id: str):
    """Remove WebSocket connection for a user on disconnect."""
    if user_id in _active_connections:
        del _active_connections[user_id]
