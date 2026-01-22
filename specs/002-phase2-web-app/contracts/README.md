# API Contracts Documentation

**Feature**: 002-phase2-web-app | **Date**: 2026-01-21

This directory contains the API contract specifications for the Todo Application REST API.

## Files

- **api-spec.yaml**: OpenAPI 3.0 specification defining all API endpoints, request/response schemas, and authentication

## API Overview

### Base URLs

- **Development**: `http://localhost:8000`
- **Production**: `https://api.todo-app.example.com`

### Authentication

All endpoints except `/api/auth/signup` and `/api/auth/signin` require JWT authentication.

**Authentication Header**:
```
Authorization: Bearer <jwt_token>
```

**Token Acquisition**:
1. Sign up: `POST /api/auth/signup` with email and password
2. Sign in: `POST /api/auth/signin` with email and password
3. Receive JWT token in response
4. Include token in Authorization header for subsequent requests

**Token Expiry**: 7 days (configurable)

## Endpoints Summary

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/signup` | Create new user account | No |
| POST | `/api/auth/signin` | Authenticate and get JWT token | No |
| POST | `/api/auth/signout` | Invalidate session (optional) | Yes |

### Task Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/{user_id}/tasks` | List all tasks for user | Yes |
| POST | `/api/users/{user_id}/tasks` | Create new task | Yes |
| GET | `/api/users/{user_id}/tasks/{task_id}` | Get task details | Yes |
| PUT | `/api/users/{user_id}/tasks/{task_id}` | Update task | Yes |
| DELETE | `/api/users/{user_id}/tasks/{task_id}` | Delete task | Yes |
| PATCH | `/api/users/{user_id}/tasks/{task_id}/complete` | Toggle completion | Yes |

## Request/Response Examples

### Sign Up

**Request**:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

**Response** (201 Created):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "created_at": "2026-01-21T10:30:00Z",
    "updated_at": "2026-01-21T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Sign In

**Request**:
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "created_at": "2026-01-21T10:30:00Z",
    "updated_at": "2026-01-21T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Create Task

**Request**:
```bash
curl -X POST http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, and vegetables"
  }'
```

**Response** (201 Created):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, and vegetables",
  "completed": false,
  "created_at": "2026-01-21T10:35:00Z",
  "updated_at": "2026-01-21T10:35:00Z"
}
```

### List Tasks

**Request**:
```bash
curl -X GET http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, and vegetables",
    "completed": false,
    "created_at": "2026-01-21T10:35:00Z",
    "updated_at": "2026-01-21T10:35:00Z"
  },
  {
    "id": 2,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Finish project report",
    "description": null,
    "completed": true,
    "created_at": "2026-01-21T09:00:00Z",
    "updated_at": "2026-01-21T10:00:00Z"
  }
]
```

### Update Task

**Request**:
```bash
curl -X PUT http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "Buy groceries and household items",
    "description": "Milk, eggs, bread, vegetables, and cleaning supplies"
  }'
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and household items",
  "description": "Milk, eggs, bread, vegetables, and cleaning supplies",
  "completed": false,
  "created_at": "2026-01-21T10:35:00Z",
  "updated_at": "2026-01-21T10:40:00Z"
}
```

### Toggle Task Completion

**Request**:
```bash
curl -X PATCH http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/tasks/1/complete \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and household items",
  "description": "Milk, eggs, bread, vegetables, and cleaning supplies",
  "completed": true,
  "created_at": "2026-01-21T10:35:00Z",
  "updated_at": "2026-01-21T10:42:00Z"
}
```

### Delete Task

**Request**:
```bash
curl -X DELETE http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/tasks/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response** (204 No Content):
```
(empty response body)
```

## Error Responses

All error responses follow this format:

```json
{
  "status_code": 400,
  "message": "Validation error",
  "details": {
    "field": "title",
    "error": "Title is required"
  }
}
```

### Common Error Codes

| Status Code | Description | Example Scenario |
|-------------|-------------|------------------|
| 400 | Bad Request | Missing required field, invalid format |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | User trying to access another user's tasks |
| 404 | Not Found | Task or user doesn't exist |
| 409 | Conflict | Email already exists during signup |
| 500 | Internal Server Error | Database connection error, unexpected error |

## Security Considerations

### Authorization

- All task endpoints verify that `user_id` in URL matches authenticated user's ID
- Attempting to access another user's tasks returns 403 Forbidden
- JWT tokens must be verified on every request

### Input Validation

- Email format validated (must contain @ and valid domain)
- Password minimum 8 characters
- Task title required, 1-200 characters
- Task description optional, max 1000 characters
- HTML tags escaped to prevent XSS attacks

### Rate Limiting

- Not implemented in Phase II
- Recommended for production: 100 requests per minute per IP
- Auth endpoints should have stricter limits (10 requests per minute)

## Testing the API

### Using OpenAPI Spec

1. Import `api-spec.yaml` into Swagger Editor: https://editor.swagger.io/
2. View interactive documentation
3. Test endpoints directly from the UI

### Using Postman

1. Import `api-spec.yaml` into Postman
2. Create environment variables for base URL and token
3. Use collection runner for automated testing

### Using curl

See examples above for curl commands

### Using Thunder Client (VS Code)

1. Install Thunder Client extension
2. Import `api-spec.yaml`
3. Test endpoints with GUI interface

## Versioning

**Current Version**: 2.0.0 (Phase II)

**Version History**:
- 1.0.0: Phase I (Console app, no API)
- 2.0.0: Phase II (Web app with REST API)

**Future Versions**:
- 3.0.0: Phase III (AI chatbot integration)
- 4.0.0: Phase IV (Kubernetes deployment)
- 5.0.0: Phase V (Event-driven architecture)

## Support

For API issues or questions:
- Review this documentation
- Check OpenAPI spec for detailed schemas
- Refer to data-model.md for entity definitions
- See quickstart.md for setup instructions
