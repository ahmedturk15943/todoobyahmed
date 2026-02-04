# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/001-ai-chatbot-mcp/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: TDD approach is mandatory per constitution - tests are included for all user stories

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Backend: Python 3.13+ with FastAPI, OpenAI Agents SDK, MCP SDK
- Frontend: TypeScript/Node.js 18+ with Next.js, OpenAI ChatKit

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify Phase I/II backend structure exists (backend/src/models/task.py, backend/src/services/task_service.py)
- [x] T002 [P] Add Phase III Python dependencies to backend/pyproject.toml (openai>=1.10.0, mcp-sdk>=0.1.0, asyncpg>=0.29.0)
- [x] T003 [P] Add Phase III frontend dependencies to frontend/package.json (@openai/chatkit>=1.0.0)
- [x] T004 [P] Create backend/src/mcp/ directory structure (server.py, tools/)
- [x] T005 [P] Create backend/src/agents/ directory
- [x] T006 [P] Create frontend/src/app/chat/ directory
- [x] T007 [P] Create frontend/src/services/ directory for API clients
- [x] T008 Configure environment variables in backend/.env (OPENAI_API_KEY, CHAT_HISTORY_LIMIT=50, CHAT_REQUEST_TIMEOUT=30)
- [x] T009 [P] Configure environment variables in frontend/.env.local (NEXT_PUBLIC_API_URL)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T010 Create Conversation model in backend/src/models/conversation.py (SQLModel with user_id, created_at, updated_at)
- [x] T011 Create Message model in backend/src/models/message.py (SQLModel with conversation_id, user_id, role, content, created_at)
- [x] T012 Create Alembic migration 003_add_conversations_messages.py in backend/alembic/versions/ (conversations and messages tables with foreign keys and indexes)
- [x] T013 Run database migration to create conversations and messages tables
- [x] T014 Create base MCP server structure in backend/src/mcp/server.py (tool registration framework)
- [x] T015 Create chat service skeleton in backend/src/services/chat_service.py (conversation history retrieval, message storage)
- [x] T016 Create chat API route skeleton in backend/src/api/routes/chat.py (POST /api/{user_id}/chat endpoint structure)
- [x] T017 [P] Create base chat API client in frontend/src/services/chatApi.ts (sendMessage function)
- [x] T018 Verify database connection pooling configured for asyncpg (pool_size=10, timeout=30)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks by describing them in natural language. The chatbot interprets intent and creates tasks via MCP tools.

**Independent Test**: Send "Add a task to buy groceries" and verify task is created with correct title and chatbot confirms creation.

### Tests for User Story 1 (TDD - Write First, Ensure FAIL)

- [x] T019 [P] [US1] Unit test for add_task MCP tool in backend/tests/unit/test_mcp_add_task.py (test success, empty title, validation)
- [x] T020 [P] [US1] Integration test for chat endpoint task creation in backend/tests/integration/test_chat_task_creation.py (end-to-end flow)
- [x] T021 [P] [US1] Contract test for chat API in backend/tests/contract/test_chat_api_contract.py (validate against OpenAPI spec)

### Implementation for User Story 1

- [x] T022 [US1] Implement add_task MCP tool in backend/src/mcp/tools/add_task.py (accepts user_id, title, description; returns task_id, status, title)
- [x] T023 [US1] Register add_task tool in backend/src/mcp/server.py (add to tools list with function schema)
- [x] T024 [US1] Create OpenAI agent with add_task tool in backend/src/agents/todo_agent.py (agent initialization, tool configuration, instructions)
- [x] T025 [US1] Implement chat endpoint logic in backend/src/api/routes/chat.py (fetch history, create agent, run agent, store messages, return response)
- [x] T026 [US1] Implement conversation history retrieval in backend/src/services/chat_service.py (get last 50 messages, format for agent)
- [x] T027 [US1] Implement message storage in backend/src/services/chat_service.py (store user message, store assistant response, update conversation timestamp)
- [x] T028 [US1] Create ChatInterface component in frontend/src/components/ChatInterface.tsx (OpenAI ChatKit integration, message sending, response display)
- [x] T029 [US1] Create chat page in frontend/src/app/chat/page.tsx (render ChatInterface, handle authentication)
- [x] T030 [US1] Implement sendMessage in frontend/src/services/chatApi.ts (POST to chat endpoint, handle conversation_id)
- [x] T031 [US1] Add error handling for AI service failures in backend/src/api/routes/chat.py (timeout, API errors, graceful degradation)
- [x] T032 [US1] Add input validation in backend/src/api/routes/chat.py (non-empty message, max length 5000 chars)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks via natural language

