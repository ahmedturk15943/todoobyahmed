# """Message model for AI chatbot feature."""
# from datetime import datetime
# from typing import Optional, Literal
# from sqlmodel import SQLModel, Field, Relationship


# class Message(SQLModel, table=True):
#     """
#     Represents a single message in a conversation.
#     Can be from either the user or the AI assistant.
#     """
#     __tablename__ = "messages"

#     id: Optional[int] = Field(default=None, primary_key=True)
#     conversation_id: int = Field(foreign_key="conversations.id", index=True)
#     user_id: str = Field(foreign_key="users.id", index=True)
#     role: Literal["user", "assistant"] = Field()
#     content: str = Field()
#     created_at: datetime = Field(default_factory=datetime.utcnow)

#     # Relationships
#     conversation: Optional["Conversation"] = Relationship(back_populates="messages")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "id": 1,
#                 "conversation_id": 1,
#                 "user_id": "user_123abc",
#                 "role": "MessageRole"   
#                 "content": "Add a task to buy groceries",
#                 "created_at": "2026-01-29T10:00:00Z"
#             }
#         }




"""Message model for AI chatbot feature."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    role: MessageRole
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "conversation_id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "role": "user",
                "content": "Add a task to buy groceries",
                "created_at": "2026-01-29T10:00:00Z"
            }
        }
