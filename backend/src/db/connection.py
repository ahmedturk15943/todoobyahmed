# """Database connection and session management."""

# from sqlmodel import create_engine, Session, SQLModel
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from contextlib import asynccontextmanager
# from typing import AsyncGenerator

# from ..config import settings


# # Convert PostgreSQL URL to async format
# async_database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

# # Create async engine
# engine = create_async_engine(
#     async_database_url,
#     echo=settings.debug,
#     future=True,
#     pool_pre_ping=True,
#     pool_size=10,
#     max_overflow=20,
# )

# # Create async session factory
# async_session_maker = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )


# async def init_db() -> None:
#     """Initialize database tables."""
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)


# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     """Dependency for getting async database session."""
#     async with async_session_maker() as session:
#         try:
#             yield session
#             await session.commit()
#         except Exception:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()









from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import settings

async_database_url = settings.database_url  # will be async now

engine = create_async_engine(
    async_database_url,
    echo=settings.debug,
    future=True,
    connect_args={"ssl": "require"},
)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def init_db():
    """Initialize database tables."""
    from sqlmodel import SQLModel
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session