---

## Phase 4: User Story 2 - Task Status Management (Priority: P1)

**Goal**: Users can view, complete, and delete tasks through conversational commands with status filtering.

**Independent Test**: Create tasks, ask "Show me all my tasks", verify list displayed. Say "Mark task 1 as complete", verify confirmation.

### Tests for User Story 2 (TDD - Write First, Ensure FAIL)

- [ ] T033 [P] [US2] Unit test for list_tasks MCP tool in backend/tests/unit/test_mcp_list_tasks.py (test all/pending/completed filters)
- [ ] T034 [P] [US2] Unit test for complete_task MCP tool in backend/tests/unit/test_mcp_complete_task.py (test success, not found, idempotency)
- [ ] T035 [P] [US2] Unit test for delete_task MCP tool in backend/tests/unit/test_mcp_delete_task.py (test success, not found)
- [ ] T036 [P] [US2] Integration test for task management flow in backend/tests/integration/test_chat_task_management.py (list, complete, delete operations)

### Implementation for User Story 2

- [ ] T037 [P] [US2] Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py (accepts user_id, status filter; returns task array)
- [ ] T038 [P] [US2] Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py (accepts user_id, task_id; returns task_id, status, title)
- [ ] T039 [P] [US2] Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py (accepts user_id, task_id; returns task_id, status, title)
- [ ] T040 [US2] Register list_tasks, complete_task, delete_task tools in backend/src/mcp/server.py (add to tools list with schemas)
- [ ] T041 [US2] Update agent instructions in backend/src/agents/todo_agent.py (add guidance for listing, completing, deleting tasks)
- [ ] T042 [US2] Enhance ChatInterface in frontend/src/components/ChatInterface.tsx (display task lists, format task IDs, show completion status)
- [ ] T043 [US2] Add task list formatting helper in frontend/src/components/ChatInterface.tsx (render tasks as numbered list with status)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - full task CRUD via chat

---

## Phase 5: User Story 3 - Task Modification (Priority: P2)

**Goal**: Users can update existing tasks by changing title or description through natural language.

**Independent Test**: Create task, say "Change task 1 to 'Call mom tonight'", verify title updated and confirmation provided.

### Tests for User Story 3 (TDD - Write First, Ensure FAIL)

- [ ] T044 [P] [US3] Unit test for update_task MCP tool in backend/tests/unit/test_mcp_update_task.py (test title update, description update, not found, validation)
- [ ] T045 [P] [US3] Integration test for task update flow in backend/tests/integration/test_chat_task_update.py (update via natural language)

### Implementation for User Story 3

- [ ] T046 [US3] Implement update_task MCP tool in backend/src/mcp/tools/update_task.py (accepts user_id, task_id, optional title, optional description; returns task_id, status, title)
- [ ] T047 [US3] Register update_task tool in backend/src/mcp/server.py (add to tools list with schema)
- [ ] T048 [US3] Update agent instructions in backend/src/agents/todo_agent.py (add guidance for updating tasks, handling partial updates)

**Checkpoint**: All P1 and P2 core task operations now available via chat

---

## Phase 6: User Story 4 - Contextual Task Discovery (Priority: P2)

**Goal**: Users can find tasks by description rather than ID (e.g., "Delete the meeting task" without knowing task ID).

**Independent Test**: Create task "Team meeting", say "Delete the meeting task", verify chatbot finds and deletes correct task.

