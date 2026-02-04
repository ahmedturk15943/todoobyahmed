# Research & Technical Decisions: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot-mcp
**Date**: 2026-01-29
**Purpose**: Document technical research findings and architectural decisions for Phase III implementation

## Overview

This document captures research findings for integrating OpenAI Agents SDK with MCP (Model Context Protocol) tools to create a conversational task management interface. Key focus areas include stateless architecture patterns, AI agent integration, and database schema design for conversation persistence.

## 1. OpenAI Agents SDK Integration

### Decision
Use OpenAI Agents SDK with function calling pattern where the agent is configured with MCP tools as available functions. The agent will be instantiated per request (stateless) with conversation history loaded from database.

### Rationale
- **Stateless Design**: Creating agent per request aligns with serverless architecture and horizontal scaling requirements
- **Tool Integration**: OpenAI Agents SDK natively supports function calling, which maps cleanly to MCP tool invocations
- **Conversation Context**: Loading history from database ensures context is maintained across server restarts
- **Error Recovery**: Stateless design means failed requests don't corrupt in-memory state

### Implementation Pattern
```python
# Per-request agent instantiation
async def handle_chat_request(user_id: str, message: str, conversation_id: Optional[int]):
    # 1. Fetch conversation history from database
    history = await get_conversation_history(conversation_id)

    # 2. Create agent with MCP tools
    agent = Agent(
        model="gpt-4",
        tools=[add_task, list_tasks, complete_task, delete_task, update_task],
        instructions="You are a helpful todo assistant..."
    )

    # 3. Build message array (history + new message)
    messages = history + [{"role": "user", "content": message}]

    # 4. Run agent
    response = await agent.run(messages)

    # 5. Store messages in database
    await store_messages(conversation_id, messages, response)

    return response
```

### Alternatives Considered
- **Persistent Agent Instances**: Rejected due to memory overhead and scaling limitations
- **Agent Pool Pattern**: Rejected due to complexity and state management challenges
- **Streaming Responses**: Deferred to future enhancement; request-response is simpler for MVP

### Error Handling Strategy
- Retry transient AI API failures (3 attempts with exponential backoff)
- Graceful degradation when AI service unavailable (return helpful error message)
- Transaction rollback if database write fails after AI response
- Timeout protection (30 second max per request)

## 2. MCP Server Implementation

### Decision
Implement MCP server as a Python module within the FastAPI backend, not as a separate service. Each MCP tool is a Python function that accepts parameters and returns structured results. Tools are stateless and access database directly.

### Rationale
- **Simplicity**: In-process MCP server avoids network overhead and deployment complexity
- **Performance**: Direct database access from tools is faster than RPC to separate service
- **Development Velocity**: Single codebase easier to develop and test
- **Stateless Tools**: Each tool invocation is independent, fetching required data from database

### MCP Tool Structure
```python
# Example: add_task tool
async def add_task(user_id: str, title: str, description: Optional[str] = None) -> dict:
    """
    MCP Tool: Create a new task

    Args:
        user_id: User identifier
        title: Task title (required)
        description: Optional task description

    Returns:
        {"task_id": int, "status": "created", "title": str}
    """
    # Validate inputs
    if not title or len(title.strip()) == 0:
        raise ValueError("Task title cannot be empty")

    # Create task in database
    task = await task_service.create_task(
        user_id=user_id,
        title=title.strip(),
        description=description.strip() if description else None
    )

    # Return structured result
    return {
        "task_id": task.id,
        "status": "created",
        "title": task.title
    }
```

### Tool Registration
Tools are registered with the OpenAI Agents SDK using function schemas:
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        }
    },
    # ... other tools
]
```

### Alternatives Considered
- **Separate MCP Service**: Rejected due to added complexity and latency
- **gRPC for Tool Communication**: Rejected as in-process calls are sufficient
- **Tool State Caching**: Rejected to maintain stateless architecture

### Best Practices Applied
- Input validation in every tool
- Structured error responses
- Consistent return format across all tools
- Database transactions for data integrity
- User isolation enforced at tool level

## 3. Stateless Architecture Patterns

### Decision
Implement fully stateless backend where each request:
1. Fetches conversation history from database
2. Processes request with fresh agent instance
3. Stores new messages in database
4. Returns response

No in-memory session state or connection pooling beyond database driver defaults.

### Rationale
- **Horizontal Scaling**: Any server instance can handle any request
- **Resilience**: Server restarts don't lose conversation state
- **Simplicity**: No distributed cache or session management needed
- **Cost Efficiency**: Serverless-compatible architecture

### Conversation History Management
```python
async def get_conversation_history(
    conversation_id: int,
    limit: int = 50
) -> List[dict]:
    """
    Fetch recent conversation history for context.

    Limits to last 50 messages to balance context vs. performance.
    Older messages are preserved in database but not loaded into context.
    """
    messages = await db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(
        Message.created_at.desc()
    ).limit(limit).all()

    # Reverse to chronological order
    messages.reverse()

    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
