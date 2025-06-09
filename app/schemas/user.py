from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")

class UserCreate(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=50, description="First name")
    lastName: str = Field(..., min_length=1, max_length=50, description="Last name")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password must be at least 8 characters")
    confirmPassword: str = Field(..., description="Password confirmation")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class UserResponse(BaseModel):
    id: str = Field(..., description="User ID as string")
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., description="User's full name")
    createdAt: str = Field(..., description="User creation timestamp in ISO format")

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class LogoutResponse(BaseModel):
    message: str = Field(..., description="Logout success message")
    success: bool = Field(default=True, description="Logout operation success status")
