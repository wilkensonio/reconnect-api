from datetime import datetime
from pydantic import EmailStr, BaseModel, field_validator


class CreateStudentResponse(BaseModel):
    id: int
    student_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str


class UserResponse(BaseModel):
    """Response model for creating a user"""

    id: int
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    created_at: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class UserUpdateResponse(BaseModel):
    """Response model for updating a user"""

    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class Get_StudentResponse(BaseModel):
    """Response model for creating a student"""

    id: int
    student_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    created_at: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class SigninResponse(BaseModel):
    """Response model for logging in a user"""
    id: int
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr


class KioskSigninResponse(BaseModel):
    """Response model for kiosk signin"""
    id: int
    student_id: str
    first_name: str
    last_name: str
    email: EmailStr
    access_token: str


class GetUsersResponse(BaseModel):
    """Response model for getting all users"""
    users: list[UserResponse]


class AvailableResponse(BaseModel):
    day: str
    start_time: str
    end_time: str

    @field_validator('start_time', 'end_time')
    def strip_seconds(cls, value):
        # Convert time from "HH:MM:SS" to "HH:MM"
        if isinstance(value, str) and len(value.split(':')) == 3:
            return value[:-3]
        return value


class CreateAppointmentResponse(BaseModel):
    id: int
    student_id: str
    faculty_id: str
    date: str
    start_time: str
    end_time: str
    reason: str
    created_at: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class GetAppointmentByIdResponse(BaseModel):
    id: int
    student_id: str
    faculty_id: str
    date: str
    start_time: str
    end_time: str
    reason: str
    created_at: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class BlacklistResponse(BaseModel):
    student_id: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class PiMessageResponse(BaseModel):
    user_id: str
    duration: int
    duration_unit: str
    message: str


class NotificationResponse(BaseModel):
    id: int
    user_id: str
    event_type: str
    message: str
