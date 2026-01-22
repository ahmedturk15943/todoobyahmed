"""Test database connection with corrected configuration."""
import asyncio
import sys
sys.path.insert(0, '.')

from src.db import engine, init_db
from sqlalchemy import text


async def test():
    print(f"Testing database connection...")
    print(f"Engine driver: {engine.dialect.driver}")
    print(f"Async support: {engine.dialect.is_async}")

    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"\nSUCCESS: Connected to PostgreSQL")
            print(f"Version: {version[:100]}")

        print("\nTesting init_db()...")
        await init_db()
        print("SUCCESS: Database initialized")

    except Exception as e:
        print(f"\nFAILED: {type(e).__name__}")
        print(f"Error: {str(e)[:300]}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test())
