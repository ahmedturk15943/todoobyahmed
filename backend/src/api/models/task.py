# # backend/src/api/models/task.py
# from pydantic import BaseModel
# from typing import Optional

# # Base task schema
# class TaskBase(BaseModel):
#     title: str
#     description: Optional[str] = None

# # Schema for creating a task
# class TaskCreate(TaskBase):
#     pass

# # Schema for updating a task
# class TaskUpdate(TaskBase):
#     completed: bool = False

# # Schema for public output
# class TaskPublic(TaskBase):
#     id: int
#     completed: bool = False






from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskPublic(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
