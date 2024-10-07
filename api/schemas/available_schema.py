from datetime import datetime, date, time
from typing import Optional
from pydantic import Field, BaseModel, constr


# Schema for creating a availability (faculty)


class AvailableBase(BaseModel):
    """Base model for creating a availability (faculty)"""

    day: str = Field(...,
                     description="The day that the user is available (e.g. Monday)")

    start_time: str = Field(...,
                            pattern=r'^\d{2}:\d{2}$',
                            description="The start time for user's availability (e.g. 08:00)")

    end_time: str = Field(...,
                          pattern=r'^\d{2}:\d{2}$',
                          description="The end time for user's availability (e.g. 17:00)")

    user_id: str = Field(...,
                         description="The id (HootLoot) of the faculty", unique=True)


class CreateAvailability(AvailableBase):
    pass


class Available(AvailableBase):
    """ auto generated id, created_at for  the availability """

    id: int = Field(..., description="Auto-incremented ID of the user")
    created_at: str = Field(...,
                            description="The date and time the record was created")

    class Config:
        """Configurations for the schema"""
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class AvailableUpdate(BaseModel):
    """Request model for updating availability, inheriting from AvailableBase"""

    day: Optional[str] = Field(
        None, description="The day that the user is available"
    )
    start_time: Optional[str] = Field(
        None, description="The start time for user's availability")
    end_time: Optional[str] = Field(
        None, description="The end time for user's availability")
    faculty_id: Optional[str] = Field(
        None, description="The id (HootLoot) of the faculty")

    class Config:
        """Configurations for the schema"""
        from_attributes = True
