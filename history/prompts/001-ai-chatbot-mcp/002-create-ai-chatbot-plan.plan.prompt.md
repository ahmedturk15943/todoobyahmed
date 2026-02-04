---
id: 002
title: Create AI Chatbot Implementation Plan
stage: plan
date: 2026-01-29
surface: agent
model: claude-sonnet-4-5
feature: 001-ai-chatbot-mcp
branch: 001-ai-chatbot-mcp
user: admin
command: /sp.plan
labels: ["planning", "architecture", "ai-chatbot", "mcp", "phase3"]
links:
  spec: specs/001-ai-chatbot-mcp/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-ai-chatbot-mcp/plan.md
  - specs/001-ai-chatbot-mcp/research.md
  - specs/001-ai-chatbot-mcp/data-model.md
  - specs/001-ai-chatbot-mcp/contracts/mcp-tools.md
  - specs/001-ai-chatbot-mcp/contracts/chat-api.yaml
  - specs/001-ai-chatbot-mcp/quickstart.md
  - CLAUDE.md (updated with Phase III technologies)
tests:
  - Constitution Check validation (all gates passed)
---

## Prompt

(User provided empty input - command executed with default workflow)

## Response snapshot

Created comprehensive implementation plan for AI-Powered Todo Chatbot (Phase III) with complete architecture, research, and design artifacts.

**Planning Workflow Completed**:

### Phase 0: Research & Technical Decisions (research.md)
Documented 5 key research areas with decisions, rationale, and alternatives:
1. **OpenAI Agents SDK Integration**: Stateless per-request agent instantiation pattern
2. **MCP Server Implementation**: In-process Python module with 5 stateless tools
3. **Stateless Architecture**: Database-backed conversation state, no in-memory sessions
4. **OpenAI ChatKit Integration**: Pre-built React components with request-response pattern
5. **Database Schema Design**: Two new tables (conversations, messages) with foreign keys

### Phase 1: Design Artifacts

**data-model.md**: Complete entity definitions
- Task (existing from Phase I/II)
- Conversation (new - groups messages)
- Message (new - user/assistant messages)
- User (existing)
- ER diagram, validation rules, SQLModel definitions, query patterns

**contracts/mcp-tools.md**: MCP tool specifications
- add_task: Create new tasks
- list_tasks: Retrieve tasks with filtering
- complete_task: Mark tasks complete
- delete_task: Remove tasks
- update_task: Modify task title/description
- Function schemas, input/output examples, error conditions, agent instructions

**contracts/chat-api.yaml**: OpenAPI specification
- POST /api/{user_id}/chat endpoint
- Request/response schemas
- Error handling (400, 401, 429, 500, 503)
- Authentication with Bearer tokens

**quickstart.md**: Setup and testing guide
- Backend setup (dependencies, environment, migration)
- Frontend setup (dependencies, environment)
- Manual testing checklist (all user stories)
- Automated testing (unit, integration, contract, e2e)
- Troubleshooting guide
- Production deployment instructions
- Performance monitoring

**plan.md**: Implementation plan
- Technical context (Python 3.13+, TypeScript, FastAPI, Next.js, OpenAI SDKs)
- Constitution Check (✅ PASSED - all gates satisfied)
- Project structure (backend/frontend with detailed file tree)
- Implementation notes (critical path, risk mitigation, dependencies, testing strategy)

**Agent Context Update**: Updated CLAUDE.md with Phase III technologies

### Constitution Check Results: ✅ PASS

All 7 constitutional principles validated:
- ✅ Spec-Driven Development: Following strict workflow
- ✅ Test-First: TDD approach planned
- ✅ Incremental Evolution: Builds on Phase I/II
- ⚠️ Reusable Intelligence: MCP tools provide reusability (acceptable for Phase III)
- ✅ Clean Code Architecture: Clear separation of concerns
- ⚠️ Cloud-Native Standards: Stateless architecture (containerization in Phase IV)
- ✅ AI-Native Integration: Core AI integration as specified

Partial compliance items justified and within constitutional guidelines.

### Key Architectural Decisions

1. **Stateless Architecture**: All state in database, enables horizontal scaling
2. **In-Process MCP Server**: Simplicity and performance over separate service
3. **Per-Request Agent**: Fresh agent instance per request, no persistent state
4. **History Limit**: Last 50 messages for performance
5. **Connection Pooling**: asyncpg with 10 connections for serverless
6. **Request-Response Pattern**: HTTP over WebSocket for MVP simplicity

### Project Structure

Backend: FastAPI + OpenAI Agents SDK + MCP tools + SQLModel
Frontend: Next.js + OpenAI ChatKit + React

New components:
- backend/src/mcp/ (MCP server and 5 tools)
- backend/src/agents/ (OpenAI Agents SDK integration)
- backend/src/api/routes/chat.py (Chat endpoint)
- backend/src/models/conversation.py, message.py (New entities)
- frontend/src/app/chat/ (Chat interface)
- frontend/src/components/ChatInterface.tsx (ChatKit integration)

## Outcome

- ✅ Impact: Complete architectural plan ready for task breakdown. Establishes stateless, scalable architecture for AI-powered conversational task management.
- 🧪 Tests: Constitution Check passed all gates. Testing strategy defined for unit, integration, contract, and e2e tests.
- 📁 Files: Created 6 planning artifacts (plan, research, data-model, 2 contracts, quickstart) + updated agent context
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks organized by user story priority
- 🧠 Reflection: Planning successfully balances AI integration complexity with Phase III scope. Stateless architecture prepares for Phase IV cloud deployment. MCP tools provide clean abstraction between AI agent and task operations. All technical unknowns resolved through research phase.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed without issues
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 7 principles validated)
- Prompt variant (if applicable): Standard /sp.plan workflow
- Next experiment (smallest change to try): Execute /sp.tasks to validate that plan provides sufficient detail for task generation

## Architectural Decisions Detected

📋 **Architectural decision detected**: Stateless architecture with database-backed conversation state vs. in-memory session management

**Decision**: Use fully stateless backend where each request fetches conversation history from database, processes with fresh agent instance, and stores results back to database.

**Rationale**:
- Enables horizontal scaling (any server handles any request)
- Resilience (server restarts don't lose state)
- Serverless-compatible
- Simpler than distributed cache/session management

**Alternatives Considered**:
- Redis for session state: Rejected to reduce dependencies
- In-memory LRU cache: Rejected to maintain pure stateless architecture
- WebSocket connections: Deferred to future enhancement

**Impact**: Long-term architectural foundation for cloud deployment in Phase IV

Document reasoning and tradeoffs? Run `/sp.adr stateless-conversation-architecture`
