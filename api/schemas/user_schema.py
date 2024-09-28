from datetime import datetime
from pydantic import Field, EmailStr, BaseModel


class userBase(BaseModel):
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


class UserCreate(userBase):
    """Request model for creating a user"""
    pass


class User(userBase):
    """ auto generated id, created_at for the user"""

    id: int = Field(..., description="Auto-incremented ID of the user")
    created_at: str = Field(...,
                            description="The date and time the user was created")

    class Config:
        """Configurations for the schema"""
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class LoginRequest(BaseModel):
    """Request model for logging in a user"""
    email: EmailStr
    password: str


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


class TokenResponse(BaseModel):
    """Response model for logging in a user"""
    id: int
    first_name: str
    last_name: str
    access_token: str
    token_type: str = "bearer"


class GetUsersResponse(BaseModel):
    """Response model for getting all users"""
    users: list[UserResponse]
