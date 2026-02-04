# Data Model: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot-mcp
**Date**: 2026-01-29
**Purpose**: Define entities, relationships, and validation rules for conversation and task management

## Overview

This document defines the data model for Phase III, which extends the existing Phase I/II task management schema with conversation and message entities. The model supports stateless conversation management with full history persistence.

## Entity Definitions

### 1. Task (Existing - Phase I/II)

**Purpose**: Represents a todo item that users can manage through the chatbot or traditional UI.

**Attributes**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `user_id` (String, Foreign Key): References users.id, identifies task owner
- `title` (String, Required): Task title, max 255 characters
- `description` (Text, Optional): Detailed task description, unlimited length
- `completed` (Boolean, Required): Task completion status, defaults to false
- `created_at` (Timestamp, Required): Task creation timestamp, auto-generated
- `updated_at` (Timestamp, Required): Last modification timestamp, auto-updated

**Validation Rules**:
- `title` must not be empty or whitespace-only
- `title` length: 1-255 characters
- `description` length: 0-10,000 characters (soft limit)
- `user_id` must reference existing user
- `completed` defaults to false on creation

**Relationships**:
- Belongs to User (many-to-one)
- Referenced by MCP tool operations

**Indexes**:
- Primary key on `id`
- Index on `(user_id, completed)` for filtering
- Index on `(user_id, created_at)` for sorting

**State Transitions**:
```
[Created] --complete_task--> [Completed]
[Completed] --update_task--> [Completed] (can update completed tasks)
[Created/Completed] --delete_task--> [Deleted]
```

---

### 2. Conversation (New - Phase III)

**Purpose**: Represents a chat session between a user and the AI assistant. Groups related messages together.

**Attributes**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `user_id` (String, Foreign Key): References users.id, identifies conversation owner
- `created_at` (Timestamp, Required): Conversation start timestamp, auto-generated
- `updated_at` (Timestamp, Required): Last message timestamp, auto-updated

**Validation Rules**:
- `user_id` must reference existing user
- `created_at` is immutable after creation
- `updated_at` is updated on every new message

**Relationships**:
- Belongs to User (many-to-one)
- Has many Messages (one-to-many)

**Indexes**:
- Primary key on `id`
- Index on `(user_id, created_at DESC)` for listing user's conversations

**Lifecycle**:
- Created when user sends first message without conversation_id
- Updated timestamp on every new message
- Persists indefinitely (no automatic expiration)
- Deleted when user is deleted (cascade)

---

### 3. Message (New - Phase III)

**Purpose**: Represents a single message in a conversation, either from the user or the AI assistant.

**Attributes**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `conversation_id` (Integer, Foreign Key): References conversations.id, groups messages
- `user_id` (String, Foreign Key): References users.id, identifies message owner
- `role` (String, Required): Message sender role, either "user" or "assistant"
- `content` (Text, Required): Message content, unlimited length
- `created_at` (Timestamp, Required): Message timestamp, auto-generated

**Validation Rules**:
- `conversation_id` must reference existing conversation
- `user_id` must reference existing user
- `role` must be exactly "user" or "assistant" (enforced by CHECK constraint)
- `content` must not be empty
- `content` length: 1-50,000 characters (soft limit)
- `created_at` is immutable after creation

**Relationships**:
- Belongs to Conversation (many-to-one)
- Belongs to User (many-to-one)

**Indexes**:
- Primary key on `id`
- Index on `(conversation_id, created_at ASC)` for chronological retrieval

**Ordering**:
- Messages within a conversation are ordered by `created_at` ascending
- History retrieval limits to last 50 messages for performance

---

### 4. User (Existing - Phase I/II)

**Purpose**: Represents an authenticated user of the system.

**Attributes**:
- `id` (String, Primary Key): Unique user identifier from Better Auth
- `email` (String, Unique): User email address
- `name` (String, Optional): User display name
- `created_at` (Timestamp, Required): Account creation timestamp
- `updated_at` (Timestamp, Required): Last profile update timestamp

**Relationships**:
- Has many Tasks (one-to-many)
- Has many Conversations (one-to-many)
- Has many Messages (one-to-many)

**Cascade Behavior**:
- Deleting user deletes all tasks, conversations, and messages (CASCADE)

---

## Entity Relationships

### ER Diagram

```
┌─────────────────┐
│      User       │
│─────────────────│
│ id (PK)         │
│ email           │
│ name            │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴────────────────────────┐
    │                             │
    │                             │
┌───▼──────────┐          ┌───────▼──────────┐
│     Task     │          │  Conversation    │
│──────────────│          │──────────────────│
│ id (PK)      │          │ id (PK)          │
│ user_id (FK) │          │ user_id (FK)     │
│ title        │          │ created_at       │
│ description  │          │ updated_at       │
│ completed    │          └────────┬─────────┘
│ created_at   │                   │
│ updated_at   │                   │ 1:N
└──────────────┘                   │
                            ┌──────▼──────────┐
                            │    Message      │
                            │─────────────────│
                            │ id (PK)         │
                            │ conversation_id │
                            │ user_id (FK)    │
                            │ role            │
                            │ content         │
                            │ created_at      │
                            └─────────────────┘
```

