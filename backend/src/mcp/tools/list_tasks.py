"""List tasks MCP tool implementation."""
from typing import List, Dict, Any
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ...models.task import Task
from ...db import get_session

logger = logging.getLogger(__name__)


async def list_tasks(
    user_id: str,
    limit: int = 50
) -> Dict[str, Any]:
    """
    MCP Tool: List user's tasks.

    Args:
        user_id: User identifier
        limit: Maximum number of tasks to return (default 50)

    Returns:
        {"tasks": [{"id": int, "title": str, "completed": bool, "description": str}], "count": int}
    """
    async for session in get_session():
        try:
            # Query tasks for user
            result = await session.execute(
                select(Task)
                .where(Task.user_id == user_id)
                .order_by(Task.created_at.desc())
                .limit(limit)
            )
            tasks = result.scalars().all()

            task_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description or "",
                    "completed": task.completed
                }
                for task in tasks
            ]

            logger.info(f"Listed {len(task_list)} tasks for user {user_id}")

            return {
                "tasks": task_list,
                "count": len(task_list)
            }
        except Exception as e:
            logger.error(f"Failed to list tasks: {str(e)}")
            raise
