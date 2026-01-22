# Quickstart: Phase I - In-Memory Python Console Todo App

**Purpose**: Quick setup guide to run and test the command-line todo application

## Prerequisites

### 1. Install Python 3.13+

**Check Version**:
```bash
python --version
```

Expected output: `Python 3.13.x` or higher

**Download** (if needed):
- Windows: https://www.python.org/downloads/
- macOS/Linux: Use system package manager

### 2. Install UV Package Manager

**Install UV**:
```bash
# On Linux/macOS
pip install uv

# On Windows (PowerShell as Admin)
irm https://astral.sh/uv/install.ps1 | iex
```

**Verify Installation**:
```bash
uv --version
```

Expected output: `uv 1.x.x` or higher

### 3. Clone and Navigate to Project

```bash
# Navigate to project directory
cd path/to/todo-app
```

## Project Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
uv venv
```

### 2. Activate Environment

**Linux/macOS**:
```bash
source .venv/bin/activate
```

**Windows (PowerShell)**:
```powershell
.venv\Scripts\activate
```

**Verify Activation**:
You should see `(.venv)` in your command prompt.

### 3. Install Dependencies

**Phase I has no external dependencies**, but we install pytest for future phases:

```bash
# Install pytest (for Phase II+ testing)
uv pip install --dev pytest
```

**Verify Installation**:
```bash
pip list | grep pytest
```

## Running the Application

### Start Application

```bash
# Run todo application
python -m src.cli.main help
```

This will display:
```
Usage: python -m src.cli.main <command>

Commands:
  add <title> [--description <desc>]    Add new task
  list                                   View all tasks
  update <id> [--title <title>] [--description <desc>]  Update task
  delete <id>                             Delete task by ID
  complete <id>                          Mark task complete
  help                                   Show this help message
```

## Quick Test Walkthrough

### Test 1: Add First Task

```bash
python -m src.cli.main add "Buy groceries" --description "Milk, eggs, bread"
```

Expected output:
```
✓ Task created: Buy groceries
```

### Test 2: List All Tasks

```bash
python -m src.cli.main list
```

Expected output:
```
| ID | Title          | Description       | Status     |
|----|----------------|------------------|------------|
|  1  | Buy groceries | Milk, eggs, bread | ✗          |
```

### Test 3: Update Task

```bash
python -m src.cli.main update 1 --title "Buy groceries (urgent)" --description "Milk, eggs, bread ASAP"
```

Expected output:
```
✓ Task updated: Buy groceries (urgent)
```

### Test 4: Mark Task Complete

```bash
python -m src.cli.main complete 1
```

Expected output:
```
✓ Task 1 marked as complete
```

### Test 5: Verify Complete Task

```bash
python -m src.cli.main list
```

Expected output:
```
| ID | Title          | Description       | Status     |
|----|----------------|------------------|------------|
|  1  | Buy groceries (urgent) | Milk, eggs, bread ASAP | ✓          |
```

### Test 6: Delete Task

```bash
python -m src.cli.main delete 1
```

Expected output:
```
✓ Task deleted: Buy groceries (urgent)
```

### Test 7: Empty List After Deletion

```bash
python -m src.cli.main list
```

Expected output:
```
No tasks found. Add a task to get started.
```

## Troubleshooting

### Issue: "No module named 'src'"

**Cause**: Not running from project root or wrong PYTHONPATH

**Solution**:
```bash
# Run from project root
python -m src.cli.main <command>

# OR add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python cli.main <command>
```

### Issue: "ModuleNotFoundError: No module named 'cli'"

**Cause**: Wrong import in CLI code

**Solution**: The CLI module should import correctly using absolute imports or proper package structure.

### Issue: UV not found

**Cause**: UV not installed or not in PATH

**Solution**: Re-run UV installation or add UV to PATH:
```bash
# Linux/macOS
export PATH="$HOME/.local/bin:$PATH"

# Windows (PowerShell)
$env:Path = "$env:Path;C:\Users\[YourName]\AppData\Local\Programs\uv\bin"
```

## Clean Up

To deactivate virtual environment:
```bash
# Linux/macOS
deactivate

# Windows (PowerShell)
deactivate
```

To remove virtual environment (if needed):
```bash
# Delete .venv directory
rm -rf .venv
```

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Run `/sp.implement` to generate Python code via Claude Code
3. Follow Test Walkthrough above to validate implementation

## Additional Notes

- **In-Memory Storage**: All tasks are lost when application exits (this is Phase I limitation)
- **No Persistence**: Tasks will not persist across application restarts (this is expected for Phase I)
- **Testing**: Use quick test walkthrough to validate all CRUD operations work correctly
- **Clean Code**: Implementation follows Python best practices with proper separation of concerns
