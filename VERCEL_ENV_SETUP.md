# Vercel Environment Variables Setup Guide

## Backend Environment Variables

Add these variables to your Vercel backend project via Dashboard:
https://vercel.com/dashboard → Select "backend" project → Settings → Environment Variables

### Required Variables

| Variable Name | Value | Notes |
|---------------|-------|-------|
| `DATABASE_URL` | `postgresql://user:password@host.region.aws.neon.tech/todo_db?sslmode=require` | Replace with your actual Neon PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | `R_LebTaggfw3o8rYBkLK4LnOs5z6HbdR09aGfOq0ryY` | Pre-generated secure secret (or generate your own) |
| `CORS_ORIGINS` | `https://frontend-mauve-iota-87.vercel.app` | Your frontend URL |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_EXPIRY_DAYS` | `7` | Token expiration in days |
| `DEBUG` | `false` | Set to false for production |
| `LOG_LEVEL` | `INFO` | Logging level |

### Important Notes

1. **For each variable**:
   - Click "Add New" button
   - Enter the Key (variable name)
   - Enter the Value
   - Select environments: Check all three boxes (Production, Preview, Development)
   - Click "Save"

2. **DATABASE_URL Format**:
   - Get this from your Neon dashboard: https://console.neon.tech
   - Navigate to your project → Connection Details
   - Copy the connection string
   - Make sure it includes `?sslmode=require` at the end

3. **After adding all variables**:
   - Go to Deployments tab
   - Click the three dots (⋯) on the latest deployment
   - Click "Redeploy"
   - Wait for deployment to complete

### Verification

After redeployment, test these endpoints:

```bash
# Health check
curl https://backend-gamma-seven-21.vercel.app/health

# Root endpoint
curl https://backend-gamma-seven-21.vercel.app/

# API docs
# Visit: https://backend-gamma-seven-21.vercel.app/docs
```

Expected responses:
- `/health` → `{"status": "healthy"}`
- `/` → `{"message": "Todo API is running", "version": "2.0.0", "docs": "/docs"}`

### Generate Your Own Secret (Optional)

If you want to generate a new BETTER_AUTH_SECRET:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Troubleshooting

If you still get 500 errors after adding variables:

1. **Verify variables are added**:
   ```bash
   cd backend
   vercel env ls
   ```
   Should show all 7 variables

2. **Check deployment logs**:
   ```bash
   vercel logs https://backend-gamma-seven-21.vercel.app
   ```

3. **Verify DATABASE_URL is correct**:
   - Test connection locally first
   - Ensure `?sslmode=require` is included
   - Check username/password are correct

4. **Redeploy after adding variables**:
   Environment variables only take effect after redeployment

### Frontend Environment Variables

Your frontend also needs to be updated to point to the backend:

**Add to frontend Vercel project**:

| Variable Name | Value |
|---------------|-------|
| `NEXT_PUBLIC_API_URL` | `https://backend-gamma-seven-21.vercel.app` |
| `BETTER_AUTH_SECRET` | `R_LebTaggfw3o8rYBkLK4LnOs5z6HbdR09aGfOq0ryY` |
| `BETTER_AUTH_URL` | `https://frontend-mauve-iota-87.vercel.app` |

Then redeploy the frontend as well.
