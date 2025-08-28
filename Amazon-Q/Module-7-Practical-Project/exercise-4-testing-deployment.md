# Exercise 4: Testing & Deployment (3 minutes)

## Objective
Complete the project with comprehensive testing, documentation, and deployment configuration using Amazon Q Developer.

## Step 1: Test Suite Creation (1.5 minutes)
**Prompt Amazon Q:**
```
Generate comprehensive test suite:
- Backend API tests with Jest and Supertest
- Frontend component tests with React Testing Library
- Integration tests for API endpoints
- E2E tests with Playwright
- Test data factories and mocks
```

**Generate Tests:**
- `backend/tests/auth.test.ts`
- `backend/tests/tasks.test.ts`
- `frontend/src/__tests__/`
- `e2e/tests/`

**Run Tests with Amazon Q:**
1. Execute test suites
2. Debug failing tests
3. Improve test coverage

## Step 2: Documentation Generation (0.5 minutes)
**Prompt Amazon Q:**
```
Generate project documentation:
- API documentation with OpenAPI/Swagger
- README with setup instructions
- Code comments and JSDoc
- Architecture documentation
- Deployment guide
```

**Generate:**
- `README.md`
- `docs/api.md`
- `docs/architecture.md`
- `swagger.yaml`

## Step 3: CI/CD Pipeline Setup (1 minute)
**Prompt Amazon Q:**
```
Create CI/CD pipeline configuration:
- GitHub Actions workflow
- Docker containers for backend and frontend
- Environment-specific deployments
- Automated testing and security scans
- Database migration scripts
```

**Generate:**
- `.github/workflows/ci.yml`
- `Dockerfile` (backend and frontend)
- `docker-compose.yml`
- `deploy/`

## Final Project Structure
```
task-management-app/
├── backend/
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── package.json
├── frontend/
│   ├── src/
│   ├── __tests__/
│   ├── Dockerfile
│   └── package.json
├── e2e/
├── docs/
├── .github/workflows/
├── docker-compose.yml
└── README.md
```

## Amazon Q Commands for Final Steps

### Testing
```
# Generate test for this function
# Fix failing test in [file]
# Add integration test for API endpoint
# Create mock data for testing
```

### Documentation
```
# Generate API documentation for these endpoints
# Create README with setup instructions
# Add JSDoc comments to this code
# Document the database schema
```

### Deployment
```
# Create Dockerfile for Node.js app
# Generate GitHub Actions workflow
# Set up environment variables for production
# Create database migration script
```

## Verification Checklist
- [ ] All tests passing (unit, integration, e2e)
- [ ] Code coverage > 80%
- [ ] API documentation complete
- [ ] Docker containers working
- [ ] CI/CD pipeline functional
- [ ] Security scans passing
- [ ] Performance optimized
- [ ] Production-ready configuration

## Final Amazon Q Security & Quality Check
1. Run comprehensive security scan
2. Check code quality metrics
3. Optimize performance bottlenecks
4. Validate deployment configuration

## Time: 3 minutes
Use Amazon Q to automate testing, documentation, and deployment setup for a production-ready application.

## 🎉 Congratulations!
You've successfully built a complete full-stack application using Amazon Q Developer, demonstrating mastery of all course concepts!