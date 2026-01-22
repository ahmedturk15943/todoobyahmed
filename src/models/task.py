"""
Task entity model for in-memory todo management.
"""
from typing import Optional
from datetime import datetime


class Task:
    """Represents a todo item with all required attributes."""

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        status: str = "incomplete",
        created_at: Optional[datetime] = None
    ):
        """
        Initialize a Task object.

        Args:
            task_id: Unique integer identifier
            title: Brief task name (required, non-empty)
            description: Detailed task information (optional, defaults to empty)
            status: Completion state - "complete" or "incomplete" (default: "incomplete")
            created_at: ISO 8601 timestamp when task was created
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at if created_at else datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert task to dictionary for storage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }

    def is_complete(self) -> bool:
        """Check if task is marked as complete."""
        return self.status == "complete"

    def mark_complete(self) -> None:
        """Mark task as complete."""
        self.status = "complete"

    def mark_incomplete(self) -> None:
        """Mark task as incomplete."""
        self.status = "incomplete"

    def update_details(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Update task title and/or description.

        Args:
            title: New title for the task (optional)
            description: New description for the task (optional)
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
