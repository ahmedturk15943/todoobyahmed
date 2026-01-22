# Todo Frontend - Next.js

**Version**: 2.0.0
**Phase**: Phase II - Multi-User Web Application
**Framework**: Next.js 16+ with App Router

## Overview

Modern, responsive web interface for the Todo application with user authentication and real-time task management.

## Features

- User authentication with Better Auth
- Responsive design (mobile to desktop)
- Task CRUD operations
- Real-time UI updates
- Server and Client Components
- TypeScript for type safety

## Prerequisites

- Node.js 18+
- npm or pnpm
- Backend API running (see backend/README.md)

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Copy `.env.local.example` to `.env.local` and fill in values:

```bash
cp .env.local.example .env.local
```

Required environment variables:
- `NEXT_PUBLIC_API_URL`: Backend API URL (e.g., `http://localhost:8000`)
- `BETTER_AUTH_SECRET`: Shared secret for JWT (must match backend)
- `BETTER_AUTH_URL`: Frontend URL (e.g., `http://localhost:3000`)

### 3. Start Development Server

```bash
npm run dev
```

Application will start at `http://localhost:3000`

## Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run with coverage
npm test -- --coverage
```

## Building for Production

```bash
# Build optimized production bundle
npm run build

# Start production server
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── (auth)/          # Auth route group
│   │   └── (dashboard)/     # Protected routes
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   ├── auth/            # Auth forms
│   │   └── tasks/           # Task components
│   ├── lib/
│   │   ├── api.ts           # API client
│   │   ├── auth.ts          # Better Auth config
│   │   └── utils.ts         # Utilities
│   ├── types/               # TypeScript types
│   └── styles/              # Global styles
├── public/                  # Static assets
├── tests/                   # Test files
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

## Development

### Code Quality

```bash
# Lint code
npm run lint

# Format code (if Prettier configured)
npm run format
```

### Component Development

- Use Server Components by default
- Add `'use client'` only when needed (interactivity, hooks, browser APIs)
- Keep components small and focused
- Use TypeScript for all components

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Configure environment variables
4. Deploy

### Other Platforms

Build the production bundle and deploy the `.next` directory:

```bash
npm run build
npm start
```

## Troubleshooting

### API Connection Issues

- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check backend server is running
- Verify CORS is configured correctly in backend

### Authentication Issues

- Verify `BETTER_AUTH_SECRET` matches backend
- Clear browser cookies and try again
- Check browser console for errors

### Build Errors

- Delete `.next` directory and rebuild
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

## License

Copyright (c) 2025 Evolution of Todo Project. All rights reserved.