### Relationship Details

**User → Task** (1:N)
- One user can have many tasks
- Foreign key: `tasks.user_id` → `users.id`
- Cascade: DELETE user → DELETE tasks

**User → Conversation** (1:N)
- One user can have many conversations
- Foreign key: `conversations.user_id` → `users.id`
- Cascade: DELETE user → DELETE conversations

**Conversation → Message** (1:N)
- One conversation contains many messages
- Foreign key: `messages.conversation_id` → `conversations.id`
- Cascade: DELETE conversation → DELETE messages

**User → Message** (1:N)
- One user can have many messages
- Foreign key: `messages.user_id` → `users.id`
- Cascade: DELETE user → DELETE messages

---

## Validation Rules Summary

### Task Validation
```python
class TaskValidation:
    MIN_TITLE_LENGTH = 1
    MAX_TITLE_LENGTH = 255
    MAX_DESCRIPTION_LENGTH = 10_000

    @staticmethod
    def validate_title(title: str) -> None:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        if len(title) > TaskValidation.MAX_TITLE_LENGTH:
            raise ValueError(f"Task title exceeds {TaskValidation.MAX_TITLE_LENGTH} characters")

    @staticmethod
    def validate_description(description: Optional[str]) -> None:
        if description and len(description) > TaskValidation.MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Task description exceeds {TaskValidation.MAX_DESCRIPTION_LENGTH} characters")
```

### Conversation Validation
```python
class ConversationValidation:
    @staticmethod
    def validate_user_id(user_id: str) -> None:
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
```

### Message Validation
```python
class MessageValidation:
    VALID_ROLES = {"user", "assistant"}
    MIN_CONTENT_LENGTH = 1
    MAX_CONTENT_LENGTH = 50_000

    @staticmethod
    def validate_role(role: str) -> None:
        if role not in MessageValidation.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}. Must be 'user' or 'assistant'")

    @staticmethod
    def validate_content(content: str) -> None:
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")
        if len(content) > MessageValidation.MAX_CONTENT_LENGTH:
            raise ValueError(f"Message content exceeds {MessageValidation.MAX_CONTENT_LENGTH} characters")
```

---

## SQLModel Definitions

### Task Model (Existing)
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Conversation Model (New)
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
```

### Message Model (New)
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, Literal

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    role: Literal["user", "assistant"] = Field()
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

---

## Query Patterns

### Common Queries

**Get user's conversations (most recent first)**:
```sql
SELECT * FROM conversations
WHERE user_id = ?
ORDER BY updated_at DESC
LIMIT 20;
```

**Get conversation history (last 50 messages)**:
```sql
SELECT * FROM messages
WHERE conversation_id = ?
ORDER BY created_at ASC
LIMIT 50;
```

**Get user's pending tasks**:
```sql
SELECT * FROM tasks
WHERE user_id = ? AND completed = false
ORDER BY created_at DESC;
```

**Get user's completed tasks**:
```sql
SELECT * FROM tasks
WHERE user_id = ? AND completed = true
ORDER BY updated_at DESC;
```

**Create new conversation**:
```sql
INSERT INTO conversations (user_id, created_at, updated_at)
VALUES (?, NOW(), NOW())
RETURNING id;
```

**Add message to conversation**:
```sql
INSERT INTO messages (conversation_id, user_id, role, content, created_at)
VALUES (?, ?, ?, ?, NOW())
RETURNING id;
```

**Update conversation timestamp**:
```sql
UPDATE conversations
SET updated_at = NOW()
WHERE id = ?;
```

---

## Performance Considerations

### Indexing Strategy
- **conversations**: Index on `(user_id, created_at DESC)` for fast conversation listing
- **messages**: Index on `(conversation_id, created_at ASC)` for fast history retrieval
- **tasks**: Existing indexes on `(user_id, completed)` and `(user_id, created_at)`

### Query Optimization
- Limit conversation history to last 50 messages to control response time
- Use pagination for conversation listing (20 per page)
- Consider materialized view for conversation summary if needed

### Scaling Considerations
- Messages table will grow fastest (2 messages per chat request)
- Consider partitioning messages table by created_at if volume exceeds 10M rows
- Monitor query performance and add covering indexes as needed
- Database connection pooling essential for serverless deployment

---

## Data Integrity

### Foreign Key Constraints
- All foreign keys enforce referential integrity
- CASCADE deletes ensure orphaned records are cleaned up
- CHECK constraints enforce valid enum values (message role)

### Transaction Boundaries
- Creating conversation + first message: Single transaction
- Adding user message + assistant response: Single transaction
- Task operations via MCP tools: Individual transactions

### Concurrency Handling
- Optimistic locking not required (append-only message pattern)
- Task updates use row-level locking (SELECT FOR UPDATE if needed)
- Conversation updated_at uses database timestamp to avoid race conditions

---

## Migration Path

### From Phase I/II to Phase III
1. Run migration to create conversations and messages tables
2. Existing tasks table unchanged (backward compatible)
3. No data migration required (new tables start empty)
4. Existing task API endpoints continue to work

### Rollback Strategy
If Phase III needs to be rolled back:
1. Drop messages table
2. Drop conversations table
3. Existing task functionality unaffected
