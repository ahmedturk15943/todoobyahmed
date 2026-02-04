"""Add task MCP tool implementation."""
from typing import Optional, Dict, Any
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ...models.task import Task
from ...db import get_session

logger = logging.getLogger(__name__)


async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    MCP Tool: Create a new task.

    Args:
        user_id: User identifier
        title: Task title (required, 1-255 characters)
        description: Optional task description

    Returns:
        {"task_id": int, "status": "created", "title": str}

    Raises:
        ValueError: If validation fails
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")

    title = title.strip()

    if len(title) > 255:
        raise ValueError(f"Task title exceeds 255 characters")

    # Validate description if provided
    if description:
        description = description.strip()
        if len(description) > 10000:
            raise ValueError(f"Task description exceeds 10,000 characters")

    # Create task in database
    async for session in get_session():
        try:
            task = Task(
                user_id=user_id,
                title=title,
                description=description if description else None,
                completed=False
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"Created task {task.id} for user {user_id}: {title}")

            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }
        except Exception as e:
            await session.rollback()
            logger.error(f"Failed to create task: {str(e)}")
            raise