```

### Database Connection Pooling
Use asyncpg with connection pooling configured for serverless:
```python
# Database configuration
DATABASE_POOL_SIZE = 10  # Max connections per instance
DATABASE_POOL_TIMEOUT = 30  # Seconds
DATABASE_POOL_RECYCLE = 3600  # Recycle connections after 1 hour

# Neon Serverless PostgreSQL supports connection pooling
# Use connection string with pooling enabled
DATABASE_URL = "postgresql://user:pass@host/db?sslmode=require&pool_size=10"
```

### Alternatives Considered
- **Redis for Session State**: Rejected as database is sufficient and reduces dependencies
- **In-Memory LRU Cache**: Rejected to maintain pure stateless architecture
- **WebSocket Connections**: Deferred to future enhancement; HTTP is simpler for MVP

### Performance Optimizations
- Limit conversation history to last 50 messages
- Index on (conversation_id, created_at) for fast history retrieval
- Batch insert for storing user + assistant messages
- Connection pooling to reduce database connection overhead

## 4. OpenAI ChatKit Integration

### Decision
Use OpenAI ChatKit as a pre-built React component library for the chat interface. Configure with domain allowlist for production deployment. Use request-response pattern (not streaming) for MVP.

### Rationale
- **Rapid Development**: Pre-built UI components accelerate frontend development
- **Consistent UX**: ChatKit provides standard chat interface patterns
- **OpenAI Integration**: Designed to work with OpenAI APIs and patterns
- **Customizable**: Can be styled to match application branding

### Frontend Architecture
```typescript
// ChatInterface component
import { ChatKit } from '@openai/chatkit';

export function ChatInterface({ userId }: { userId: string }) {
  const [conversationId, setConversationId] = useState<number | null>(null);

  const handleSendMessage = async (message: string) => {
    const response = await fetch(`/api/${userId}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        conversation_id: conversationId,
        message: message
      })
    });

    const data = await response.json();
    setConversationId(data.conversation_id);

    return data.response;
  };

  return (
    <ChatKit
      onSendMessage={handleSendMessage}
      placeholder="Ask me to manage your tasks..."
    />
  );
}
```

### Domain Allowlist Configuration
For production deployment:
1. Deploy frontend to get production URL (e.g., https://todo-app.vercel.app)
2. Add domain to OpenAI allowlist: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Obtain domain key from OpenAI
4. Configure environment variable: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY=<key>`

### Alternatives Considered
- **Custom Chat UI**: Rejected to accelerate development; can customize later
- **Streaming Responses**: Deferred to future enhancement; adds complexity
- **WebSocket Connection**: Deferred to future enhancement; HTTP sufficient for MVP

### Best Practices Applied
- Environment-based configuration (dev vs. prod)
- Error boundary for graceful failure handling
- Loading states during AI processing
- Message history persistence in backend (not frontend state)

## 5. Database Schema Design

### Decision
Add two new tables (conversations, messages) to existing schema. Use foreign keys to maintain referential integrity. Index on user_id and conversation_id for performance.

### Schema Design

#### Conversations Table
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_conversations (user_id, created_at DESC)
);
```

#### Messages Table
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_conversation FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_conversation_messages (conversation_id, created_at ASC)
);
```

### Rationale
- **Referential Integrity**: Foreign keys ensure data consistency
- **Cascade Deletes**: User deletion removes all conversations and messages
- **Indexing Strategy**: Optimized for common queries (user's conversations, conversation history)
- **Role Constraint**: Enforces valid message roles at database level
- **Timestamps**: Enable sorting and auditing

### Migration Strategy
```python
# Alembic migration: 003_add_conversations_messages.py
def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_user_conversations', 'conversations', ['user_id', 'created_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_role')
    )
    op.create_index('idx_conversation_messages', 'messages', ['conversation_id', 'created_at'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('conversations')
```

### Alternatives Considered
- **Single Messages Table**: Rejected as conversations provide useful grouping
- **NoSQL Document Store**: Rejected to maintain consistency with existing PostgreSQL schema
- **Message Embeddings**: Deferred to future enhancement for semantic search

### Performance Considerations
- Index on (conversation_id, created_at) enables fast history retrieval
- Limit query to last 50 messages to control response time
- Consider partitioning messages table if volume exceeds 10M rows
- Monitor query performance and add indexes as needed

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| Agent Pattern | Stateless per-request instantiation | Enables horizontal scaling and resilience |
| MCP Server | In-process Python module | Simplicity and performance |
| Architecture | Fully stateless with database-backed state | Serverless-compatible, scalable |
| Frontend | OpenAI ChatKit with request-response | Rapid development, standard UX |
| Database | Two new tables with foreign keys | Referential integrity, optimized queries |
| History Limit | Last 50 messages per conversation | Balance context vs. performance |
| Connection Pool | asyncpg with 10 connections | Serverless-optimized |
| Error Handling | Retry with exponential backoff | Resilience to transient failures |

## Next Steps

1. Implement data models (data-model.md)
2. Define API contracts (contracts/)
3. Create quickstart guide (quickstart.md)
4. Begin implementation with /sp.tasks
