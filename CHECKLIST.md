# Phase II Todo Application - Setup Checklist

## ✅ Completed

- [x] Project structure created (backend/, frontend/)
- [x] Backend code implemented (FastAPI + SQLModel)
- [x] Frontend code implemented (Next.js + TypeScript)
- [x] Environment files created (.env, .env.local)
- [x] Authentication secret generated and configured
- [x] Database schema script ready (init_db.sql)
- [x] Documentation created (README.md, SETUP.md)
- [x] Quick start scripts created (quickstart.bat, quickstart.sh)

## 🔴 Required: Database Setup

**You must complete this step before running the application!**

### Option 1: Use Neon (Recommended - Free Tier Available)

1. **Create Neon Account**:
   - Visit: https://neon.tech
   - Click "Sign Up" (free tier available)
   - Verify your email

2. **Create Database Project**:
   - Click "Create Project"
   - Name: `todo-app`
   - Region: Choose closest to you
   - Click "Create Project"

3. **Get Connection String**:
   - After creation, copy the connection string
   - Format: `postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`

4. **Update Backend Configuration**:
   - Open: `backend/.env`
   - Replace `DATABASE_URL` with your actual connection string
   - Save the file

5. **Initialize Database**:
   - In Neon dashboard, click "SQL Editor"
   - Copy contents of `backend/scripts/init_db.sql`
   - Paste into SQL Editor
   - Click "Run"
   - Verify: You should see "Users table created" and "Tasks table created"

### Option 2: Use Local PostgreSQL

If you prefer local PostgreSQL:

1. Install PostgreSQL 14+ on your machine
2. Create a database: `createdb todo_app`
3. Update `backend/.env` with: `DATABASE_URL=postgresql://localhost/todo_app`
4. Run the init script: `psql -d todo_app -f backend/scripts/init_db.sql`

## 📦 Next: Install Dependencies

### Backend Dependencies

```bash
cd backend

# Create virtual environment
uv venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"
```

### Frontend Dependencies

```bash
cd frontend

# Install npm packages
npm install
```

## 🚀 Start the Application

### Terminal 1 - Backend Server

```bash
cd backend
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
uvicorn src.main:app --reload --port 8000
```

**Backend running at**: http://localhost:8000
**API docs at**: http://localhost:8000/docs

### Terminal 2 - Frontend Server

```bash
cd frontend
npm run dev
```

**Frontend running at**: http://localhost:3000

## 🧪 Test the Application

1. Visit http://localhost:3000
2. Click "Sign Up" and create an account
3. Sign in with your credentials
4. Create a new task
5. Test edit, delete, and complete features

## 📋 Quick Start Options

### Option A: Manual Setup (Recommended for learning)
Follow the steps above one by one

### Option B: Quick Start Script (Windows)
```bash
quickstart.bat
```

### Option C: Quick Start Script (macOS/Linux)
```bash
./quickstart.sh
```

**Note**: Scripts will pause for you to complete database setup first!

## 🔍 Verification

After setup, verify everything works:

- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Can access http://localhost:3000
- [ ] Can access http://localhost:8000/docs (API documentation)
- [ ] Can create a new account
- [ ] Can sign in
- [ ] Can create tasks
- [ ] Can edit tasks
- [ ] Can delete tasks
- [ ] Can mark tasks complete/incomplete

## 🆘 Troubleshooting

### Backend won't start
- **Error: "Could not connect to database"**
  - Check DATABASE_URL in backend/.env
  - Verify Neon database is running
  - Ensure connection string includes `?sslmode=require`

- **Error: "Module not found"**
  - Activate virtual environment: `.venv\Scripts\activate`
  - Reinstall dependencies: `uv pip install -e ".[dev]"`

### Frontend won't start
- **Error: "Cannot find module"**
  - Delete node_modules: `rm -rf node_modules`
  - Reinstall: `npm install`

- **Error: "Port 3000 already in use"**
  - Kill process on port 3000
  - Or use different port: `npm run dev -- -p 3001`

### Authentication errors
- **Error: "Invalid token"**
  - Verify BETTER_AUTH_SECRET matches in both .env files
  - Clear browser localStorage and cookies
  - Try signing up with a new account

### Database errors
- **Error: "relation does not exist"**
  - Run init_db.sql script in Neon SQL Editor
  - Verify tables created: Check Neon dashboard

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **Project README**: README.md
- **Setup Guide**: SETUP.md
- **Backend README**: backend/README.md
- **Frontend README**: frontend/README.md

## 🎯 Current Status

**Environment Configuration**: ✅ Complete
- Backend .env: Created with auth secret
- Frontend .env.local: Created with auth secret
- Auth secret: `zRbY8F_Ir-BbU4soAF_QwwRNoIqwd99N9xFFTBoss2Q`

**Database Setup**: ⏳ Waiting for you
- Need to create Neon account
- Need to create database project
- Need to update DATABASE_URL in backend/.env
- Need to run init_db.sql script

**Dependencies**: ⏳ Waiting for database setup
- Backend dependencies: Not installed yet
- Frontend dependencies: Not installed yet

**Next Action**: Complete database setup, then run quickstart script or follow manual steps above.
