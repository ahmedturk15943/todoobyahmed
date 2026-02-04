"""Chat service for managing conversations and messages."""
from datetime import datetime
from typing import List, Dict, Optional
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ..models.conversation import Conversation
from ..models.message import Message

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing chat conversations and messages."""

    @staticmethod
    async def get_or_create_conversation(
        session: AsyncSession,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> Conversation:
        """
        Get existing conversation or create a new one.

        Args:
            session: Database session
            user_id: User identifier
            conversation_id: Optional existing conversation ID

        Returns:
            Conversation object
        """
        if conversation_id:
            # Fetch existing conversation
            result = await session.execute(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            )
            conversation = result.scalar_one_or_none()

            if not conversation:
                raise ValueError(f"Conversation {conversation_id} not found or does not belong to user")

            return conversation
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            logger.info(f"Created new conversation {conversation.id} for user {user_id}")
            return conversation

    @staticmethod
    async def get_conversation_history(
        session: AsyncSession,
        conversation_id: int,
        limit: int = 50
    ) -> List[Dict[str, str]]:
        """
        Retrieve conversation history for AI agent context.

        Args:
            session: Database session
            conversation_id: Conversation ID
            limit: Maximum number of messages to retrieve (default 50)

        Returns:
            List of messages in format [{"role": "user", "content": "..."}]
        """
        result = await session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()

        # Reverse to chronological order
        messages = list(reversed(messages))

        # Format for AI agent
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        logger.info(f"Retrieved {len(history)} messages for conversation {conversation_id}")
        return history

    @staticmethod
    async def store_messages(
        session: AsyncSession,
        conversation_id: int,
        user_id: str,
        user_message: str,
        assistant_message: str
    ) -> None:
        """
        Store user and assistant messages in the database.

        Args:
            session: Database session
            conversation_id: Conversation ID
            user_id: User identifier
            user_message: User's message content
            assistant_message: Assistant's response content
        """
        # Store user message
        user_msg = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=user_message
        )
        session.add(user_msg)

        # Store assistant message
        assistant_msg = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=assistant_message
        )
        session.add(assistant_msg)

        # Update conversation timestamp
        result = await session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one()
        conversation.updated_at = datetime.utcnow()

        await session.commit()
        logger.info(f"Stored messages for conversation {conversation_id}")
