from pydantic import BaseModel, Field


class NotificationSchema(BaseModel):
    """Base model for creating a notification"""

    user_id: str = Field(...,
                         description="The user id")

    event_type: str = Field(...,
                            description="The type of event")

    message: str = Field(...,
                         description="The message to be displayed")
