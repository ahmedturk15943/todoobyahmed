# MCP Tools Specification

**Feature**: 001-ai-chatbot-mcp
**Date**: 2026-01-29
**Purpose**: Define MCP (Model Context Protocol) tool schemas for AI agent integration

## Overview

This document defines the 5 MCP tools that the AI agent uses to manage tasks. Each tool is a stateless function that accepts parameters and returns structured results. Tools are invoked by the OpenAI Agents SDK based on user intent interpretation.

---

## Tool 1: add_task

**Purpose**: Create a new task for the user

**Function Schema**:
```json
{
  "type": "function",
  "function": {
    "name": "add_task",
    "description": "Create a new task for the user. Use this when the user wants to add, create, or remember something.",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "The authenticated user's identifier"
        },
        "title": {
          "type": "string",
          "description": "The task title (required, 1-255 characters)"
        },
        "description": {
          "type": "string",
          "description": "Optional detailed description of the task"
        }
      },
      "required": ["user_id", "title"]
    }
  }
}
```

**Input Example**:
```json
{
  "user_id": "user_123abc",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "Unique identifier of the created task"
    },
    "status": {
      "type": "string",
      "enum": ["created"],
      "description": "Operation status"
    },
    "title": {
      "type": "string",
      "description": "The task title as stored"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

**Output Example**:
```json
{
  "task_id": 15,
  "status": "created",
  "title": "Buy groceries"
}
```

**Error Conditions**:
- Empty or whitespace-only title → ValueError
- Title exceeds 255 characters → ValueError
- Description exceeds 10,000 characters → ValueError
- Invalid user_id → ValueError

---

## Tool 2: list_tasks

**Purpose**: Retrieve tasks from the user's task list

**Function Schema**:
```json
{
  "type": "function",
  "function": {
    "name": "list_tasks",
    "description": "Retrieve tasks from the user's list. Can filter by completion status. Use this when the user wants to see, show, or list their tasks.",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "The authenticated user's identifier"
        },
        "status": {
          "type": "string",
          "enum": ["all", "pending", "completed"],
          "description": "Filter tasks by completion status. Defaults to 'all'."
        }
      },
      "required": ["user_id"]
    }
  }
}
```

**Input Example**:
```json
{
  "user_id": "user_123abc",
  "status": "pending"
}
```

**Output Schema**:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "integer",
        "description": "Task unique identifier"
      },
      "title": {
        "type": "string",
        "description": "Task title"
      },
      "description": {
        "type": "string",
        "description": "Task description (may be null)"
      },
      "completed": {
        "type": "boolean",
        "description": "Task completion status"
      },
      "created_at": {
        "type": "string",
        "format": "date-time",
        "description": "Task creation timestamp"
      },
      "updated_at": {
        "type": "string",
        "format": "date-time",
        "description": "Last update timestamp"
      }
    },
    "required": ["id", "title", "completed", "created_at", "updated_at"]
  }
}
```

