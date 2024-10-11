from datetime import datetime
from typing import ClassVar
from pydantic import BaseModel, ConfigDict, Field


class CommonField(BaseModel):
    """ auto generated id, created_at for  the appointment """

    id: int = Field(..., description="Auto-incremented ID of the appointment")
    created_at: str = Field(...,
                            description="The date and time the record was created")

    class Config:
        """Configurations for the schema"""
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
