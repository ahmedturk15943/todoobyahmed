# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot-mcp
**Date**: 2026-01-29
**Purpose**: Setup instructions and testing procedures for Phase III implementation

## Overview

This guide provides step-by-step instructions for setting up and testing the AI-powered todo chatbot. The system consists of a FastAPI backend with OpenAI Agents SDK and MCP tools, plus a Next.js frontend with OpenAI ChatKit.

## Prerequisites

### Required Software
- Python 3.13+ with UV package manager
- Node.js 18+ with npm
- PostgreSQL client (for database access)
- Git

### Required Accounts & Keys
- OpenAI API account with API key
- Neon Serverless PostgreSQL database
- Better Auth configuration (from Phase II)

### Environment Setup
Ensure Phase I/II is functional:
- Task CRUD operations working
- Database schema in place
- Authentication system operational

## Backend Setup

### 1. Install Dependencies

```bash
cd backend

# Install Python dependencies with UV
uv pip install -e .

# Or using pip
pip install -r requirements.txt
```

**New Dependencies for Phase III**:
```toml
# Add to pyproject.toml [project.dependencies]
openai = "^1.10.0"           # OpenAI Agents SDK
mcp-sdk = "^0.1.0"           # Official MCP SDK
asyncpg = "^0.29.0"          # Async PostgreSQL driver
```

### 2. Environment Variables

Create or update `.env` file in backend directory:

```bash
# Existing from Phase II
DATABASE_URL=postgresql://user:password@host:5432/dbname
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=http://localhost:8000

# New for Phase III
OPENAI_API_KEY=sk-...your-openai-api-key
OPENAI_MODEL=gpt-4                    # or gpt-4-turbo
MCP_SERVER_ENABLED=true
CHAT_HISTORY_LIMIT=50                 # Max messages to load
CHAT_REQUEST_TIMEOUT=30               # Seconds
```

### 3. Database Migration

Run Alembic migration to create conversations and messages tables:

```bash
cd backend

# Generate migration (if not already created)
alembic revision --autogenerate -m "Add conversations and messages tables"

# Review the generated migration in alembic/versions/

# Apply migration
alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\dt"
# Should show: tasks, conversations, messages, users
```

### 4. Verify Backend Setup

Start the FastAPI development server:

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

Check health endpoint:
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

Check API documentation:
```bash
# Open in browser
http://localhost:8000/docs
# Should show chat endpoint: POST /api/{user_id}/chat
```

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend

# Install Node dependencies
npm install

# Or using yarn
yarn install
```

**New Dependencies for Phase III**:
```json
// Add to package.json dependencies
{
  "@openai/chatkit": "^1.0.0",
  "axios": "^1.6.0"
}
```

### 2. Environment Variables

Create or update `.env.local` file in frontend directory:

```bash
# Existing from Phase II
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000

# New for Phase III
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key  # For production only
```

**Note**: For local development, domain key is not required. For production deployment, see "Production Deployment" section below.

### 3. Verify Frontend Setup

Start the Next.js development server:

```bash
cd frontend
npm run dev
```

Open in browser:
```bash
http://localhost:3000
```

Navigate to chat interface:
```bash
http://localhost:3000/chat
```

## Testing the Chatbot

### Manual Testing Checklist

#### 1. Task Creation (P1)
- [ ] Send: "Add a task to buy groceries"
  - Expected: Task created, confirmation message
- [ ] Send: "I need to remember to pay bills"
  - Expected: Task created with title "Pay bills"
- [ ] Send: "Create a task: Call mom - remind her about dinner"
  - Expected: Task with title "Call mom" and description

#### 2. Task Listing (P1)
- [ ] Send: "Show me all my tasks"
  - Expected: List of all tasks with IDs and titles
- [ ] Send: "What's pending?"
  - Expected: Only incomplete tasks shown
- [ ] Send: "What have I completed?"
  - Expected: Only completed tasks shown

#### 3. Task Completion (P1)
- [ ] Send: "Mark task 1 as complete"
  - Expected: Task marked complete, confirmation
- [ ] Send: "I finished task 2"
  - Expected: Task marked complete

#### 4. Task Deletion (P1)
- [ ] Send: "Delete task 3"
  - Expected: Task deleted, confirmation
- [ ] Send: "Remove the groceries task"
  - Expected: AI finds task by description and deletes it

#### 5. Task Update (P2)
- [ ] Send: "Change task 1 to 'Call mom tonight'"
  - Expected: Task title updated
- [ ] Send: "Update task 2 description to include meeting notes"
  - Expected: Task description updated

#### 6. Conversation Continuity (P3)
- [ ] Close browser tab
- [ ] Reopen chat interface
- [ ] Verify conversation history is displayed
- [ ] Send new message
- [ ] Verify context is maintained

#### 7. Error Handling
- [ ] Send: "Delete task 999"
  - Expected: "Task not found" message
- [ ] Send: "Complete task 999"
  - Expected: "Task not found" message
- [ ] Send empty message
  - Expected: Error or prompt for input
- [ ] Send very long message (>5000 chars)
  - Expected: Error or truncation

### Automated Testing

#### Unit Tests

Run MCP tool tests:
```bash
cd backend
pytest tests/unit/test_mcp_tools.py -v
```

Expected output:
```
test_add_task_success PASSED
test_add_task_empty_title PASSED
test_list_tasks_all PASSED
test_list_tasks_pending PASSED
test_complete_task_success PASSED
test_complete_task_not_found PASSED
test_delete_task_success PASSED
test_update_task_success PASSED
```

#### Integration Tests

Run chat endpoint tests:
```bash
cd backend
pytest tests/integration/test_chat_endpoint.py -v
```

Expected output:
```
test_chat_new_conversation PASSED
test_chat_continue_conversation PASSED
test_chat_task_creation PASSED
test_chat_task_listing PASSED
test_chat_invalid_conversation PASSED
```

#### Contract Tests

Validate API against OpenAPI spec:
```bash
cd backend
pytest tests/contract/test_chat_api_contract.py -v
```

#### End-to-End Tests

Run full user flow tests:
```bash
cd frontend
npm run test:e2e
```

## Troubleshooting

### Backend Issues

**Problem**: "OpenAI API key not found"
```bash
# Solution: Verify environment variable
echo $OPENAI_API_KEY
# Should output: sk-...

