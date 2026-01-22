# Implementation Tasks: Phase I - In-Memory Python Console Todo App

**Branch**: `001-phase1-cli-app`
**Date**: 2025-12-28
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Overview

This task breakdown implements a command-line todo application with in-memory storage supporting core CRUD operations. Tasks are organized by user story with clear phases for incremental delivery.

**Total Tasks**: 18
**Estimated Timeline**: 2-4 hours
**Test Strategy**: Manual CLI testing (Phase I MVP - no automated tests required)

---

## Phase 1: Setup (Project Initialization)

**Goal**: Initialize Python project with proper directory structure and dependency management

- [ ] T001 Create project directory structure per implementation plan in src/, tests/
- [ ] T002 Create __init__.py files in src/models, src/services, src/cli, src/lib, tests/
- [ ] T003 Initialize pyproject.toml for UV dependency management with Python 3.13+ requirement
- [ ] T004 Create README.md with project title and overview

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Create data model and service layer before implementing CLI interface

- [ ] T005 [US1] Create Task model in src/models/task.py with id, title, description, status, created_at attributes
- [ ] T006 [US1] Create TodoService class in src/services/todo_service.py with add, list, update, delete, complete, get_next_id methods
- [ ] T007 [US1] Implement in-memory storage using Python dict in TodoService with auto-incrementing ID generation
- [ ] T008 [US1] Add input validation for task operations (title non-empty, ID exists for updates)

---

## Phase 3: User Story 1 - Manage Core Todo Items (Priority: P1)

**Goal**: User can add, delete, update, view, and mark tasks complete through CLI

**Independent Test**: Can be tested by manually exercising all CRUD operations and verifying task list updates correctly with proper feedback messages

- [ ] T009 [P] [US1] Create CLI argument parser in src/cli/main.py with subcommands: add, list, update, delete, complete, help
- [ ] T010 [P] [US1] Implement 'add' command in src/cli/main.py that calls TodoService.add() with title and description arguments
- [ ] T011 [P] [US1] Implement 'list' command in src/cli/main.py that calls TodoService.list() and displays tasks in table format
- [ ] T012 [P] [US1] Implement 'update' command in src/cli/main.py that calls TodoService.update() with id, title, description arguments
- [ ] T013 [P] [US1] Implement 'delete' command in src/cli/main.py that calls TodoService.delete() with id argument
- [ ] T014 [P] [US1] Implement 'complete' command in src/cli/main.py that calls TodoService.complete() with id argument
- [ ] T015 [P] [US1] Add user feedback messages in src/cli/main.py (✓ for success, ✗ for errors) for all commands
- [ ] T016 [P] [US1] Add error handling in src/cli/main.py for invalid task ID, missing required arguments, and non-existent operations

---

## Phase 4: User Story 2 - Task List Display and Organization (Priority: P2)

**Goal**: User can view tasks in organized, readable format with clear status indicators

**Independent Test**: Can be tested by running list command and verifying table formatting with aligned columns and status indicators (✓/✗)

- [ ] T017 [P] [US2] Implement table formatting in src/cli/main.py for task list display with aligned columns (ID, Title, Description, Status)
- [ ] T018 [P] [US2] Add status indicators (✓ for complete, ✗ for incomplete) to task list output in src/cli/main.py
- [ ] T019 [P] [US2] Display "No tasks found" message when task list is empty in TodoService.list() method

---

## Phase 5: Polish & Cross-Cutting Concerns

**Goal**: Complete application with graceful exit, help documentation, and clean code practices

- [ ] T020 Implement 'help' command in src/cli/main.py that displays usage examples for all commands
- [ ] T021 Add graceful application exit handling in src/cli/main.py for keyboard interrupt (Ctrl+C) with appropriate message
- [ ] T022 Add code comments and docstrings in src/models/task.py, src/services/todo_service.py, src/cli/main.py following PEP 8 style guide
- [ ] T023 Verify all modules can be imported correctly with relative imports from src package
- [ ] T024 Create setup instructions in README.md matching quickstart.md guide

---

## Dependencies

**Prerequisite Tasks**:
Phase 1 → No prerequisites
Phase 2 → Phase 1 must complete (project structure exists)
Phase 3 → Phase 2 must complete (Task model and TodoService exist)
Phase 4 → Phase 3 must complete (CLI commands implemented)
Phase 5 → Phases 3 and 4 must complete (CLI functionality complete)

**Blocking Relationships**:
- T005 (Task model) blocks T006 (TodoService)
- T006 (TodoService) blocks T009-T016 (all CLI commands)
- T009-T016 (CLI commands) block T017-T018 (display formatting)

**Parallel Opportunities**:
Tasks marked with [P] can be executed in parallel with other tasks in same phase (no cross-phase dependencies):
- [P] T010, T012, T013, T014, T015, T016 can be executed in parallel once T009 (parser) is complete
- [P] T005 and T008 (validation) can be executed in parallel
- [P] T020 (help) can be done anytime
- T021-T024 (polish) can be done once CLI functionality works

---

## Execution Strategy

**MVP Scope (Recommended for First Run)**:
Implement Phase 1 through Phase 3 to get core CRUD working:
- Setup tasks (T001-T004)
- Foundational tasks (T005-T008)
- User Story 1 tasks (T009-T016)

This provides:
- Working CLI with add, list, update, delete, complete commands
- In-memory task storage with auto-incrementing IDs
- Basic error handling and user feedback

**Incremental Delivery**:
After MVP, implement User Story 2 (T017-T019) for better display, then polish (T020-T024).

---

## Acceptance Testing

**After Each Phase**:
- **Phase 1**: Verify directory structure created, pyproject.toml initialized with Python 3.13+
- **Phase 2**: Verify Task model validates attributes, TodoService manages dict storage correctly
- **Phase 3**: Test all 5 CRUD operations: add, list, update, delete, complete
- **Phase 4**: Verify table formatting aligned, status indicators visible, empty list message displays
- **Phase 5**: Verify help displays examples, exit works gracefully, code follows PEP 8

**Final Validation**:
Run all quickstart validation scenarios from quickstart.md:
1. Add task with title only → creates with ID, empty description
2. Add task with title and description → creates with both fields populated
3. List tasks → displays in table format
4. Update existing task → updates details, displays confirmation
5. Complete task → status changes, confirmation displayed
6. Delete task → removes task, confirmation displayed
7. Attempt invalid operations → displays helpful error messages

---

## Task Completion Criteria

Each task is complete when:
- [ ] Code is written following clean code principles
- [ ] File paths match implementation plan
- [ ] Functionality matches spec requirements
- [ ] Manual testing passes acceptance scenarios
- [ ] Code can be imported and runs without errors
