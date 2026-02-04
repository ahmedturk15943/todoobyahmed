# from sqlmodel import Session, create_engine
# from .config import settings

# engine = create_engine(
#     settings.database_url,
#     echo=settings.debug,
#     pool_pre_ping=True,
# )

# def get_session():
#     with Session(engine) as session:
#         yield session





"""Database connection and session management for Todo App."""

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# Async engine for PostgreSQL (using asyncpg)
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug,
    pool_pre_ping=True,
)

# Async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency for FastAPI endpoints
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session