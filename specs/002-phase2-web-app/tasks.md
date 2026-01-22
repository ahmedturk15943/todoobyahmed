# Tasks: Full-Stack Multi-User Todo Web Application

**Input**: Design documents from `/specs/002-phase2-web-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included per constitution Principle II (Test-First is mandatory)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo**: `backend/src/`, `frontend/src/`
- **Backend**: Python FastAPI with SQLModel
- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create monorepo directory structure (backend/, frontend/, specs/, history/)
- [ ] T002 Initialize backend Python project with UV in backend/pyproject.toml
- [ ] T003 [P] Initialize frontend Next.js project with TypeScript in frontend/
- [ ] T004 [P] Configure backend linting (ruff) and formatting (black) in backend/pyproject.toml
- [ ] T005 [P] Configure frontend linting (ESLint) and formatting (Prettier) in frontend/.eslintrc.json
- [ ] T006 [P] Create backend .env.example with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS
- [ ] T007 [P] Create frontend .env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
- [ ] T008 [P] Configure Tailwind CSS in frontend/tailwind.config.js
- [ ] T009 [P] Create backend .gitignore for Python (.venv, __pycache__, .env)
- [ ] T010 [P] Create frontend .gitignore for Node.js (node_modules, .next, .env.local)
- [ ] T011 Create root README.md with project overview and setup instructions
- [ ] T012 [P] Create backend/README.md with backend-specific setup
- [ ] T013 [P] Create frontend/README.md with frontend-specific setup

**Checkpoint**: Project structure initialized, ready for foundational development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Setup

- [ ] T014 Create Neon PostgreSQL database and obtain connection string
- [ ] T015 Create database schema SQL script in backend/scripts/init_db.sql (users and tasks tables)
- [ ] T016 Run database initialization script to create tables and indexes
- [ ] T017 Create database connection module in backend/src/db/connection.py with async engine
- [ ] T018 Create database session dependency in backend/src/api/dependencies.py

### Backend Core Infrastructure

- [ ] T019 [P] Install FastAPI dependencies (fastapi, uvicorn, sqlmodel, asyncpg, python-jose, passlib, bcrypt)
- [ ] T020 [P] Create configuration module in backend/src/config.py (load env vars, validate settings)
- [ ] T021 [P] Create FastAPI app instance in backend/src/main.py with CORS middleware
- [ ] T022 [P] Create error handling middleware in backend/src/api/middleware/error_handler.py
- [ ] T023 Create JWT authentication middleware in backend/src/api/middleware/jwt_auth.py
- [ ] T024 [P] Create base response models in backend/src/api/models/responses.py (Error, Success)
- [ ] T025 [P] Setup logging configuration in backend/src/config.py

### Frontend Core Infrastructure

- [ ] T026 [P] Install frontend dependencies (better-auth, axios, tailwindcss, react-hook-form)
- [ ] T027 [P] Create API client module in frontend/src/lib/api.ts with JWT token handling
- [ ] T028 [P] Configure Better Auth in frontend/src/lib/auth.ts with JWT plugin
- [ ] T029 [P] Create TypeScript types in frontend/src/types/user.ts and frontend/src/types/task.ts
- [ ] T030 [P] Create root layout in frontend/src/app/layout.tsx with global styles
- [ ] T031 [P] Create reusable UI components (Button, Input, Card, Modal) in frontend/src/components/ui/
- [ ] T032 [P] Create global styles in frontend/src/styles/globals.css with Tailwind directives

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, sign in, and sign out securely with JWT authentication

**Independent Test**: Visit application, create account with email/password, sign out, sign back in

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T033 [P] [US1] Contract test for POST /api/auth/signup in backend/tests/contract/test_auth_signup.py
- [ ] T034 [P] [US1] Contract test for POST /api/auth/signin in backend/tests/contract/test_auth_signin.py
- [ ] T035 [P] [US1] Integration test for signup flow in backend/tests/integration/test_auth_flow.py
- [ ] T036 [P] [US1] Integration test for signin flow in backend/tests/integration/test_auth_flow.py
- [ ] T037 [P] [US1] Unit test for password hashing in backend/tests/unit/test_auth_service.py
- [ ] T038 [P] [US1] Frontend component test for SignUpForm in frontend/tests/components/SignUpForm.test.tsx
- [ ] T039 [P] [US1] Frontend component test for SignInForm in frontend/tests/components/SignInForm.test.tsx

### Backend Implementation for User Story 1

- [ ] T040 [P] [US1] Create User model in backend/src/models/user.py with SQLModel (id, email, password_hash, timestamps)
- [ ] T041 [US1] Create AuthService in backend/src/services/auth_service.py (signup, signin, hash_password, verify_password, create_jwt)
- [ ] T042 [US1] Create auth request/response models in backend/src/api/models/auth.py (SignUpRequest, SignInRequest, AuthResponse)
- [ ] T043 [US1] Implement POST /api/auth/signup endpoint in backend/src/api/routes/auth.py
- [ ] T044 [US1] Implement POST /api/auth/signin endpoint in backend/src/api/routes/auth.py
- [ ] T045 [US1] Implement POST /api/auth/signout endpoint in backend/src/api/routes/auth.py (optional, token invalidation)
- [ ] T046 [US1] Add email validation and password strength checks in backend/src/services/auth_service.py
- [ ] T047 [US1] Add error handling for duplicate email, invalid credentials in backend/src/api/routes/auth.py

### Frontend Implementation for User Story 1

- [ ] T048 [P] [US1] Create SignUpForm component in frontend/src/components/auth/SignUpForm.tsx
- [ ] T049 [P] [US1] Create SignInForm component in frontend/src/components/auth/SignInForm.tsx
- [ ] T050 [US1] Create signup page in frontend/src/app/(auth)/signup/page.tsx
- [ ] T051 [US1] Create signin page in frontend/src/app/(auth)/signin/page.tsx
- [ ] T052 [US1] Implement auth API calls in frontend/src/lib/api.ts (signup, signin, signout)
- [ ] T053 [US1] Add form validation with react-hook-form in SignUpForm and SignInForm
- [ ] T054 [US1] Add error message display for auth failures in auth forms
- [ ] T055 [US1] Implement automatic redirect after successful signup/signin to /tasks

**Checkpoint**: User Story 1 complete - users can create accounts, sign in, and sign out

---

## Phase 4: User Story 2 - View and Manage Personal Todo List (Priority: P1)

**Goal**: Display all tasks for authenticated user in a clean web interface with data isolation

**Independent Test**: Sign in and view task list page - tasks display if they exist, empty state if none

### Tests for User Story 2

- [ ] T056 [P] [US2] Contract test for GET /api/users/{user_id}/tasks in backend/tests/contract/test_tasks_list.py
- [ ] T057 [P] [US2] Integration test for task list with data isolation in backend/tests/integration/test_task_isolation.py
- [ ] T058 [P] [US2] Unit test for TaskService.get_all_tasks in backend/tests/unit/test_task_service.py
- [ ] T059 [P] [US2] Frontend component test for TaskList in frontend/tests/components/TaskList.test.tsx
- [ ] T060 [P] [US2] Frontend component test for TaskItem in frontend/tests/components/TaskItem.test.tsx

### Backend Implementation for User Story 2

- [ ] T061 [P] [US2] Create Task model in backend/src/models/task.py with SQLModel (id, user_id, title, description, completed, timestamps)
- [ ] T062 [US2] Create TaskService in backend/src/services/task_service.py with get_all_tasks method
- [ ] T063 [US2] Create task response models in backend/src/api/models/tasks.py (TaskResponse, TaskListResponse)
- [ ] T064 [US2] Implement GET /api/users/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py
- [ ] T065 [US2] Add user_id validation (must match authenticated user) in backend/src/api/routes/tasks.py
- [ ] T066 [US2] Add authorization check middleware for task endpoints in backend/src/api/middleware/jwt_auth.py

### Frontend Implementation for User Story 2

- [ ] T067 [P] [US2] Create TaskList component in frontend/src/components/tasks/TaskList.tsx
- [ ] T068 [P] [US2] Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [ ] T069 [US2] Create tasks page in frontend/src/app/(dashboard)/tasks/page.tsx
- [ ] T070 [US2] Implement task list API call in frontend/src/lib/api.ts (getTasks)
- [ ] T071 [US2] Add empty state component for no tasks in frontend/src/components/tasks/EmptyState.tsx
- [ ] T072 [US2] Add loading state while fetching tasks in tasks page
- [ ] T073 [US2] Add authentication guard to redirect unauthenticated users to signin
- [ ] T074 [US2] Display task title, description, status, and creation date in TaskItem

**Checkpoint**: User Story 2 complete - users can view their task list with proper data isolation

---

## Phase 5: User Story 3 - Create New Tasks (Priority: P1)

**Goal**: Enable users to create new tasks with title and optional description

**Independent Test**: Sign in, click "Add Task", fill in title and description, submit, verify task appears

### Tests for User Story 3

- [ ] T075 [P] [US3] Contract test for POST /api/users/{user_id}/tasks in backend/tests/contract/test_tasks_create.py
- [ ] T076 [P] [US3] Integration test for task creation with validation in backend/tests/integration/test_task_creation.py
- [ ] T077 [P] [US3] Unit test for TaskService.create_task in backend/tests/unit/test_task_service.py
- [ ] T078 [P] [US3] Frontend component test for TaskForm in frontend/tests/components/TaskForm.test.tsx

### Backend Implementation for User Story 3

- [ ] T079 [US3] Add create_task method to TaskService in backend/src/services/task_service.py
- [ ] T080 [US3] Create task request models in backend/src/api/models/tasks.py (CreateTaskRequest)
- [ ] T081 [US3] Implement POST /api/users/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py
- [ ] T082 [US3] Add title validation (required, 1-200 chars) in backend/src/api/models/tasks.py
- [ ] T083 [US3] Add description validation (optional, max 1000 chars) in backend/src/api/models/tasks.py
- [ ] T084 [US3] Add XSS prevention (escape HTML) in backend/src/services/task_service.py

### Frontend Implementation for User Story 3

- [ ] T085 [P] [US3] Create TaskForm component in frontend/src/components/tasks/TaskForm.tsx
- [ ] T086 [US3] Add "Add Task" button to tasks page in frontend/src/app/(dashboard)/tasks/page.tsx
- [ ] T087 [US3] Implement task creation API call in frontend/src/lib/api.ts (createTask)
- [ ] T088 [US3] Add form validation for title (required, max 200 chars) in TaskForm
- [ ] T089 [US3] Add form validation for description (optional, max 1000 chars) in TaskForm
- [ ] T090 [US3] Show success message after task creation
- [ ] T091 [US3] Refresh task list after successful creation
- [ ] T092 [US3] Add modal or inline form for task creation

**Checkpoint**: User Story 3 complete - users can create new tasks with validation

---

## Phase 6: User Story 4 - Update and Delete Tasks (Priority: P2)

**Goal**: Enable users to edit task details and permanently delete tasks

**Independent Test**: Sign in, edit a task's title/description, save, verify changes persist; delete a task, verify it's removed

### Tests for User Story 4

- [ ] T093 [P] [US4] Contract test for PUT /api/users/{user_id}/tasks/{task_id} in backend/tests/contract/test_tasks_update.py
- [ ] T094 [P] [US4] Contract test for DELETE /api/users/{user_id}/tasks/{task_id} in backend/tests/contract/test_tasks_delete.py
- [ ] T095 [P] [US4] Integration test for task update with authorization in backend/tests/integration/test_task_update.py
- [ ] T096 [P] [US4] Integration test for task deletion with authorization in backend/tests/integration/test_task_delete.py
- [ ] T097 [P] [US4] Unit test for TaskService.update_task in backend/tests/unit/test_task_service.py
- [ ] T098 [P] [US4] Unit test for TaskService.delete_task in backend/tests/unit/test_task_service.py

### Backend Implementation for User Story 4

- [ ] T099 [P] [US4] Add update_task method to TaskService in backend/src/services/task_service.py
- [ ] T100 [P] [US4] Add delete_task method to TaskService in backend/src/services/task_service.py
- [ ] T101 [US4] Create update task request model in backend/src/api/models/tasks.py (UpdateTaskRequest)
- [ ] T102 [US4] Implement PUT /api/users/{user_id}/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [ ] T103 [US4] Implement DELETE /api/users/{user_id}/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [ ] T104 [US4] Add authorization check (task belongs to authenticated user) in update/delete endpoints
- [ ] T105 [US4] Add 404 error handling for non-existent tasks in update/delete endpoints

### Frontend Implementation for User Story 4

- [ ] T106 [P] [US4] Add edit button to TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [ ] T107 [P] [US4] Add delete button to TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [ ] T108 [US4] Implement task update API call in frontend/src/lib/api.ts (updateTask)
- [ ] T109 [US4] Implement task deletion API call in frontend/src/lib/api.ts (deleteTask)
- [ ] T110 [US4] Add edit mode to TaskForm component (pre-fill with existing values)
- [ ] T111 [US4] Add confirmation dialog for task deletion
- [ ] T112 [US4] Refresh task list after successful update or deletion
- [ ] T113 [US4] Add cancel button to discard changes in edit mode

**Checkpoint**: User Story 4 complete - users can update and delete tasks with proper authorization

---

## Phase 7: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Enable users to toggle task completion status with visual feedback

**Independent Test**: Sign in, click checkbox next to task, verify status changes and persists on refresh

### Tests for User Story 5

- [ ] T114 [P] [US5] Contract test for PATCH /api/users/{user_id}/tasks/{task_id}/complete in backend/tests/contract/test_tasks_complete.py
- [ ] T115 [P] [US5] Integration test for completion toggle in backend/tests/integration/test_task_completion.py
- [ ] T116 [P] [US5] Unit test for TaskService.toggle_complete in backend/tests/unit/test_task_service.py

### Backend Implementation for User Story 5

- [ ] T117 [US5] Add toggle_complete method to TaskService in backend/src/services/task_service.py
- [ ] T118 [US5] Implement PATCH /api/users/{user_id}/tasks/{task_id}/complete endpoint in backend/src/api/routes/tasks.py
- [ ] T119 [US5] Add authorization check (task belongs to authenticated user) in complete endpoint
- [ ] T120 [US5] Return updated task with new completion status in response

### Frontend Implementation for User Story 5

- [ ] T121 [US5] Add checkbox to TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [ ] T122 [US5] Implement task completion toggle API call in frontend/src/lib/api.ts (toggleComplete)
- [ ] T123 [US5] Add visual indicator for completed tasks (strikethrough, checkmark, color) in TaskItem
- [ ] T124 [US5] Update task list state after completion toggle (optimistic update)
- [ ] T125 [US5] Add hover effect on checkbox for better UX

**Checkpoint**: User Story 5 complete - users can toggle task completion with visual feedback

---

## Phase 8: User Story 6 - Responsive Web Interface (Priority: P3)

**Goal**: Ensure application adapts to different screen sizes (desktop, tablet, mobile)

**Independent Test**: Access application on different screen sizes, verify layout adjusts appropriately

### Tests for User Story 6

- [ ] T126 [P] [US6] Visual regression test for desktop layout (1920px) using Playwright
- [ ] T127 [P] [US6] Visual regression test for tablet layout (768px) using Playwright
- [ ] T128 [P] [US6] Visual regression test for mobile layout (375px) using Playwright

### Frontend Implementation for User Story 6

- [ ] T129 [P] [US6] Add responsive breakpoints to Tailwind config in frontend/tailwind.config.js
- [ ] T130 [P] [US6] Make TaskList component responsive (grid on desktop, stack on mobile)
- [ ] T131 [P] [US6] Make TaskItem component responsive (adjust padding, font sizes)
- [ ] T132 [P] [US6] Make TaskForm component responsive (full width on mobile)
- [ ] T133 [P] [US6] Make auth forms responsive (center on desktop, full width on mobile)
- [ ] T134 [P] [US6] Add mobile navigation menu (hamburger icon) if needed
- [ ] T135 [P] [US6] Test all user flows on mobile viewport (320px-768px)
- [ ] T136 [P] [US6] Test all user flows on desktop viewport (1024px-1920px)

**Checkpoint**: User Story 6 complete - application is fully responsive across all screen sizes

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T137 [P] Add API documentation with FastAPI Swagger UI at /docs
- [ ] T138 [P] Add request/response logging in backend middleware
- [ ] T139 [P] Add error boundary component in frontend for graceful error handling
- [ ] T140 [P] Add loading spinners for all async operations in frontend
- [ ] T141 [P] Optimize database queries with proper indexes (already in schema)
- [ ] T142 [P] Add rate limiting to auth endpoints (prevent brute force)
- [ ] T143 [P] Add HTTPS redirect in production environment
- [ ] T144 [P] Add security headers (CORS, CSP, X-Frame-Options) in backend
- [ ] T145 [P] Add accessibility improvements (ARIA labels, keyboard navigation)
- [ ] T146 [P] Add meta tags for SEO in frontend layout
- [ ] T147 Run all quickstart.md validation scenarios
- [ ] T148 Create deployment guide in specs/002-phase2-web-app/deployment.md
- [ ] T149 Update root README.md with Phase II information
- [ ] T150 Create ADRs for significant architectural decisions (monorepo, JWT auth, Neon)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (Auth) must complete before US2-US6 (need authentication to access tasks)
  - US2 (View) should complete before US3-US5 (need to see tasks before modifying)
  - US3 (Create) can proceed after US2
  - US4 (Update/Delete) can proceed after US2
  - US5 (Complete) can proceed after US2
  - US6 (Responsive) can proceed in parallel with US2-US5
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on US1 (need authentication to view tasks)
- **User Story 3 (P1)**: Depends on US1 and US2 (need auth and view capability)
- **User Story 4 (P2)**: Depends on US1 and US2 (need auth and view capability)
- **User Story 5 (P2)**: Depends on US1 and US2 (need auth and view capability)
- **User Story 6 (P3)**: Can proceed in parallel with US2-US5 (independent styling work)

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Backend models before services
- Backend services before API endpoints
- Backend API before frontend API calls
- Frontend components before pages
- Core implementation before integration

### Parallel Opportunities

- **Setup (Phase 1)**: Tasks T003-T013 can run in parallel (different files)
- **Foundational (Phase 2)**: Tasks T019-T032 can run in parallel (different files)
- **Within Each User Story**: All test tasks marked [P] can run in parallel
- **Within Each User Story**: All model tasks marked [P] can run in parallel
- **User Stories**: US3, US4, US5 can be worked on in parallel after US2 completes
- **User Story 6**: Can proceed in parallel with US2-US5 (independent styling work)

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Launch all tests for User Story 1 together:
Task T033: "Contract test for POST /api/auth/signup"
Task T034: "Contract test for POST /api/auth/signin"
Task T035: "Integration test for signup flow"
Task T036: "Integration test for signin flow"
Task T037: "Unit test for password hashing"
Task T038: "Frontend component test for SignUpForm"
Task T039: "Frontend component test for SignInForm"

# Launch backend models together:
Task T040: "Create User model in backend/src/models/user.py"

# Launch frontend components together:
Task T048: "Create SignUpForm component"
Task T049: "Create SignInForm component"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (View Tasks)
5. Complete Phase 5: User Story 3 (Create Tasks)
6. **STOP and VALIDATE**: Test all three stories independently
7. Deploy/demo MVP

**MVP Delivers**: Users can sign up, sign in, view their tasks, and create new tasks

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Auth working)
3. Add User Story 2 → Test independently → Deploy/Demo (Can view tasks)
4. Add User Story 3 → Test independently → Deploy/Demo (MVP! Can create tasks)
5. Add User Story 4 → Test independently → Deploy/Demo (Can edit/delete)
6. Add User Story 5 → Test independently → Deploy/Demo (Can mark complete)
7. Add User Story 6 → Test independently → Deploy/Demo (Responsive design)
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication) - MUST complete first
3. Once US1 is done:
   - Developer A: User Story 2 (View Tasks) - MUST complete before US3-US5
4. Once US2 is done:
   - Developer A: User Story 3 (Create Tasks)
   - Developer B: User Story 4 (Update/Delete Tasks)
   - Developer C: User Story 5 (Toggle Complete)
   - Developer D: User Story 6 (Responsive Design) - can start earlier
5. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 150 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 13 tasks
- Phase 2 (Foundational): 19 tasks
- Phase 3 (US1 - Authentication): 23 tasks (7 tests + 16 implementation)
- Phase 4 (US2 - View Tasks): 19 tasks (5 tests + 14 implementation)
- Phase 5 (US3 - Create Tasks): 18 tasks (4 tests + 14 implementation)
- Phase 6 (US4 - Update/Delete): 21 tasks (6 tests + 15 implementation)
- Phase 7 (US5 - Toggle Complete): 12 tasks (3 tests + 9 implementation)
- Phase 8 (US6 - Responsive): 11 tasks (3 tests + 8 implementation)
- Phase 9 (Polish): 14 tasks

**Parallel Opportunities**: 67 tasks marked [P] can run in parallel within their phase

**MVP Scope** (Phases 1-5): 92 tasks
- Delivers: Authentication, view tasks, create tasks
- Estimated effort: 60-70% of total work
- Provides core value proposition

**Test Coverage**: 28 test tasks across all user stories (TDD approach)

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (Red-Green-Refactor)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution Principle II (Test-First) is enforced with test tasks before implementation
- Monorepo structure enables parallel frontend/backend development
- JWT authentication enables stateless, scalable auth
- Data isolation enforced at API layer (user_id validation)
