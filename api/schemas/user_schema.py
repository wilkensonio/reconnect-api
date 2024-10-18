from datetime import datetime
from pydantic import Field, EmailStr, BaseModel
from .common_field_model import CommonField
# User schema for creating a user (faculty)


class UserBase(BaseModel):
    """Base model for creating a user"""

    user_id: str = Field(...,
                         description="Faculty ID (school id) must be unique", unique=True)

    first_name: str = Field(...,
                            description="First Name cannot be empty", min_length=1)

    last_name: str = Field(...,
                           description="Last Name cannot be empty", min_length=1)

    email: EmailStr = Field(...,
                            description="Email must be unique", unique=True)

    password: str = Field(...,
                          description="Password must be at least 8 characters", min_length=8)
    phone_number: str = Field(..., description="Phone number must be unique",
                              min_length=10)


class UserCreate(UserBase):
    """Request model for creating a user (faculty) inheriting from UserBase"""
    pass


class User(UserBase):
    """ auto generated id, created_at for the user

    inherited from UserBase"""

    id: int = Field(..., description="Auto-incremented ID of the user")
    created_at: str = Field(...,
                            description="The date and time the user was created")

    class Config:
        """Configurations for the schema"""
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

# Student schema for creating a student


class StudentBase(BaseModel):
    """Base model for creating a student

    inherited from BaseModel"""

    student_id: str = Field(...,
                            description="Student ID (school id) must be unique", unique=True)

    first_name: str = Field(...,
                            description="First Name cannot be empty", min_length=1)

    last_name: str = Field(...,
                           description="Last Name cannot be empty", min_length=1)

    email: EmailStr = Field(...,
                            description="Email must be unique", unique=True)

    phone_number: str = Field(..., description="Phone number must be unique",
                              min_length=10)


class StudentCreate(StudentBase):
    """Request model for creating a student

    inherited from StudentBase"""
    pass


class Student(CommonField, StudentBase):
    pass

# User schema for logging in a user


class LoginRequest(BaseModel):
    """Request model for logging in a user"""

    email: EmailStr
    password: str

# response models


class EmailVerification(BaseModel):
    """Request model for email verification"""
    email: EmailStr


class EmailVerificationCode(BaseModel):
    """Response model for email verification"""
    user_code: str
    secret_code: str


# kiosk schema
class KioskLoginRequest (BaseModel):
    """Request model for logging in a kiosk"""
    user_id: str


class ResetPassword(BaseModel):
    """Request model for resetting a password"""
    email: EmailStr
    password: str
