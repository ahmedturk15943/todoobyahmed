"""Simple database connection test."""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def test():
    url = "postgresql+asyncpg://neondb_owner:npg_8c9HxvkLraDh@ep-square-king-ahxafak1-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
    print(f"Testing: {url[:60]}...")

    engine = create_async_engine(url, echo=False)

    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"SUCCESS: Connected to PostgreSQL")
            print(f"Version: {version[:80]}...")
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {str(e)[:200]}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test())
