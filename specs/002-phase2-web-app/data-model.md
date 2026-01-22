# Data Model: Full-Stack Multi-User Todo Web Application

**Feature**: 002-phase2-web-app | **Date**: 2026-01-21

This document defines the data entities, their attributes, relationships, and validation rules.

## Entity Definitions

### User Entity

**Purpose**: Represents an individual user account with authentication credentials.

**Attributes**:

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | Primary Key, Auto-generated | Unique identifier for the user |
| email | String | Required, Unique, Max 255 chars | User's email address (used for login) |
| password_hash | String | Required, Max 255 chars | Bcrypt hashed password (never store plain text) |
| created_at | Timestamp | Auto-generated | Account creation timestamp |
| updated_at | Timestamp | Auto-updated | Last modification timestamp |

**Validation Rules**:
- Email must be valid format (contains @, valid domain)
- Email must be unique across all users
- Password must be minimum 8 characters before hashing
- Password must contain at least one letter and one number (recommended)
- Password hash uses bcrypt with minimum 10 rounds

**Indexes**:
- Primary index on `id` (automatic)
- Unique index on `email` (for fast lookup during signin)

**State Transitions**: None (users are either active or deleted)

**Business Rules**:
- Email cannot be changed after account creation (Phase II limitation)
- Deleting a user cascades to delete all their tasks
- User accounts cannot be soft-deleted (permanent deletion only)

---

### Task Entity

**Purpose**: Represents a todo item belonging to a specific user.

**Attributes**:

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier for the task |
| user_id | UUID | Foreign Key (users.id), Required, Indexed | Owner of the task |
| title | String | Required, Min 1 char, Max 200 chars | Task title/summary |
| description | Text | Optional, Max 1000 chars | Detailed task description |
| completed | Boolean | Default false, Indexed | Completion status |
| created_at | Timestamp | Auto-generated | Task creation timestamp |
| updated_at | Timestamp | Auto-updated | Last modification timestamp |

**Validation Rules**:
- Title is required and cannot be empty string
- Title must be 1-200 characters (trimmed)
- Description is optional, max 1000 characters
- Completed defaults to false on creation
- User_id must reference an existing user
- Special characters and emojis are allowed in title and description
- HTML tags should be escaped to prevent XSS

**Indexes**:
- Primary index on `id` (automatic)
- Index on `user_id` (for filtering tasks by user)
- Index on `completed` (for filtering by status)
- Composite index on `(user_id, completed)` (for common query pattern)

**State Transitions**:
```
[Created] → completed = false
    ↓
[Mark Complete] → completed = true
    ↓
[Mark Incomplete] → completed = false
    ↓
[Deleted] → removed from database
```

**Business Rules**:
- Tasks can only be viewed/modified by their owner (user_id)
- Tasks cannot be transferred to another user
- Completed tasks can be toggled back to incomplete
- Deleting a task is permanent (no soft delete in Phase II)
- Tasks are returned in creation order (newest first) by default

---

## Relationships

### User → Task (One-to-Many)

**Relationship**: One User has many Tasks

**Cardinality**: 1:N (one user can have 0 to many tasks)

**Foreign Key**: `task.user_id` references `user.id`

**Cascade Rules**:
- **ON DELETE CASCADE**: When a user is deleted, all their tasks are automatically deleted
- **ON UPDATE CASCADE**: If user.id changes (unlikely with UUID), task.user_id updates automatically

**Constraints**:
- A task must belong to exactly one user (user_id is required)
- A user can exist without any tasks (0 tasks is valid)
- Tasks cannot be orphaned (user_id must reference existing user)

**Query Patterns**:
- Get all tasks for a user: `SELECT * FROM tasks WHERE user_id = ?`
- Get completed tasks for a user: `SELECT * FROM tasks WHERE user_id = ? AND completed = true`
- Count tasks for a user: `SELECT COUNT(*) FROM tasks WHERE user_id = ?`

---

## Database Schema (SQL)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast email lookup during signin
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common query patterns
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- Trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## SQLModel Definitions (Python)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid

class User(SQLModel, table=True):
    """User entity with authentication credentials."""
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)

class Task(SQLModel, table=True):
    """Task entity belonging to a user."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: User = Relationship(back_populates="tasks")
```

---

## TypeScript Type Definitions

```typescript
// User type (frontend)
export interface User {
  id: string;  // UUID
  email: string;
  createdAt: string;  // ISO 8601 timestamp
  updatedAt: string;  // ISO 8601 timestamp
}

// Task type (frontend)
export interface Task {
  id: number;
  userId: string;  // UUID
  title: string;
  description: string | null;
  completed: boolean;
  createdAt: string;  // ISO 8601 timestamp
  updatedAt: string;  // ISO 8601 timestamp
}

// API request/response types
export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
}

export interface SignUpRequest {
  email: string;
  password: string;
}

export interface SignInRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}
```

---

## Data Validation Summary

### User Validation
- ✅ Email format validation (regex)
- ✅ Email uniqueness check (database constraint)
- ✅ Password minimum length (8 characters)
- ✅ Password complexity (letter + number recommended)
- ✅ Password hashing (bcrypt, 10+ rounds)

### Task Validation
- ✅ Title required (non-empty after trim)
- ✅ Title length (1-200 characters)
- ✅ Description optional (max 1000 characters)
- ✅ User ownership verification (user_id matches authenticated user)
- ✅ XSS prevention (escape HTML in title/description)

### Cross-Entity Validation
- ✅ Foreign key integrity (task.user_id references valid user)
- ✅ Authorization checks (user can only access their own tasks)
- ✅ Cascade delete (user deletion removes all tasks)

---

## Migration Strategy

**Initial Setup** (Phase II):
1. Create database in Neon
2. Run SQL schema creation script
3. Verify tables and indexes created
4. Test with sample data

**Future Migrations** (Phase III+):
- Use Alembic for schema changes
- Version control migration scripts
- Test migrations on staging before production
- Implement rollback procedures

---

## Performance Considerations

**Indexes**:
- Primary keys automatically indexed
- Email indexed for fast signin lookup
- user_id indexed for task filtering
- completed indexed for status filtering
- Composite index (user_id, completed) for common query

**Query Optimization**:
- Use SELECT with specific columns (avoid SELECT *)
- Implement pagination for large task lists (LIMIT/OFFSET)
- Use connection pooling to reduce connection overhead
- Cache frequently accessed data (user profile)

**Scalability**:
- UUID for user IDs allows distributed ID generation
- Integer for task IDs provides fast auto-increment
- Indexes support up to 10,000 tasks per user efficiently
- Neon handles connection pooling and scaling automatically
