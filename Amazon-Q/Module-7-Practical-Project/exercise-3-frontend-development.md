# Exercise 3: Frontend Development (4 minutes)

## Objective
Build a React TypeScript frontend using Amazon Q Developer for component generation and API integration.

## Step 1: Project Setup & Routing (1 minute)
**Prompt Amazon Q:**
```
Create React TypeScript app with:
- React Router for navigation
- Authentication context
- API service layer
- Tailwind CSS for styling
- Component structure for task management
```

**Generate:**
- `src/App.tsx`
- `src/components/`
- `src/services/api.ts`
- `src/contexts/AuthContext.tsx`

## Step 2: Authentication Components (1 minute)
**Prompt Amazon Q:**
```
Create authentication components:
- Login form with validation
- Register form
- Protected route wrapper
- User profile component
- Logout functionality
```

**Generate:**
- `src/components/auth/LoginForm.tsx`
- `src/components/auth/RegisterForm.tsx`
- `src/components/auth/ProtectedRoute.tsx`

## Step 3: Task Management Interface (1.5 minutes)
**Prompt Amazon Q:**
```
Create task management components:
- Task list with filtering and sorting
- Task creation form
- Task edit modal
- Task status updates
- Priority indicators
- Due date handling
```

**Generate:**
- `src/components/tasks/TaskList.tsx`
- `src/components/tasks/TaskForm.tsx`
- `src/components/tasks/TaskItem.tsx`
- `src/components/tasks/TaskFilters.tsx`

## Step 4: API Integration & State Management (0.5 minutes)
**Prompt Amazon Q:**
```
Implement API integration:
- HTTP client with interceptors
- Error handling and loading states
- Local state management with React hooks
- Optimistic updates for better UX
```

**Generate:**
- `src/hooks/useTasks.ts`
- `src/hooks/useAuth.ts`
- `src/services/taskService.ts`

## Key Components Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   ├── tasks/
│   │   └── common/
│   ├── hooks/
│   ├── services/
│   ├── contexts/
│   └── types/
├── package.json
└── tsconfig.json
```

## Amazon Q Prompts for Quick Generation
1. **Component Generation:**
   ```
   Create a React component for [specific functionality] with TypeScript and proper props interface
   ```

2. **API Integration:**
   ```
   Add API calls to this component for [specific operations] with error handling
   ```

3. **Styling:**
   ```
   Add Tailwind CSS classes for responsive design and modern UI
   ```

## Verification Checklist
- [ ] Authentication flow working
- [ ] Task CRUD operations functional
- [ ] Responsive design implemented
- [ ] Error handling in place
- [ ] TypeScript types properly defined
- [ ] API integration complete

## Time: 4 minutes
Use Amazon Q's component generation to rapidly build the interface while maintaining code quality.