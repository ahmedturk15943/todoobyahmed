"""Delete task MCP tool implementation."""
from typing import Dict, Any
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ...models.task import Task
from ...db import get_session

logger = logging.getLogger(__name__)


async def delete_task(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    MCP Tool: Delete a task.

    Args:
        user_id: User identifier
        task_id: Task ID to delete

    Returns:
        {"task_id": int, "status": "deleted", "title": str}

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

            title = task.title
            task_id = task.id

            # Delete task
            await session.delete(task)
            await session.commit()

            logger.info(f"Deleted task {task_id} for user {user_id}: {title}")

            return {
                "task_id": task_id,
                "status": "deleted",
                "title": title
            }
        except Exception as e:
            await session.rollback()
            logger.error(f"Failed to delete task: {str(e)}")
            raise
