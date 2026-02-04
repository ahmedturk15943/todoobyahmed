#!/bin/bash
# Script to add environment variables to Vercel backend
# Run this from the backend directory

echo "Adding environment variables to Vercel backend..."

# Note: You'll be prompted to enter values for each variable
# When prompted, select: Production, Preview, Development (all environments)

# 1. DATABASE_URL
echo "Adding DATABASE_URL..."
vercel env add DATABASE_URL production preview development

# 2. BETTER_AUTH_SECRET
echo "Adding BETTER_AUTH_SECRET..."
echo "R_LebTaggfw3o8rYBkLK4LnOs5z6HbdR09aGfOq0ryY" | vercel env add BETTER_AUTH_SECRET production preview development

# 3. CORS_ORIGINS
echo "Adding CORS_ORIGINS..."
echo "https://frontend-mauve-iota-87.vercel.app" | vercel env add CORS_ORIGINS production preview development

# 4. JWT_ALGORITHM
echo "Adding JWT_ALGORITHM..."
echo "HS256" | vercel env add JWT_ALGORITHM production preview development

# 5. JWT_EXPIRY_DAYS
echo "Adding JWT_EXPIRY_DAYS..."
echo "7" | vercel env add JWT_EXPIRY_DAYS production preview development

# 6. DEBUG
echo "Adding DEBUG..."
echo "false" | vercel env add DEBUG production

# 7. LOG_LEVEL
echo "Adding LOG_LEVEL..."
echo "INFO" | vercel env add LOG_LEVEL production preview development

echo "All environment variables added!"
echo "Now redeploying to production..."
vercel --prod

echo "Done! Test your backend at: https://backend-gamma-seven-21.vercel.app/health"