# If empty, add to .env file
echo "OPENAI_API_KEY=sk-your-key" >> backend/.env
```

**Problem**: "Database connection failed"
```bash
# Solution: Verify database URL
psql $DATABASE_URL -c "SELECT 1"
# Should output: 1

# Check if tables exist
psql $DATABASE_URL -c "\dt"
```

**Problem**: "MCP tool not found"
```bash
# Solution: Verify tool registration
# Check backend/src/mcp/server.py
# Ensure all 5 tools are registered
```

**Problem**: "AI response timeout"
```bash
# Solution: Increase timeout in .env
CHAT_REQUEST_TIMEOUT=60  # Increase to 60 seconds
```

### Frontend Issues

**Problem**: "ChatKit component not rendering"
```bash
# Solution: Verify installation
npm list @openai/chatkit
# Should show version

# Reinstall if needed
npm install @openai/chatkit --force
```

**Problem**: "CORS error when calling API"
```bash
# Solution: Verify CORS configuration in backend
# Check backend/src/main.py
# Ensure frontend URL is in allowed origins
```

**Problem**: "Domain allowlist error (production)"
```bash
# Solution: Add domain to OpenAI allowlist
# 1. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
# 2. Add your production URL
# 3. Get domain key
# 4. Update NEXT_PUBLIC_OPENAI_DOMAIN_KEY
```

### Database Issues

**Problem**: "Conversation history not loading"
```bash
# Solution: Check messages table
psql $DATABASE_URL -c "SELECT COUNT(*) FROM messages"
# Should show message count

# Check indexes
psql $DATABASE_URL -c "\d messages"
# Should show index on (conversation_id, created_at)
```

**Problem**: "Slow query performance"
```bash
# Solution: Analyze query plan
psql $DATABASE_URL -c "EXPLAIN ANALYZE SELECT * FROM messages WHERE conversation_id = 1 ORDER BY created_at ASC LIMIT 50"

# Add missing indexes if needed
psql $DATABASE_URL -c "CREATE INDEX IF NOT EXISTS idx_conversation_messages ON messages(conversation_id, created_at)"
```

## Production Deployment

### Backend Deployment (Vercel/Railway/Render)

1. **Set environment variables** in hosting platform:
   - `DATABASE_URL` (Neon connection string)
   - `OPENAI_API_KEY`
   - `BETTER_AUTH_SECRET`
   - All other variables from `.env`

2. **Run database migration**:
   ```bash
   # SSH into deployment or run via CI/CD
   alembic upgrade head
   ```

3. **Verify deployment**:
   ```bash
   curl https://your-api.example.com/health
   ```

### Frontend Deployment (Vercel)

1. **Deploy to get production URL**:
   ```bash
   cd frontend
   vercel deploy --prod
   # Note the URL: https://your-app.vercel.app
   ```

2. **Configure OpenAI domain allowlist**:
   - Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
   - Click "Add domain"
   - Enter: `https://your-app.vercel.app` (no trailing slash)
   - Save and copy the domain key

3. **Update environment variables** in Vercel:
   - `NEXT_PUBLIC_OPENAI_DOMAIN_KEY=<your-domain-key>`
   - `NEXT_PUBLIC_API_URL=https://your-api.example.com/api`

4. **Redeploy**:
   ```bash
   vercel deploy --prod
   ```

### Post-Deployment Verification

- [ ] Health check passes
- [ ] Authentication works
- [ ] Chat interface loads
- [ ] Can create tasks via chat
- [ ] Can list tasks via chat
- [ ] Conversation history persists
- [ ] Error handling works

## Performance Monitoring

### Key Metrics to Monitor

1. **Response Time**:
   - Target: 95% of requests under 3 seconds
   - Monitor: API endpoint latency

2. **AI API Usage**:
   - Monitor: OpenAI API calls per hour
   - Set alerts for cost thresholds

3. **Database Performance**:
   - Monitor: Query execution time
   - Monitor: Connection pool usage

4. **Error Rates**:
   - Monitor: 4xx and 5xx response rates
   - Set alerts for >1% error rate

### Monitoring Tools

```bash
# Backend logs
tail -f backend/logs/app.log

# Database queries
psql $DATABASE_URL -c "SELECT * FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10"

# OpenAI API usage
# Check: https://platform.openai.com/usage
```

## Next Steps

After successful setup and testing:

1. **Run /sp.tasks** to generate implementation tasks
2. **Implement P1 user stories** first (task creation, listing, completion)
3. **Run tests** after each implementation
4. **Deploy to staging** for user acceptance testing
5. **Implement P2/P3 stories** based on feedback
6. **Deploy to production** when all acceptance criteria met

## Support

For issues or questions:
- Check troubleshooting section above
- Review error logs in backend/logs/
- Consult API documentation at /docs endpoint
- Review spec.md and plan.md for requirements