### Tests for User Story 4 (TDD - Write First, Ensure FAIL)

- [ ] T049 [P] [US4] Integration test for contextual task discovery in backend/tests/integration/test_chat_contextual_discovery.py (find by description, handle multiple matches, handle no matches)

### Implementation for User Story 4

- [ ] T050 [US4] Enhance agent instructions in backend/src/agents/todo_agent.py (add guidance for using list_tasks to find tasks by description before operations)
- [ ] T051 [US4] Add multi-match handling in agent instructions (list matching tasks and ask user to clarify)
- [ ] T052 [US4] Add no-match handling in agent instructions (inform user no tasks found, offer to list all tasks)

**Checkpoint**: Natural language task discovery working - users don't need to remember task IDs

---

## Phase 7: User Story 5 - Conversation Continuity (Priority: P3)

**Goal**: Users can resume previous conversations, maintaining context across sessions and server restarts.

**Independent Test**: Have conversation, close browser, reopen, verify conversation history displayed and context maintained.

### Tests for User Story 5 (TDD - Write First, Ensure FAIL)

- [ ] T053 [P] [US5] Integration test for conversation persistence in backend/tests/integration/test_conversation_continuity.py (create conversation, restart server simulation, resume conversation)
- [ ] T054 [P] [US5] Frontend test for conversation history display in frontend/tests/components/ChatInterface.test.tsx (verify history loads on mount)

### Implementation for User Story 5

