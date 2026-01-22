"""Test database connection with asyncpg driver."""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings


async def test_connection():
    """Test async database connection."""
    print(f"Testing connection to: {settings.database_url[:50]}...")
    print(f"Driver: asyncpg")

    engine = create_async_engine(
        settings.database_url,
        echo=True,
        future=True,
    )

    try:
        async with engine.begin() as conn:
            result = await conn.execute("SELECT version()")
            version = result.scalar()
            print(f"\n✓ Connection successful!")
            print(f"PostgreSQL version: {version}")
    except Exception as e:
        print(f"\n✗ Connection failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_connection())
