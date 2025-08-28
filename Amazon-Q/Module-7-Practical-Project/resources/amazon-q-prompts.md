# Amazon Q Developer Prompts for Project Integration

## Project Setup Prompts

### Architecture Planning
```
Design a full-stack architecture for a task management application with Node.js backend, React frontend, and PostgreSQL database. Include folder structure, technology stack, and deployment considerations.
```

### Package Configuration
```
Generate package.json files for a monorepo with backend (Express, TypeScript, PostgreSQL) and frontend (React, TypeScript, Tailwind CSS) workspaces.
```

## Backend Development Prompts

### Database Models
```
Create TypeScript models for User and Task entities with:
- User: id, email, password_hash, first_name, last_name, timestamps
- Task: id, title, description, status, priority, user_id, due_date, timestamps
- Include proper relationships and validation
```

### Authentication System
```
Implement JWT authentication system with:
- User registration with password hashing
- Login with email/password
- JWT token generation and validation
- Authentication middleware for protected routes
```

### REST API Endpoints
```
Create RESTful API endpoints for task management:
- GET /api/tasks (with filtering by status, priority, due date)
- POST /api/tasks (create new task)
- PUT /api/tasks/:id (update task)
- DELETE /api/tasks/:id (delete task)
- Include proper validation and error handling
```

## Frontend Development Prompts

### React Components
```
Create React TypeScript components for:
- TaskList with filtering and sorting
- TaskForm for creating/editing tasks
- TaskItem with status updates
- Authentication forms (login/register)
- Protected route wrapper
```

### API Integration
```
Implement API service layer with:
- HTTP client with interceptors
- Authentication token handling
- Error handling and loading states
- React hooks for data fetching
```

## Testing Prompts

### Backend Tests
```
Generate comprehensive test suite for:
- Authentication endpoints (register, login, token validation)
- Task CRUD operations
- Database models and relationships
- Middleware functions
- Error handling scenarios
```

### Frontend Tests
```
Create React component tests using Testing Library for:
- Task list rendering and interactions
- Form submissions and validation
- Authentication flow
- API integration with mocked responses
```

## Security & Quality Prompts

### Security Analysis
```
Perform security analysis and implement:
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Rate limiting
- CORS configuration
- Security headers
```

### Code Quality
```
Review and improve code quality:
- Add TypeScript strict mode
- Implement error boundaries
- Add proper logging
- Optimize database queries
- Add code comments and documentation
```

## Deployment Prompts

### Docker Configuration
```
Create Docker configuration for:
- Backend Node.js application
- Frontend React build
- PostgreSQL database
- Docker Compose for local development
- Multi-stage builds for production
```

### CI/CD Pipeline
```
Generate GitHub Actions workflow for:
- Automated testing on pull requests
- Security scanning
- Build and deployment
- Environment-specific configurations
- Database migrations
```

## Documentation Prompts

### API Documentation
```
Generate OpenAPI/Swagger documentation for all API endpoints including:
- Request/response schemas
- Authentication requirements
- Error responses
- Example requests
```

### Project Documentation
```
Create comprehensive README with:
- Project overview and features
- Setup and installation instructions
- Development workflow
- API usage examples
- Deployment guide
```

## Optimization Prompts

### Performance
```
Optimize application performance:
- Database query optimization
- Frontend bundle size reduction
- Caching strategies
- Lazy loading implementation
- API response optimization
```

### Monitoring
```
Add monitoring and observability:
- Application logging
- Error tracking
- Performance metrics
- Health check endpoints
- Database monitoring
```