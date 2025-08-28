# Exercise 2: Backend Development (8 minutes)

## Objective
Build a complete REST API backend using Amazon Q Developer for code generation, debugging, and security.

## Step 1: Database Layer (2 minutes)
**Prompt Amazon Q:**
```
Create database connection and models for:
- User model with authentication methods
- Task model with CRUD operations
- Database connection pool setup
- Migration scripts
```

**Generate:**
- `src/models/User.ts`
- `src/models/Task.ts`
- `src/database/connection.ts`
- `src/database/migrations/`

## Step 2: Authentication System (2 minutes)
**Prompt Amazon Q:**
```
Implement JWT authentication with:
- User registration and login endpoints
- Password hashing with bcrypt
- JWT token generation and validation
- Authentication middleware
```

**Generate:**
- `src/auth/authController.ts`
- `src/middleware/auth.ts`
- `src/utils/jwt.ts`
- `src/utils/password.ts`

## Step 3: Task API Endpoints (2 minutes)
**Prompt Amazon Q:**
```
Create REST API endpoints for tasks:
- GET /api/tasks - List user tasks with filtering
- POST /api/tasks - Create new task
- PUT /api/tasks/:id - Update task
- DELETE /api/tasks/:id - Delete task
- Include validation and error handling
```

**Generate:**
- `src/controllers/taskController.ts`
- `src/routes/tasks.ts`
- `src/middleware/validation.ts`

## Step 4: Security & Error Handling (1 minute)
**Prompt Amazon Q:**
```
Add security middleware and error handling:
- Rate limiting
- CORS configuration
- Input sanitization
- Global error handler
- Request logging
```

**Use Amazon Q Security Scan:**
1. Run security analysis on generated code
2. Fix any vulnerabilities found
3. Add security headers

## Step 5: Testing & Debugging (1 minute)
**Prompt Amazon Q:**
```
Generate unit tests for:
- Authentication functions
- Task CRUD operations
- API endpoint tests
- Database model tests
```

**Debug with Amazon Q:**
1. Test API endpoints
2. Fix any runtime errors
3. Optimize database queries

## Key Files Generated
```
backend/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── middleware/
│   ├── utils/
│   └── app.ts
├── tests/
├── package.json
└── tsconfig.json
```

## Verification Checklist
- [ ] Database models working
- [ ] Authentication endpoints functional
- [ ] Task CRUD operations complete
- [ ] Security middleware active
- [ ] Tests passing
- [ ] No security vulnerabilities

## Time: 8 minutes
Let Amazon Q handle the heavy lifting while you focus on integration and testing.