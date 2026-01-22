"""
TodoService - Business logic layer for in-memory task management.

Uses JSON file persistence to maintain state across CLI command invocations.
While storage is in-memory (data lost on app exit), tasks persist between commands.
"""
import json
import os
from typing import List, Optional, Dict
from src.models.task import Task


class TodoService:
    """
    Service layer for managing todo items in memory with file-based persistence.

    Handles all business logic including:
    - Adding tasks with auto-incrementing IDs
    - Listing all tasks
    - Updating task details
    - Deleting tasks by ID
    - Marking tasks as complete
    - Input validation
    - File-based persistence for state across command invocations
    """

    # Persistence file path (in project root, gitignored)
    DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".todo_data.json")

    def __init__(self):
        """Initialize service by loading from persistence file or creating empty storage."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1
        self.load()

    def load(self) -> None:
        """Load tasks from JSON persistence file.

        IMPORTANT: Task IDs from JSON are ignored to ensure IDs always start
        from 1 on restart. All tasks are renumbered sequentially.
        """
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Load raw tasks from JSON (IDs in JSON are ignored)
                    raw_tasks = data.get("tasks", {})
                    # Renumber tasks with sequential IDs starting from 1
                    self.tasks = {}
                    for index, (old_id, task_data) in enumerate(sorted(raw_tasks.items(), key=lambda x: int(x[0]))):
                        new_id = index + 1
                        self.tasks[new_id] = Task(
                            task_id=new_id,
                            title=task_data["title"],
                            description=task_data.get("description", ""),
                            status=task_data.get("status", "incomplete"),
                            created_at=task_data.get("created_at")
                        )
                    # next_id is always 1 + count of tasks
                    self.next_id = len(self.tasks) + 1
            except (json.JSONDecodeError, FileNotFoundError, IOError, ValueError) as e:
                # If file is corrupted or unreadable, start fresh
                print(f"Warning: Could not load data file, starting fresh: {e}")
                self.tasks = {}
                self.next_id = 1
        else:
            # No file exists, start with empty storage
            self.tasks = {}
            self.next_id = 1

    def save(self) -> None:
        """Save tasks to JSON persistence file (without IDs for clean restart behavior)."""
        try:
            data = {
                "tasks": {
                    str(task_id): {
                        "title": task.title,
                        "description": task.description,
                        "status": task.status,
                        "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else task.created_at
                    }
                    for task_id, task in self.tasks.items()
                }
            }
            with open(self.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save data file: {e}")

    def add(self, title: str, description: str = "") -> Task:
        """
        Add a new task to in-memory storage.

        Args:
            title: Brief task name (required, validated non-empty)
            description: Detailed task information (optional)

        Returns:
            Task: The newly created task

        Raises:
            ValueError: If title is empty
        """
        if not title or not title.strip():
            raise ValueError("Task title is required")

        # Trim whitespace from title
        title = title.strip()

        # Create new task with auto-incrementing ID
        task = Task(
            task_id=self.next_id,
            title=title,
            description=description,
            status="incomplete"
        )

        # Store in memory and increment ID
        self.tasks[task.id] = task
        self.next_id += 1

        # Persist to file
        self.save()

        return task

    def list_all(self) -> List[Task]:
        """
        Retrieve all tasks from in-memory storage.

        Returns:
            List[Task]: All tasks ordered by ID
        """
        return [self.tasks[task_id] for task_id in sorted(self.tasks.keys())]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: Unique identifier of task

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        return self.tasks.get(task_id)

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task's details.

        Args:
            task_id: Unique identifier of task to update
            title: New title for task (optional)
            description: New description for task (optional)

        Returns:
            Optional[Task]: The updated task if found, None otherwise

        Raises:
            ValueError: If task with given ID does not exist
        """
        task = self.get_by_id(task_id)

        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        # Update task details
        task.update_details(title=title, description=description)

        # Persist to file
        self.save()

        return task

    def delete(self, task_id: int) -> bool:
        """
        Delete a task from in-memory storage.

        Args:
            task_id: Unique identifier of task to delete

        Returns:
            bool: True if task was deleted, False if task not found

        Raises:
            ValueError: If task with given ID does not exist
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} not found")

        del self.tasks[task_id]
        self.save()

        return True

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id: Unique identifier of task to mark complete

        Returns:
            Optional[Task]: The updated task if found, None otherwise

        Raises:
            ValueError: If task with given ID does not exist
        """
        task = self.get_by_id(task_id)

        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        task.mark_complete()
        self.save()

        return task

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id: Unique identifier of task to mark incomplete

        Returns:
            Optional[Task]: The updated task if found, None otherwise

        Raises:
            ValueError: If task with given ID does not exist
        """
        task = self.get_by_id(task_id)

        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")

        task.mark_incomplete()
        self.save()

        return task

    def is_empty(self) -> bool:
        """Check if there are any tasks in storage."""
        return len(self.tasks) == 0
