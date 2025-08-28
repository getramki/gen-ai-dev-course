# Exercise 1: Project Setup & Planning (5 minutes)

## Objective
Use Amazon Q Developer to plan and set up a complete full-stack task management application.

## Step 1: Project Architecture Planning
**Prompt Amazon Q:**
```
Create a project architecture for a task management system with:
- Node.js/Express REST API
- React TypeScript frontend
- PostgreSQL database
- JWT authentication
- File structure and technology decisions
```

**Expected Output:**
- Complete project structure
- Technology stack rationale
- Database schema design
- API endpoint planning

## Step 2: Initialize Project Structure
**Prompt Amazon Q:**
```
Generate package.json files and folder structure for:
1. Backend API server with Express, TypeScript, PostgreSQL
2. Frontend React app with TypeScript
3. Shared types and utilities
```

**Tasks:**
1. Create root project directory
2. Set up backend and frontend folders
3. Generate package.json files
4. Configure TypeScript configs

## Step 3: Database Schema Design
**Prompt Amazon Q:**
```
Design PostgreSQL schema for task management with:
- Users table (id, email, password_hash, created_at)
- Tasks table (id, title, description, status, priority, user_id, due_date)
- Include proper indexes and constraints
```

**Expected Files:**
- `database/schema.sql`
- `database/migrations/`
- Database connection configuration

## Step 4: Environment Configuration
**Prompt Amazon Q:**
```
Create environment configuration files for:
- Development, testing, production environments
- Database connection strings
- JWT secrets and API keys
- Docker configuration for local development
```

## Verification Checklist
- [ ] Project structure created
- [ ] Package.json files configured
- [ ] Database schema designed
- [ ] Environment files set up
- [ ] TypeScript configurations ready

## Time: 5 minutes
Focus on getting the foundation right - Amazon Q will help generate the complete structure quickly.