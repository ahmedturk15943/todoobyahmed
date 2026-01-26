# Quick Deployment Setup Guide

## 🚀 Your Deployment URLs
- **Frontend**: https://frontend-mauve-iota-87.vercel.app
- **Backend**: https://backend-gamma-seven-21.vercel.app
- **GitHub**: https://github.com/ahmedturk15943/todo2.git

## ⚠️ Current Status
- ✅ Frontend: Deployed and accessible
- ❌ Backend: Deployed but needs environment variables

## 🔧 Required Setup Steps

### Step 1: Set Backend Environment Variables

Go to: https://vercel.com/ahmed-raza-turks-projects/backend/settings/environment-variables

Click "Add New" and add these variables (one at a time):

**Required Variables:**

1. **DATABASE_URL** (Production)
   - Value: Your Neon PostgreSQL connection string
   - Example: `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`
   - Get this from: https://console.neon.tech

2. **BETTER_AUTH_SECRET** (Production)
   - Value: Generate using: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - Example: `xK7mP9nQ2rS5tU8vW1yZ4aB6cD9eF2gH3iJ5kL8mN1oP4qR7sT0uV3wX6yZ9`
   - ⚠️ Save this value - you'll need it for frontend too!

3. **CORS_ORIGINS** (Production)
   - Value: `https://frontend-mauve-iota-87.vercel.app`

4. **JWT_ALGORITHM** (Production)
   - Value: `HS256`

5. **JWT_EXPIRY_DAYS** (Production)
   - Value: `7`

6. **DEBUG** (Production)
   - Value: `false`

7. **LOG_LEVEL** (Production)
   - Value: `INFO`

### Step 2: Set Frontend Environment Variables

Go to: https://vercel.com/ahmed-raza-turks-projects/frontend/settings/environment-variables

Click "Add New" and add these variables:

1. **NEXT_PUBLIC_API_URL** (Production)
   - Value: `https://backend-gamma-seven-21.vercel.app`

2. **BETTER_AUTH_SECRET** (Production)
   - Value: (Use the SAME value from backend step 2)

3. **BETTER_AUTH_URL** (Production)
   - Value: `https://frontend-mauve-iota-87.vercel.app`

### Step 3: Redeploy Both Applications

After setting all environment variables, redeploy:

**Option A: Via Vercel Dashboard**
1. Go to backend deployments: https://vercel.com/ahmed-raza-turks-projects/backend
2. Click on the latest deployment
3. Click "Redeploy" button
4. Repeat for frontend: https://vercel.com/ahmed-raza-turks-projects/frontend

**Option B: Via CLI**
```bash
# Redeploy backend
cd backend
vercel --prod

# Redeploy frontend
cd frontend
vercel --prod
```

### Step 4: Initialize Database

Before using the app, you need to set up your database:

1. Create a Neon PostgreSQL database at https://console.neon.tech
2. Copy the connection string
3. Run the initialization script:
   ```bash
   # Connect to your Neon database and run:
   psql "your-connection-string" -f backend/scripts/init_db.sql
   ```

### Step 5: Test Your Application

1. Visit: https://frontend-mauve-iota-87.vercel.app
2. Click "Sign Up" to create an account
3. Sign in and start managing tasks

## 🔍 Troubleshooting

### Backend Health Check
```bash
curl https://backend-gamma-seven-21.vercel.app/health
```
Should return: `{"status":"healthy"}`

### Check Logs
```bash
# Backend logs
vercel logs https://backend-gamma-seven-21.vercel.app

# Frontend logs
vercel logs https://frontend-mauve-iota-87.vercel.app
```

### Common Issues

**"FUNCTION_INVOCATION_FAILED"**
- Missing environment variables
- Database connection failed
- Solution: Set all required environment variables and redeploy

**"Cannot connect to API"**
- CORS not configured correctly
- Backend URL incorrect in frontend
- Solution: Verify CORS_ORIGINS and NEXT_PUBLIC_API_URL

**"Database connection error"**
- Invalid DATABASE_URL
- Database not initialized
- Solution: Check connection string and run init_db.sql

## 📝 Next Steps After Setup

1. **Custom Domain** (Optional)
   - Add your domain in Vercel project settings
   - Update environment variables with new domain

2. **Monitoring**
   - Set up Vercel Analytics
   - Monitor error rates and performance

3. **CI/CD**
   - Automatic deployments are already configured via GitHub
   - Every push to main branch will trigger a deployment

## 🆘 Need Help?

If you encounter issues:
1. Check the logs using `vercel logs <url>`
2. Verify all environment variables are set correctly
3. Ensure database is initialized and accessible
4. Check that CORS_ORIGINS matches your frontend URL exactly
