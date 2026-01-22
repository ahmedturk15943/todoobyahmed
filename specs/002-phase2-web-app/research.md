# Research: Full-Stack Multi-User Todo Web Application

**Feature**: 002-phase2-web-app | **Date**: 2026-01-21

This document captures technical research and decisions made during the planning phase.

## Technology Decisions

### Frontend Framework: Next.js 16+ with App Router

**Decision**: Use Next.js 16+ with App Router for the frontend

**Rationale**:
- Server Components by default reduce client-side JavaScript bundle size
- Built-in routing with file-system based structure
- Excellent TypeScript support
- Strong ecosystem and community
- Simplified data fetching with async/await in components
- Built-in optimization (image optimization, code splitting, etc.)

**Alternatives Considered**:
- **React + Vite**: More lightweight but requires manual routing setup and lacks server components
- **SvelteKit**: Excellent performance but smaller ecosystem and team may be less familiar
- **Vue + Nuxt**: Good option but TypeScript support not as mature as Next.js

**Best Practices**:
- Use Server Components by default, Client Components only when needed (interactivity, browser APIs)
- Implement route groups for logical organization: (auth) and (dashboard)
- Use Next.js middleware for authentication checks
- Leverage React Server Actions for form submissions (optional, can use API routes)
- Implement proper error boundaries and loading states

### Backend Framework: FastAPI

**Decision**: Use FastAPI for the REST API backend

**Rationale**:
- Automatic OpenAPI documentation generation
- Built-in request/response validation with Pydantic
- Excellent async/await support for database operations
- Type hints throughout for better IDE support
- High performance (comparable to Node.js and Go)
- Easy integration with SQLModel (Pydantic + SQLAlchemy)

**Alternatives Considered**:
- **Flask**: Simpler but lacks automatic validation and async support
- **Django REST Framework**: More batteries-included but heavier and more opinionated
- **Node.js + Express**: Would match frontend language but Python chosen for Phase I consistency

**Best Practices**:
- Use dependency injection for database sessions and authentication
- Implement proper exception handlers for consistent error responses
- Use Pydantic models for request/response validation
- Organize routes by resource (auth, tasks)
- Implement CORS middleware for frontend communication
- Use async database operations with SQLModel

### ORM: SQLModel

**Decision**: Use SQLModel for database models and queries

**Rationale**:
- Combines SQLAlchemy (powerful ORM) with Pydantic (validation)
- Single model definition serves as both database model and API schema
- Excellent FastAPI integration
- Type-safe queries with IDE autocomplete
- Async support for non-blocking database operations

**Alternatives Considered**:
- **SQLAlchemy alone**: More verbose, requires separate Pydantic models
- **Tortoise ORM**: Async-first but smaller community and less mature
- **Raw SQL with asyncpg**: Maximum control but more boilerplate and no ORM benefits

**Best Practices**:
- Define relationships between User and Task models
- Use Pydantic validators for field validation
- Implement proper indexes for query performance (user_id, completed)
- Use async session management with context managers
- Separate database models from API response models when needed

### Database: Neon Serverless PostgreSQL

**Decision**: Use Neon Serverless PostgreSQL for data persistence

**Rationale**:
- Serverless architecture with automatic scaling
- PostgreSQL compatibility (mature, reliable, feature-rich)
- Generous free tier for development
- Built-in connection pooling
- Automatic backups and point-in-time recovery
- No infrastructure management required

**Alternatives Considered**:
- **Supabase**: Good option but adds unnecessary features (auth, storage, realtime)
- **PlanetScale**: MySQL-based, less feature-rich than PostgreSQL
- **Local PostgreSQL**: Requires manual setup and management

**Best Practices**:
- Use connection pooling to handle concurrent requests
- Store connection string in environment variables
- Implement proper migration strategy (Alembic if needed)
- Use transactions for multi-step operations
- Index foreign keys and frequently queried columns

### Authentication: Better Auth + JWT

**Decision**: Use Better Auth on frontend with JWT tokens for API authentication

**Rationale**:
- Better Auth provides modern, type-safe authentication for Next.js
- JWT tokens enable stateless authentication (no session storage needed)
- Tokens can be verified independently by backend
- Supports multiple authentication strategies
- Good TypeScript support and documentation

**Alternatives Considered**:
- **NextAuth.js**: Popular but more complex setup for simple email/password auth
- **Clerk**: Excellent but paid service, overkill for Phase II
- **Custom auth**: More control but requires implementing security best practices from scratch

**Best Practices**:
- Store JWT tokens in httpOnly cookies (not localStorage for security)
- Implement token refresh mechanism (7-day expiry)
- Use shared secret between frontend and backend (BETTER_AUTH_SECRET)
- Hash passwords with bcrypt (minimum 10 rounds)
- Implement rate limiting on auth endpoints (prevent brute force)
- Validate JWT signature and expiry on every API request

### JWT Integration Pattern

**Decision**: Frontend includes JWT in Authorization header, backend verifies with middleware

