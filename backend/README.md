# Todo Backend - FastAPI

**Version**: 2.0.0
**Phase**: Phase II - Multi-User Web Application
**Framework**: FastAPI with SQLModel ORM

## Overview

RESTful API backend for the Todo application with user authentication, task management, and PostgreSQL persistence.

## Features

- User authentication with JWT tokens
- Task CRUD operations with data isolation
- PostgreSQL database with SQLModel ORM
- Automatic API documentation (OpenAPI/Swagger)
- Async/await for non-blocking operations
- Comprehensive error handling

## Prerequisites

- Python 3.13+
- UV package manager
- Neon PostgreSQL database (or local PostgreSQL)

## Setup

### 1. Install Dependencies

```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared secret for JWT verification (32+ characters)
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### 3. Initialize Database

```bash
# Run database initialization script
python -m src.db.init_db
```

### 4. Start Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --port 8000
```

Server will start at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Testing

```bash
# Run all tests
pytest

# Run specific test types
pytest -m unit
pytest -m integration
pytest -m contract

# Run with coverage
pytest --cov=src --cov-report=html
```

## Project Structure

```
backend/
├── src/
│   ├── models/          # SQLModel entities
│   ├── services/        # Business logic
│   ├── api/
│   │   ├── routes/      # API endpoints
│   │   └── middleware/  # JWT auth, error handling
│   ├── db/              # Database connection
│   ├── config.py        # Configuration management
│   └── main.py          # FastAPI app entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── pyproject.toml
└── pytest.ini
```

## Development

### Code Quality

```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Type checking (if using mypy)
mypy src
```

### Database Migrations

For schema changes, use Alembic:

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Troubleshooting

### Database Connection Issues

- Verify `DATABASE_URL` in `.env` is correct
- Check Neon database is accessible
- Ensure connection string includes `sslmode=require` for Neon

### JWT Authentication Errors

- Verify `BETTER_AUTH_SECRET` matches frontend configuration
- Check token expiry (default 7 days)
- Ensure Authorization header format: `Bearer <token>`

## License

Copyright (c) 2025 Evolution of Todo Project. All rights reserved.
