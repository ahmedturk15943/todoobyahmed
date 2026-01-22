"""Authentication request and response models."""

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime


class SignUpRequest(BaseModel):
    """Request model for user signup."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class SignInRequest(BaseModel):
    """Request model for user signin."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User data in API responses."""
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime


class AuthResponse(BaseModel):
    """Response model for authentication endpoints."""
    user: UserResponse
    token: str
    message: str
