# Quickstart Guide: Full-Stack Multi-User Todo Web Application

**Feature**: 002-phase2-web-app | **Date**: 2026-01-21

This guide provides step-by-step instructions to set up, run, and test the Phase II full-stack web application.

## Prerequisites

### Required Software

**Backend**:
- Python 3.13 or higher
- UV package manager (install: `pip install uv`)
- Git

**Frontend**:
- Node.js 18 or higher
- npm or pnpm package manager

**Database**:
- Neon account (free tier available at https://neon.tech)

**Development Tools** (recommended):
- VS Code or your preferred IDE
- Postman or Thunder Client for API testing
- Git Bash or WSL 2 (for Windows users)

### System Requirements

- Operating System: Windows 10+, macOS 10.15+, or Linux
- RAM: Minimum 4GB (8GB recommended)
- Disk Space: 2GB free space
- Internet connection for package installation and database access

## Initial Setup

### 1. Clone Repository

```bash
# Clone the repository (if not already cloned)
git clone <repository-url>
cd todo_app

# Navigate to Phase II directory
cd phase2  # or wherever the monorepo is located
```

### 2. Database Setup

**Create Neon Database**:

1. Sign up at https://neon.tech (free tier)
2. Create a new project named "todo-app"
3. Create a database named "todo_db"
4. Copy the connection string (format: `postgresql://user:password@host/database`)

**Initialize Database Schema**:

```bash
# Connect to Neon database using psql or Neon SQL Editor
# Run the SQL schema from specs/002-phase2-web-app/data-model.md

# Or use the provided migration script (if available)
cd backend
python scripts/init_db.py
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment with UV
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Edit .env file with your configuration
# Required variables:
# - DATABASE_URL=<your-neon-connection-string>
# - BETTER_AUTH_SECRET=<generate-random-32-char-string>
# - CORS_ORIGINS=http://localhost:3000
```

**Example .env file**:
```env
DATABASE_URL=postgresql://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/todo_db
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars-random
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

**Generate Secret Key** (Python):
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
# or
pnpm install

# Create .env.local file from template
cp .env.local.example .env.local

# Edit .env.local file with your configuration
# Required variables:
# - NEXT_PUBLIC_API_URL=http://localhost:8000
# - BETTER_AUTH_SECRET=<same-secret-as-backend>
```

**Example .env.local file**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars-random
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Running the Application

### Start Backend Server

```bash
# From backend directory
cd backend

# Activate virtual environment (if not already activated)
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Start FastAPI server with hot reload
uvicorn src.main:app --reload --port 8000

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Start Frontend Server

```bash
# From frontend directory (in a new terminal)
cd frontend

# Start Next.js development server
npm run dev
# or
pnpm dev

# Server will start at http://localhost:3000
```

**Expected Output**:
```
  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

### Verify Setup

1. **Backend Health Check**:
   - Open http://localhost:8000/docs
   - You should see the FastAPI Swagger UI with all endpoints

2. **Frontend Health Check**:
   - Open http://localhost:3000
   - You should see the landing page

3. **Database Connection**:
   - Backend logs should show successful database connection
   - No connection errors in terminal

## Testing Scenarios

### Scenario 1: User Registration and Authentication

**Objective**: Verify users can create accounts and sign in

**Steps**:
1. Open http://localhost:3000
2. Click "Sign Up" button
3. Enter email: `test@example.com`
4. Enter password: `TestPass123`
5. Click "Create Account"
6. Verify you're redirected to the tasks page
7. Click "Sign Out"
8. Click "Sign In"
9. Enter same credentials
10. Verify you're signed in and see tasks page

**Expected Results**:
- ✅ Account created successfully
- ✅ Automatic signin after signup
- ✅ Redirect to tasks page
- ✅ Sign out clears session
- ✅ Sign in with existing credentials works
- ✅ Invalid credentials show error message

### Scenario 2: Create and View Tasks

**Objective**: Verify task creation and display

**Steps**:
1. Sign in to the application
2. Click "Add Task" or "+" button
3. Enter title: "Buy groceries"
4. Enter description: "Milk, eggs, bread"
5. Click "Save" or "Create"
6. Verify task appears in the list
7. Refresh the page (F5)
8. Verify task still appears (persistence)

**Expected Results**:
- ✅ Task creation form appears
- ✅ Task is created and appears in list
- ✅ Task shows title, description, and incomplete status
- ✅ Task persists after page refresh
- ✅ Empty title shows validation error

### Scenario 3: Update Task

**Objective**: Verify task editing functionality

**Steps**:
1. Sign in and view your tasks
2. Click "Edit" button on a task
3. Change title to "Buy groceries and household items"
4. Change description to "Milk, eggs, bread, cleaning supplies"
5. Click "Save"
6. Verify changes are reflected immediately
7. Refresh page
8. Verify changes persisted

**Expected Results**:
- ✅ Edit form pre-fills with current values
- ✅ Changes save successfully
- ✅ Updated task displays new values
- ✅ Changes persist after refresh
- ✅ Cancel button discards changes

### Scenario 4: Toggle Task Completion

**Objective**: Verify completion status toggling

**Steps**:
1. Sign in and view your tasks
2. Click checkbox next to an incomplete task
3. Verify task shows as complete (strikethrough, checkmark, etc.)
4. Click checkbox again
5. Verify task shows as incomplete
6. Refresh page
7. Verify status persisted

**Expected Results**:
- ✅ Clicking checkbox toggles status
- ✅ Visual indicator shows completion (strikethrough, color, icon)
- ✅ Status persists after refresh
- ✅ Can toggle back to incomplete

### Scenario 5: Delete Task

**Objective**: Verify task deletion

**Steps**:
1. Sign in and view your tasks
2. Click "Delete" button on a task
3. Confirm deletion (if confirmation dialog appears)
4. Verify task is removed from list
5. Refresh page
6. Verify task is still gone (permanent deletion)

**Expected Results**:
- ✅ Delete button removes task
- ✅ Task disappears from list immediately
- ✅ Deletion is permanent (persists after refresh)
- ✅ Optional: Confirmation dialog prevents accidental deletion

### Scenario 6: Data Isolation

**Objective**: Verify users can only see their own tasks

**Steps**:
1. Sign up as User A (email: `usera@example.com`)
2. Create 2-3 tasks as User A
3. Sign out
4. Sign up as User B (email: `userb@example.com`)
5. Verify User B sees empty task list (no User A tasks)
6. Create 1-2 tasks as User B
7. Sign out
8. Sign in as User A
9. Verify User A only sees their own tasks (not User B's)

**Expected Results**:
- ✅ Each user sees only their own tasks
- ✅ No cross-user data leakage
- ✅ Task counts are independent per user

### Scenario 7: Responsive Design

**Objective**: Verify UI adapts to different screen sizes

**Steps**:
1. Open application in desktop browser (1920px width)
2. Verify layout uses full width effectively
3. Resize browser to tablet width (768px)
4. Verify layout adjusts appropriately
5. Resize to mobile width (375px)
6. Verify layout stacks vertically and remains usable
7. Test all operations (create, edit, delete) on mobile

**Expected Results**:
- ✅ Desktop layout is spacious and organized
- ✅ Tablet layout adjusts columns/spacing
- ✅ Mobile layout stacks vertically
- ✅ All functionality works on all screen sizes
- ✅ No horizontal scrolling on mobile

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
# Reinstall dependencies
uv pip install -r requirements.txt
```

**Problem**: `Database connection error`
**Solution**:
- Verify DATABASE_URL in .env is correct
- Check Neon dashboard for database status
- Ensure database is not paused (Neon auto-pauses after inactivity)
- Test connection with psql: `psql <DATABASE_URL>`

**Problem**: `CORS error in browser console`
**Solution**:
- Verify CORS_ORIGINS in backend .env includes frontend URL
- Restart backend server after changing .env
- Check browser console for specific CORS error details

### Frontend Issues

**Problem**: `Module not found` errors
**Solution**:
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem**: `API calls failing with 404`
**Solution**:
- Verify NEXT_PUBLIC_API_URL in .env.local is correct
- Ensure backend server is running on port 8000
- Check browser Network tab for actual request URL

**Problem**: `Authentication not working`
**Solution**:
- Verify BETTER_AUTH_SECRET matches in both frontend and backend
- Clear browser cookies and localStorage
- Check browser console for JWT errors
- Verify token is being sent in Authorization header

### Database Issues

**Problem**: `Tables not found`
**Solution**:
```bash
# Run database initialization script
cd backend
python scripts/init_db.py
# Or manually run SQL from data-model.md
```

**Problem**: `Connection pool exhausted`
**Solution**:
- Restart backend server
- Check for connection leaks in code
- Increase connection pool size in Neon dashboard

## Development Tips

### Hot Reload

- **Backend**: Uvicorn automatically reloads on file changes
- **Frontend**: Next.js automatically reloads on file changes
- If changes don't appear, try hard refresh (Ctrl+Shift+R)

### Debugging

**Backend**:
```python
# Add print statements or use debugger
import pdb; pdb.set_trace()

# Or use VS Code debugger with launch.json
```

**Frontend**:
```typescript
// Use console.log for debugging
console.log('User data:', user);

// Or use browser DevTools debugger
debugger;
```

### API Testing

**Using FastAPI Docs**:
1. Open http://localhost:8000/docs
2. Click "Authorize" button
3. Enter JWT token from signin response
4. Test endpoints directly from UI

**Using curl**:
```bash
# Sign up
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123"}'

# Save token from response, then use it:
TOKEN="<jwt-token-from-response>"

# List tasks
curl http://localhost:8000/api/users/<user-id>/tasks \
  -H "Authorization: Bearer $TOKEN"
```

## Next Steps

After completing the quickstart:

1. **Run Tests**: Execute test suites (when implemented)
   ```bash
   # Backend tests
   cd backend && pytest

   # Frontend tests
   cd frontend && npm test
   ```

2. **Review Code**: Examine generated implementation
   - Backend: `backend/src/`
   - Frontend: `frontend/src/`

3. **Create Tasks**: Run `/sp.tasks` to break down implementation

4. **Implement Features**: Run `/sp.implement` to generate code

5. **Deploy**: Follow deployment guide (when ready)

## Support

For issues or questions:
- Review specification: `specs/002-phase2-web-app/spec.md`
- Check implementation plan: `specs/002-phase2-web-app/plan.md`
- Review API contracts: `specs/002-phase2-web-app/contracts/`
- Consult data model: `specs/002-phase2-web-app/data-model.md`

## Success Criteria Validation

After completing all scenarios, verify these success criteria from the spec:

- ✅ SC-001: Account creation and signin within 1 minute
- ✅ SC-002: Task list loads within 2 seconds
- ✅ SC-003: Task creation completes within 3 seconds
- ✅ SC-004: All 5 operations work without errors
- ✅ SC-005: Data isolation verified (users see only their tasks)
- ✅ SC-006: Persistence verified (data survives restart)
- ✅ SC-007: Responsive design works (320px-1920px)
- ✅ SC-008: 95% success rate on operations
- ✅ SC-009: Handles 100 concurrent users (load testing required)
- ✅ SC-010: Basic accessibility (keyboard navigation, screen readers)

**Phase II is complete when all success criteria are validated!**
