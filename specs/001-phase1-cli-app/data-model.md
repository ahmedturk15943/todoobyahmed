# Data Model: Phase I - In-Memory Python Console Todo App

**Purpose**: Define Task entity structure for in-memory todo management

## Entity: Task

**Attributes**:
- **id** (integer): Unique identifier, auto-increments starting from 1
- **title** (string): Brief task name, required, non-empty
- **description** (string): Detailed task information, optional, defaults to empty string
- **status** (enum): Completion state, values: "complete" | "incomplete"
  - Default: "incomplete"
  - Transitions: "incomplete" → "complete" (mark as complete), "complete" → "incomplete" (future feature)
- **created_at** (string): ISO 8601 timestamp (YYYY-MM-DDTHH:MM:SS) when task was created

## Validation Rules

**Title Validation** (FR-001):
- Must be non-empty string
- Trim whitespace
- Maximum length: 200 characters (practical limit for CLI display)

**ID Validation** (FR-002):
- Must exist for update/delete/complete operations (FR-006)
- Must be unique across all tasks (auto-increment ensures this)

**Status Validation** (FR-003):
- Must be valid enum value ("complete" or "incomplete")
- Default value is "incomplete" when creating new task

## Storage Pattern

In-memory storage uses Python dict:
```python
tasks = {
    1: {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "status": "incomplete",
        "created_at": "2025-12-28T14:30:00"
    },
    2: {
        "id": 2,
        "title": "Complete homework",
        "description": "Math assignment due Friday",
        "status": "complete",
        "created_at": "2025-12-28T15:00:00"
    }
}
```

**Note**: Data is lost when application exits (Phase I limitation)
