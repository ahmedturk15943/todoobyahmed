"""FastAPI dependencies for dependency injection."""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.connection import get_session


# Database session dependency
SessionDep = Annotated[AsyncSession, Depends(get_session)]
