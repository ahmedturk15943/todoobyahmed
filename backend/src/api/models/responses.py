"""Base response models for API endpoints."""

from pydantic import BaseModel
from typing import Optional, Any


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    message: str
    details: Optional[Any] = None


class SuccessResponse(BaseModel):
    """Standard success response format."""
    message: str
    data: Optional[Any] = None
