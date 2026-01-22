# Phase II Setup Guide

## Step 1: Database Setup ✅ REQUIRED FIRST

### Create Neon PostgreSQL Database

1. **Sign up for Neon** (if you haven't already):
   - Visit: https://neon.tech
   - Click "Sign Up" (free tier available)
   - Verify your email

2. **Create a new project**:
   - Click "Create Project"
   - Name: "todo-app" (or any name you prefer)
   - Region: Choose closest to you
   - Click "Create Project"

3. **Get your connection string**:
   - After project creation, you'll see the connection string
   - It looks like: `postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`
   - Copy this entire string

4. **Update backend/.env**:
   - Open `backend/.env`
   - Replace the `DATABASE_URL` value with your actual connection string
   - Save the file

5. **Initialize the database**:
   - In Neon dashboard, click "SQL Editor"
   - Copy the contents of `backend/scripts/init_db.sql`
   - Paste into the SQL Editor
   - Click "Run" to create tables and indexes

## Step 2: Install Backend Dependencies

```bash
cd backend

# Create virtual environment
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"
```

## Step 3: Install Frontend Dependencies

```bash
cd frontend

# Install dependencies
npm install
```

## Step 4: Start the Servers

### Terminal 1 - Backend:
```bash
cd backend
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
uvicorn src.main:app --reload --port 8000
```

Backend will start at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Frontend will start at: http://localhost:3000

## Step 5: Test the Application

1. **Visit the app**: http://localhost:3000
2. **Sign Up**: Create a new account
3. **Sign In**: Log in with your credentials
4. **Create Tasks**: Add some tasks
5. **Test Features**: Edit, delete, complete tasks

## Verification Checklist

- [ ] Neon database created and connection string copied
- [ ] Database initialized with init_db.sql script
- [ ] backend/.env updated with DATABASE_URL
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can sign up and create account
- [ ] Can sign in with credentials
- [ ] Can create, view, edit, delete tasks

## Troubleshooting

### Backend won't start
- Check DATABASE_URL is correct in backend/.env
- Verify virtual environment is activated
- Check port 8000 is not in use: `netstat -ano | findstr :8000`

### Frontend won't start
- Check NEXT_PUBLIC_API_URL in frontend/.env.local
- Verify node_modules installed: `npm install`
- Check port 3000 is not in use: `netstat -ano | findstr :3000`

### Can't connect to database
- Verify Neon database is running (check dashboard)
- Check connection string includes `?sslmode=require`
- Ensure database tables created (run init_db.sql)

### Authentication errors
- Verify BETTER_AUTH_SECRET matches in both .env files
- Clear browser localStorage and cookies
- Check backend logs for JWT errors

## Next Steps After Setup

Once everything is running:
1. Test all user flows (signup, signin, CRUD operations)
2. Run backend tests: `cd backend && pytest`
3. Run frontend tests: `cd frontend && npm test`
4. Review API documentation: http://localhost:8000/docs
5. Test responsive design on different screen sizes

## Environment Variables Summary

**Backend (.env)**:
- DATABASE_URL: Your Neon PostgreSQL connection string
- BETTER_AUTH_SECRET: zRbY8F_Ir-BbU4soAF_QwwRNoIqwd99N9xFFTBoss2Q
- CORS_ORIGINS: http://localhost:3000

**Frontend (.env.local)**:
- NEXT_PUBLIC_API_URL: http://localhost:8000
- BETTER_AUTH_SECRET: zRbY8F_Ir-BbU4soAF_QwwRNoIqwd99N9xFFTBoss2Q
- BETTER_AUTH_URL: http://localhost:3000
