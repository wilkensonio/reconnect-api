from datetime import datetime
from pydantic import Field, EmailStr, BaseModel


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


class TokenResponse(BaseModel):
    """Response model for logging in a user"""
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    access_token: str
    token_type: str = "bearer"


class GetUsersResponse(BaseModel):
    """Response model for getting all users"""
    users: list[UserResponse]

# Email verification schema
