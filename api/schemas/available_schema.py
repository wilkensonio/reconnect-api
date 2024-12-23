from datetime import datetime, date, time
from typing import Optional
from pydantic import Field, BaseModel, constr
from .common_field_model import CommonField

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


class Available(CommonField, AvailableBase):
    pass


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


#  Schema for creating an appointment


class AppointmentBase(BaseModel):
    """Request model for creating an appointment"""

    start_time: str = Field(...,
                            pattern=r'^\d{2}:\d{2}$',
                            description="The start time for the appointment (e.g. 08:00)")

    end_time: str = Field(...,
                          pattern=r'^\d{2}:\d{2}$',
                          description="The end time for the appointment (e.g. 17:00)")

    student_id: str = Field(...,
                            description="The id (HootLoot) of the student")

    faculty_id: str = Field(...,
                            description="The id (HootLoot) of the faculty")

    reason: str = Field(..., description="The reason for the appointment")

    date: str = Field(...,
                      pattern=r'^\d{4}-\d{2}-\d{2}$',
                      description="The date of the appointment")

    class Config:
        """Configurations for the schema"""
        from_attributes = True


class CreateAppointment(AppointmentBase):
    pass


class Appointment(CommonField, AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    """Request model for updating an appointment"""

    start_time: Optional[str] = Field(
        None, description="The start time for the appointment")
    end_time: Optional[str] = Field(
        None, description="The end time for the appointment")
    student_id: Optional[str] = Field(
        None, description="The id (HootLoot) of the student")
    faculty_id: Optional[str] = Field(
        None, description="The id (HootLoot) of the faculty")
    date: Optional[str] = Field(
        None, description="The date of the appointment")
    reason: Optional[str] = Field(
        None, description="The reason for the appointment")

    class Config:
        """Configurations for the schema"""
        from_attributes = True