**Output Example**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-29T10:00:00Z",
    "updated_at": "2026-01-29T10:00:00Z"
  },
  {
    "id": 2,
    "title": "Call mom",
    "description": null,
    "completed": false,
    "created_at": "2026-01-29T11:00:00Z",
    "updated_at": "2026-01-29T11:00:00Z"
  }
]
```

**Error Conditions**:
- Invalid status value → ValueError
- Invalid user_id → ValueError

---

## Tool 3: complete_task

**Purpose**: Mark a task as complete

**Function Schema**:
```json
{
  "type": "function",
  "function": {
    "name": "complete_task",
    "description": "Mark a task as complete. Use this when the user indicates a task is done, finished, or completed.",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "The authenticated user's identifier"
        },
        "task_id": {
          "type": "integer",
          "description": "The unique identifier of the task to complete"
        }
      },
      "required": ["user_id", "task_id"]
    }
  }
}
```

**Input Example**:
```json
{
  "user_id": "user_123abc",
  "task_id": 3
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The task identifier"
    },
    "status": {
      "type": "string",
      "enum": ["completed"],
      "description": "Operation status"
    },
    "title": {
      "type": "string",
      "description": "The task title"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

**Output Example**:
```json
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

**Error Conditions**:
- Task not found → ValueError("Task not found")
- Task does not belong to user → ValueError("Task not found")
- Task already completed → Success (idempotent operation)

---

## Tool 4: delete_task

**Purpose**: Remove a task from the user's list

**Function Schema**:
```json
{
  "type": "function",
  "function": {
    "name": "delete_task",
    "description": "Remove a task from the user's list. Use this when the user wants to delete, remove, or cancel a task.",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "The authenticated user's identifier"
        },
        "task_id": {
          "type": "integer",
          "description": "The unique identifier of the task to delete"
        }
      },
      "required": ["user_id", "task_id"]
    }
  }
}
```

**Input Example**:
```json
{
  "user_id": "user_123abc",
  "task_id": 2
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The deleted task identifier"
    },
    "status": {
      "type": "string",
      "enum": ["deleted"],
      "description": "Operation status"
    },
    "title": {
      "type": "string",
      "description": "The task title that was deleted"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

**Output Example**:
```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

**Error Conditions**:
- Task not found → ValueError("Task not found")
- Task does not belong to user → ValueError("Task not found")

---

## Tool 5: update_task

**Purpose**: Modify a task's title or description

**Function Schema**:
```json
{
  "type": "function",
  "function": {
    "name": "update_task",
    "description": "Update a task's title or description. Use this when the user wants to change, update, or rename a task.",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "The authenticated user's identifier"
        },
        "task_id": {
          "type": "integer",
          "description": "The unique identifier of the task to update"
        },
        "title": {
          "type": "string",
          "description": "New task title (optional, 1-255 characters)"
        },
        "description": {
          "type": "string",
          "description": "New task description (optional)"
        }
      },
      "required": ["user_id", "task_id"]
    }
  }
}
```

**Input Example**:
```json
{
  "user_id": "user_123abc",
  "task_id": 1,
  "title": "Buy groceries and fruits"
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The task identifier"
    },
    "status": {
      "type": "string",
      "enum": ["updated"],
      "description": "Operation status"
    },
    "title": {
      "type": "string",
      "description": "The updated task title"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

**Output Example**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

**Error Conditions**:
- Task not found → ValueError("Task not found")
- Task does not belong to user → ValueError("Task not found")
- Empty or whitespace-only title → ValueError("Title cannot be empty")
- Title exceeds 255 characters → ValueError
- Description exceeds 10,000 characters → ValueError
- Neither title nor description provided → ValueError("Must provide title or description")

---

## Agent Instructions

The AI agent should be configured with these instructions for using the MCP tools:

```
You are a helpful todo assistant. Your role is to help users manage their tasks through natural language conversation.

TOOL USAGE GUIDELINES:

1. Task Creation (add_task):
   - Use when user mentions: "add", "create", "remember", "I need to", "remind me to"
   - Extract task title from user's message
   - Include description if user provides additional details
   - Confirm creation with friendly message

2. Task Listing (list_tasks):
   - Use when user asks: "show", "list", "what are", "what's", "see my tasks"
   - Filter by status based on context:
     - "pending" for: "what's left", "what do I need to do", "incomplete"
     - "completed" for: "what have I done", "what did I finish", "completed"
     - "all" for: "show all", "everything", "all tasks"
   - Present tasks in a clear, numbered format

3. Task Completion (complete_task):
   - Use when user says: "done", "complete", "finished", "mark as complete"
   - Confirm which task was completed
   - Celebrate completion with positive message

4. Task Deletion (delete_task):
   - Use when user says: "delete", "remove", "cancel", "get rid of"
   - If user references task by description (not ID), use list_tasks first to find it
   - Confirm deletion

5. Task Update (update_task):
   - Use when user says: "change", "update", "rename", "modify"
   - Update only the fields user mentions
   - Confirm what was changed

ERROR HANDLING:
- If task not found, inform user and offer to list their tasks
- If user request is ambiguous, ask clarifying questions
- If multiple tasks match description, list them and ask which one
- Always be helpful and friendly in responses

CONVERSATION STYLE:
- Be concise but friendly
- Confirm actions taken
- Use natural language, not technical jargon
- Offer helpful suggestions when appropriate
```

---

## Testing Checklist

For each MCP tool, verify:
- [ ] Tool accepts valid inputs and returns expected output
- [ ] Tool rejects invalid inputs with clear error messages
- [ ] Tool enforces user isolation (cannot access other users' tasks)
- [ ] Tool handles edge cases (empty strings, very long inputs, special characters)
- [ ] Tool is idempotent where appropriate (complete_task)
- [ ] Tool returns consistent error format
- [ ] Tool execution time is under 1 second (excluding AI processing)
