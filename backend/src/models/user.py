"""User model for authentication and task ownership."""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class User(SQLModel, table=True):
    """User entity with authentication credentials."""
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks (will be defined when Task model is created)
    # tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)


class UserPublic(SQLModel):
    """Public user model (without password hash)."""
    id: uuid.UUID
    email: str
    created_at: datetime
    updated_at: datetime
