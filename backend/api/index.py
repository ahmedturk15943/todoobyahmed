"""Vercel serverless function entry point."""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Set environment variables if not set (fallbacks for local testing)
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://placeholder"
if not os.getenv("BETTER_AUTH_SECRET"):
    os.environ["BETTER_AUTH_SECRET"] = "placeholder-secret-key-minimum-32-chars"
if not os.getenv("JWT_ALGORITHM"):
    os.environ["JWT_ALGORITHM"] = "HS256"
if not os.getenv("JWT_EXPIRY_DAYS"):
    os.environ["JWT_EXPIRY_DAYS"] = "7"
if not os.getenv("CORS_ORIGINS"):
    os.environ["CORS_ORIGINS"] = "http://localhost:3000"
if not os.getenv("DEBUG"):
    os.environ["DEBUG"] = "false"
if not os.getenv("LOG_LEVEL"):
    os.environ["LOG_LEVEL"] = "INFO"

# Mark as Vercel environment
os.environ["VERCEL"] = "1"

try:
    # Import app after environment is set
    from src.main import app

    # Export the app for Vercel (must be named 'app')
    app = app
except Exception as e:
    # If import fails, create a minimal app for debugging
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    async def root():
        return {
            "error": "Failed to initialize main app",
            "details": str(e),
            "type": type(e).__name__
        }

    @app.get("/health")
    async def health():
        return {"status": "error", "message": str(e)}

