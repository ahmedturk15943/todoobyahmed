# Claude Code Agent Context

**Project**: Evolution of Todo - Hackathon II
**Feature**: Phase I - In-Memory Python Console App
**Updated**: 2025-12-28

## Active Technologies

- **Python**: 3.13+
- **Package Manager**: UV
- **CLI Framework**: argparse or click
- **Architecture**: Console CLI application
- **Storage**: In-memory (dict/list)
- **Testing**: pytest (for future phases)

## Code Patterns

### Python Best Practices

**Project Structure**:
```
src/
├── models/
│   └── task.py              # Task entity definition
├── services/
│   └── todo_service.py      # Business logic for task management
├── cli/
│   ├── __init__.py
│   └── main.py             # CLI entry point and argument parsing
└── lib/
    └── __init__.py
```

**Module Design**:
- **Single Responsibility**: Each module has one clear purpose
- **Dependency Inversion**: High-level modules depend on abstractions
- **Clear Boundaries**: CLI handles I/O, Services handle business logic, Models define data structures
- **DRY Principle**: Don't Repeat Yourself - prefer explicit imports over complex inheritance

**CLI Patterns**:
- Use `argparse` for simple CLIs (already in stdlib)
- Subcommands pattern: `todo-app <command> <args>`
- Clear help messages with usage examples
- Consistent exit codes: 0 for success, 1 for errors, 2 for usage
- User-friendly error messages with suggestions

**Error Handling**:
- Validate user input immediately
- Display clear error messages in red (if terminal supports)
- Suggest correct usage when invalid input provided
- Graceful exit on keyboard interrupt (Ctrl+C)
- No exceptions escape to user without context

**Output Formatting**:
- Success: `✓ Task created: [title]`
- Error: `✗ Error: [message]`
- Lists: Aligned columns, consistent spacing
- Use colors if terminal supports ANSI codes

**In-Memory Storage Pattern**:
```python
# Simple dict-based storage
tasks = {
    1: {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "status": "incomplete",
        "created_at": "2025-12-28T14:30:00"
    }
}

# Auto-incrementing ID
next_id = max(tasks.keys()) + 1 if tasks else 1
```

**Task Management Operations**:
- Add: Create task with auto-incrementing ID
- List: Display all tasks in table format
- Update: Modify title/description by ID
- Delete: Remove task by ID
- Complete: Change status from "incomplete" to "complete"
- Validation: Check task ID exists before operations

## Architecture Decisions

### Why This Architecture?

**Separation of Concerns**:
- **CLI Layer** (`cli/`): Handles command parsing, user interaction, output formatting
- **Service Layer** (`services/`): Contains business logic, task operations
- **Model Layer** (`models/`): Defines data structures, validation rules

**Rationale**:
- Clear boundaries between layers make code easier to test and maintain
- CLI can focus on user experience, not business rules
- Services can be unit tested without CLI dependencies
- Models define contract for data, ensuring consistency

### Tradeoffs Considered

**Option 1: Monolithic CLI Script**
- Pro: Simple, single file, easy to run
- Con: Hard to test business logic independently, unclear responsibilities

**Option 2: Layered Architecture (CHOSEN)**
- Pro: Each layer has single responsibility, easier to test, clearer code organization
- Pro: Services can be reused in future phases (web app)
- Pro: Follows Clean Code Architecture principles from constitution
- Con: More files, more complex structure initially
- Con: Requires careful coordination between layers

### Future-Proofing

This architecture supports:
- **Phase II (Web App)**: Service layer can become REST API, CLI becomes optional
- **Phase III (AI Chatbot)**: Service layer exposes functions for AI agents
- **Phase IV (Kubernetes)**: Same codebase containerized and scaled

## Anti-Patterns (Things to Avoid)

**❌ Don't**:
- Mix business logic with CLI code
- Use global variables for state
- Skip input validation
- Return cryptic error messages
- Store tasks in file (not spec-compliant for Phase I)

**✅ Do**:
- Validate all user input
- Use dependency injection for services in CLI
- Write clear docstrings for functions
- Follow PEP 8 style guide
- Add type hints for better IDE support
- Provide helpful error messages with suggestions

## Testing Strategy

**Phase I**: No automated tests required (MVP focus)
- Manual testing through CLI usage
- Quickstart guide includes test scenarios

**Future Phases**:
- `pytest` for unit tests
- Integration tests for service layer
- Contract tests for API (Phase II+)

## Common Issues and Solutions

**Issue**: Task ID collision
**Solution**: Auto-increment from existing tasks, ensure uniqueness

**Issue**: Empty task title
**Solution**: Validate immediately, clear error message with example

**Issue**: Invalid task ID (non-existent)
**Solution**: Check existence before operation, display helpful error

**Issue**: Task state corruption
**Solution**: Use enum for status, validate transitions in service layer