**Implementation**:
1. User signs up/signs in via Better Auth
2. Better Auth issues JWT token with user ID and email
3. Frontend stores token in httpOnly cookie
4. Frontend includes token in `Authorization: Bearer <token>` header for API requests
5. Backend middleware extracts token, verifies signature with shared secret
6. Backend decodes token to get user ID, attaches to request context
7. API routes filter data by authenticated user ID

**Security Considerations**:
- Tokens expire after 7 days (configurable)
- Shared secret must be strong (minimum 32 characters, random)
- Backend validates token signature to prevent tampering
- User ID in URL must match authenticated user ID (prevent unauthorized access)
- Implement proper CORS to prevent cross-origin attacks

## Integration Patterns

### Frontend-Backend Communication

**Pattern**: REST API with JSON payloads

**Endpoints**:
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Authenticate user, return JWT
- `POST /api/auth/signout` - Invalidate session (optional)
- `GET /api/users/{user_id}/tasks` - List all tasks for user
- `POST /api/users/{user_id}/tasks` - Create new task
- `GET /api/users/{user_id}/tasks/{task_id}` - Get task details
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/users/{user_id}/tasks/{task_id}/complete` - Toggle completion

**Request/Response Format**:
- Content-Type: application/json
- Authentication: Bearer token in Authorization header
- Error responses: Consistent format with status code, message, details

### Database Schema Design

**User Table**:
- `id`: UUID (primary key)
- `email`: String (unique, indexed)
- `password_hash`: String (bcrypt hashed)
- `created_at`: Timestamp
- `updated_at`: Timestamp

**Task Table**:
- `id`: Integer (primary key, auto-increment)
- `user_id`: UUID (foreign key to users.id, indexed)
- `title`: String (max 200 chars, required)
- `description`: Text (max 1000 chars, optional)
- `completed`: Boolean (default false, indexed)
- `created_at`: Timestamp
- `updated_at`: Timestamp

**Relationships**:
- One User has many Tasks (one-to-many)
- Each Task belongs to one User (foreign key constraint)
- Cascade delete: When user deleted, all their tasks deleted

### Error Handling Strategy

**Backend**:
- 400 Bad Request: Validation errors (missing required fields, invalid format)
- 401 Unauthorized: Missing or invalid JWT token
- 403 Forbidden: User attempting to access another user's resources
- 404 Not Found: Resource doesn't exist
- 500 Internal Server Error: Unexpected errors (database connection, etc.)

**Frontend**:
- Display user-friendly error messages
- Handle network errors gracefully (retry, offline message)
- Validate input client-side before API call (faster feedback)
- Show loading states during API calls
- Implement error boundaries for unexpected errors

## Development Workflow

### Local Development Setup

1. **Backend**:
   - Install Python 3.13+ and UV
   - Create virtual environment: `uv venv`
   - Install dependencies: `uv pip install -r requirements.txt`
   - Set environment variables in `.env` file
   - Run migrations (if using Alembic)
   - Start server: `uvicorn src.main:app --reload --port 8000`

2. **Frontend**:
   - Install Node.js 18+ and npm/pnpm
   - Install dependencies: `npm install`
   - Set environment variables in `.env.local` file
   - Start dev server: `npm run dev` (runs on port 3000)

3. **Database**:
   - Create Neon project and database
   - Copy connection string to `.env` files
   - Run initial migrations to create tables

### Testing Strategy

**Backend Tests**:
- Unit tests: Test models, services in isolation
- Integration tests: Test API endpoints with test database
- Contract tests: Validate API responses match OpenAPI spec
- Use pytest fixtures for database setup/teardown
- Mock external dependencies (database for unit tests)

**Frontend Tests**:
- Component tests: Test UI components with React Testing Library
- Integration tests: Test user flows (signup, create task, etc.)
- Mock API calls with MSW (Mock Service Worker)
- Test accessibility (keyboard navigation, screen readers)

### Deployment Considerations

**Backend**:
- Deploy to platform supporting Python (Vercel, Railway, Render, DigitalOcean)
- Set environment variables in platform dashboard
- Use production-grade ASGI server (Uvicorn with Gunicorn)
- Enable CORS for frontend domain only

**Frontend**:
- Deploy to Vercel (optimal for Next.js)
- Set environment variables for API URL and auth secret
- Configure custom domain (optional)
- Enable automatic deployments from git

**Database**:
- Neon handles scaling and backups automatically
- Monitor connection pool usage
- Set up alerts for high query latency

## Open Questions & Risks

### Resolved
- ✅ How to handle JWT verification in FastAPI? → Use middleware with python-jose library
- ✅ How to share auth secret between frontend and backend? → Environment variable in both services
- ✅ How to prevent users from accessing other users' tasks? → Validate user_id in URL matches JWT user_id

### Remaining
- ⚠️ Should we implement password reset in Phase II? → Deferred to later phase per spec
- ⚠️ Should we add email verification? → Deferred to later phase per spec
- ⚠️ How to handle database migrations? → Use Alembic if schema changes needed, or manual SQL for initial setup

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Better Auth Documentation](https://www.better-auth.com/docs)
- [Neon Documentation](https://neon.tech/docs)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
