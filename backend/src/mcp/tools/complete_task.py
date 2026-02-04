"""Complete task MCP tool implementation."""
from typing import Dict, Any
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ...models.task import Task
from ...db import get_session

logger = logging.getLogger(__name__)


async def complete_task(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    MCP Tool: Mark a task as completed.

    Args:
        user_id: User identifier
        task_id: Task ID to complete

    Returns:
        {"task_id": int, "status": "completed", "title": str}

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    async for session in get_session():
        try:
            # Find task
            result = await session.execute(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
            )
            task = result.scalar_one_or_none()

            if not task:
                raise ValueError(f"Task {task_id} not found or does not belong to user")

            # Mark as completed
            task.completed = True
            await session.commit()
            await session.refresh(task)

            logger.info(f"Completed task {task.id} for user {user_id}: {task.title}")

            return {
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }
        except Exception as e:
            await session.rollback()
            logger.error(f"Failed to complete task: {str(e)}")
            raise