- [ ] T055 [US5] Implement conversation list endpoint in backend/src/api/routes/chat.py (GET /api/{user_id}/conversations - return user's conversations)
- [ ] T056 [US5] Implement conversation history loading in frontend/src/components/ChatInterface.tsx (load messages on mount if conversation_id provided)
- [ ] T057 [US5] Create conversation list component in frontend/src/components/ConversationList.tsx (display user's conversations, click to resume)
- [ ] T058 [US5] Add conversation selection to chat page in frontend/src/app/chat/page.tsx (show conversation list, handle selection)
- [ ] T059 [US5] Implement conversation resume logic in frontend/src/services/chatApi.ts (pass conversation_id to continue existing conversation)
- [ ] T060 [US5] Add conversation context display in frontend/src/components/ChatInterface.tsx (show conversation created date, message count)

**Checkpoint**: All user stories complete - full conversational task management with persistence

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and production readiness

- [ ] T061 [P] Add rate limiting to chat endpoint in backend/src/api/routes/chat.py (prevent abuse, 10 requests per minute per user)
- [ ] T062 [P] Add structured logging in backend/src/services/chat_service.py (log AI API calls, tool invocations, errors)
- [ ] T063 [P] Add performance monitoring in backend/src/api/routes/chat.py (track response times, AI API latency)
- [ ] T064 [P] Optimize database queries in backend/src/services/chat_service.py (ensure indexes used, limit history to 50 messages)
- [ ] T065 [P] Add loading states to frontend/src/components/ChatInterface.tsx (show spinner during AI processing)
- [ ] T066 [P] Add error boundaries to frontend/src/app/chat/page.tsx (graceful error handling, retry logic)
- [ ] T067 [P] Add input sanitization in backend/src/api/routes/chat.py (prevent injection attacks, validate user input)
- [ ] T068 [P] Add OpenAI API cost tracking in backend/src/services/chat_service.py (log token usage, estimate costs)
- [ ] T069 [P] Create README.md in backend/ (setup instructions, environment variables, running migrations)
- [ ] T070 [P] Create README.md in frontend/ (setup instructions, environment variables, ChatKit configuration)
- [ ] T071 [P] Update root README.md (Phase III overview, architecture diagram, deployment instructions)
- [ ] T072 Run quickstart.md validation (follow all setup steps, verify all manual tests pass)
- [ ] T073 [P] Add API documentation in backend/src/api/routes/chat.py (docstrings for endpoints, parameter descriptions)
- [ ] T074 [P] Add component documentation in frontend/src/components/ChatInterface.tsx (props documentation, usage examples)
- [ ] T075 Security audit (verify user isolation, check for SQL injection, validate authentication on all endpoints)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent of US1 but builds on same infrastructure
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Independent of US1/US2
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Uses list_tasks from US2 but independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Independent of other stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- MCP tools before agent integration
- Backend services before API endpoints
- API endpoints before frontend components
- Core implementation before error handling and polish

### Parallel Opportunities

- **Phase 1 (Setup)**: All tasks marked [P] can run in parallel (T002, T003, T004, T005, T006, T007, T009)
- **Phase 2 (Foundational)**: T017 can run in parallel with backend tasks
- **Within User Stories**: All test tasks marked [P] can run in parallel
- **Across User Stories**: Once Foundational completes, all user stories can start in parallel (if team capacity allows)
- **Phase 8 (Polish)**: All tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (TDD - write first):
Task T019: "Unit test for add_task MCP tool in backend/tests/unit/test_mcp_add_task.py"
Task T020: "Integration test for chat endpoint task creation in backend/tests/integration/test_chat_task_creation.py"
Task T021: "Contract test for chat API in backend/tests/contract/test_chat_api_contract.py"

# After tests fail, implement in sequence:
Task T022: "Implement add_task MCP tool"
Task T023: "Register add_task tool"
Task T024: "Create OpenAI agent with add_task tool"
# ... continue with implementation tasks
```

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together (TDD - write first):
Task T033: "Unit test for list_tasks MCP tool"
Task T034: "Unit test for complete_task MCP tool"
Task T035: "Unit test for delete_task MCP tool"
Task T036: "Integration test for task management flow"

# After tests fail, implement MCP tools in parallel:
Task T037: "Implement list_tasks MCP tool"
Task T038: "Implement complete_task MCP tool"
Task T039: "Implement delete_task MCP tool"

# Then continue with integration tasks
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Natural Language Task Creation)
4. Complete Phase 4: User Story 2 (Task Status Management)
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Deploy/demo MVP with core conversational task management

**MVP Scope**: Users can create, list, complete, and delete tasks via natural language chat. This delivers immediate value and validates the AI + MCP architecture.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Task creation via chat)
3. Add User Story 2 → Test independently → Deploy/Demo (Full task CRUD via chat - MVP!)
4. Add User Story 3 → Test independently → Deploy/Demo (Task updates)
5. Add User Story 4 → Test independently → Deploy/Demo (Contextual discovery)
6. Add User Story 5 → Test independently → Deploy/Demo (Conversation continuity)
7. Add Polish → Production ready

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Task Creation)
   - Developer B: User Story 2 (Task Management)
   - Developer C: User Story 3 (Task Updates)
3. Stories complete and integrate independently
4. Developer D can work on User Story 5 (Conversation Continuity) in parallel
5. All developers converge on Polish phase

---

## Task Summary

**Total Tasks**: 75
- Phase 1 (Setup): 9 tasks
- Phase 2 (Foundational): 9 tasks
- Phase 3 (US1 - Task Creation): 14 tasks (3 tests + 11 implementation)
- Phase 4 (US2 - Task Management): 11 tasks (4 tests + 7 implementation)
- Phase 5 (US3 - Task Modification): 5 tasks (2 tests + 3 implementation)
- Phase 6 (US4 - Contextual Discovery): 4 tasks (1 test + 3 implementation)
- Phase 7 (US5 - Conversation Continuity): 8 tasks (2 tests + 6 implementation)
- Phase 8 (Polish): 15 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phases

**MVP Scope**: Phases 1-4 (42 tasks) deliver core conversational task management

**Test Coverage**: 16 test tasks (TDD approach) covering all user stories

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- TDD: Verify tests fail before implementing (Red-Green-Refactor)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MCP tools are the core abstraction - implement and test thoroughly
- Agent instructions guide AI behavior - iterate based on testing
- Stateless architecture: all state in database, no in-memory sessions
