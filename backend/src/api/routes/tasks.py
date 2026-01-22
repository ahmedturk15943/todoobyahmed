"""Task API routes for CRUD operations."""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
import uuid

from ..dependencies import SessionDep
from ..middleware.jwt_auth import get_current_user_id, verify_user_access
from ..models.task import TaskPublic, TaskCreate, TaskUpdate
from ...services.task_service import TaskService


router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskPublic])
async def get_tasks(
    user_id: uuid.UUID,
    session: SessionDep,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    """
    Get all tasks for a user.

    Args:
        user_id: User ID from path
        session: Database session
        current_user_id: Authenticated user ID from JWT

    Returns:
        List of tasks

    Raises:
        HTTPException: If user is not authorized
    """
    # Verify user can only access their own tasks
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access these tasks",
        )

    tasks = await TaskService.get_all_tasks(user_id, session)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: uuid.UUID,
    task_data: TaskCreate,
    session: SessionDep,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    """
    Create a new task.

    Args:
        user_id: User ID from path
        task_data: Task creation data
        session: Database session
        current_user_id: Authenticated user ID from JWT

    Returns:
        Created task

    Raises:
        HTTPException: If user is not authorized or validation fails
    """
    # Verify user can only create tasks for themselves
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create tasks for this user",
        )

    try:
        task = await TaskService.create_task(user_id, task_data, session)
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskPublic)
async def get_task(
    user_id: uuid.UUID,
    task_id: int,
    session: SessionDep,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    """
    Get a specific task.

    Args:
        user_id: User ID from path
        task_id: Task ID
        session: Database session
        current_user_id: Authenticated user ID from JWT

    Returns:
        Task details

    Raises:
        HTTPException: If user is not authorized or task not found
    """
    # Verify user can only access their own tasks
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this task",
        )

    task = await TaskService.get_task_by_id(task_id, user_id, session)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskPublic)
async def update_task(
    user_id: uuid.UUID,
    task_id: int,
    task_data: TaskUpdate,
    session: SessionDep,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    """
    Update a task.

    Args:
        user_id: User ID from path
        task_id: Task ID
        task_data: Task update data
        session: Database session
        current_user_id: Authenticated user ID from JWT

    Returns:
        Updated task

    Raises:
        HTTPException: If user is not authorized, task not found, or validation fails
    """
    # Verify user can only update their own tasks
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task",
        )

    try:
        task = await TaskService.update_task(task_id, user_id, task_data, session)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: uuid.UUID,
    task_id: int,
    session: SessionDep,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    """
    Delete a task.

    Args:
        user_id: User ID from path
        task_id: Task ID
        session: Database session
        current_user_id: Authenticated user ID from JWT

    Raises:
        HTTPException: If user is not authorized or task not found
    """
    # Verify user can only delete their own tasks
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this task",
        )

    deleted = await TaskService.delete_task(task_id, user_id, session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskPublic)
async def toggle_complete(
    user_id: uuid.UUID,
    task_id: int,
    session: SessionDep,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    """
    Toggle task completion status.

    Args:
        user_id: User ID from path
        task_id: Task ID
        session: Database session
        current_user_id: Authenticated user ID from JWT

    Returns:
        Updated task

    Raises:
        HTTPException: If user is not authorized or task not found
    """
    # Verify user can only update their own tasks
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task",
        )

    task = await TaskService.toggle_complete(task_id, user_id, session)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task
