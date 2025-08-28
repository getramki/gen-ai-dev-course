# Module 2: Code Generation and Completion

**Duration:** 30 minutes  
**Objective:** Master Amazon Q's intelligent code completion and natural language code generation

---

## Topic 2.1: Intelligent Code Completion (15 minutes)

### Understanding Auto-Completion

Amazon Q provides context-aware code suggestions that:
- Analyze your current code context
- Suggest complete functions, classes, and code blocks
- Adapt to your coding style and patterns
- Support multiple programming languages

### Types of Completions

#### Single-Line Completions
- Variable assignments
- Function calls
- Import statements
- Simple expressions

#### Multi-Line Completions
- Complete function implementations
- Class definitions with methods
- Loop structures with logic
- Error handling blocks

#### Context-Aware Suggestions
- Based on existing code patterns
- Considers variable names and types
- Follows project conventions
- Integrates with existing functions

### Triggering Completions

#### Automatic Triggers
- Start typing function names
- After opening parentheses or brackets
- When defining new functions or classes
- After comment descriptions

#### Manual Triggers
- **Alt+C** (Windows/Linux) or **Option+C** (Mac)
- Pause typing for 1-2 seconds
- Use in any code context

### Best Practices for Completions

1. **Write descriptive comments** before functions
2. **Use meaningful variable names** for better context
3. **Accept suggestions with Tab** key
4. **Reject with Escape** if not suitable
5. **Partial acceptance** with Ctrl+Right Arrow

---

## Topic 2.2: Code Generation from Natural Language (15 minutes)

### Natural Language Prompting

Transform requirements into code using conversational descriptions:

#### Effective Prompt Patterns
```
"Create a [language] function that [specific action]"
"Write a [type] class for [purpose] with [features]"
"Generate [algorithm] implementation for [problem]"
"Build a [component] that handles [functionality]"
```

#### Specificity Levels
- **Basic:** "Create a sorting function"
- **Better:** "Create a Python function to sort a list of dictionaries"
- **Best:** "Create a Python function to sort a list of user dictionaries by age, then by name"

### Code Generation Capabilities

#### Functions and Methods
- Algorithm implementations
- Data processing functions
- Utility methods
- API endpoints

#### Classes and Objects
- Data models
- Service classes
- Design pattern implementations
- Custom data structures

#### Complete Applications
- REST API servers
- CLI tools
- Data processing scripts
- Web components

### Language-Specific Features

#### Python
- Type hints and docstrings
- Exception handling
- List comprehensions
- Context managers

#### JavaScript/TypeScript
- Async/await patterns
- ES6+ features
- Type definitions
- React components

#### Java
- Annotations and generics
- Exception handling
- Stream API usage
- Spring Boot patterns

---

## Hands-On Exercise 2.1: REST API with Auto-Completion

### Objective
Build a complete REST API using Amazon Q's intelligent completions.

### Setup
Create a new file: `user_api.py`

### Step 1: Basic Structure (5 minutes)
Start typing and use completions:

```python
# Create a Flask REST API for user management
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user storage
users = []
```

**Try this:** After typing the comment, start typing `@app.route` and accept Amazon Q's suggestions.

### Step 2: CRUD Operations (10 minutes)
Use completions to build endpoints:

1. **Create User Endpoint**
   - Type: `# POST endpoint to create a new user`
   - Start typing: `@app.route('/users', methods=['POST'])`
   - Accept completions for the function

2. **Get Users Endpoint**
   - Type: `# GET endpoint to retrieve all users`
   - Let Amazon Q complete the implementation

3. **Update User Endpoint**
   - Type: `# PUT endpoint to update user by ID`
   - Use completions for parameter handling

4. **Delete User Endpoint**
   - Type: `# DELETE endpoint to remove user by ID`
   - Accept suggested error handling

### Expected Completion Behavior
- Amazon Q should suggest complete function implementations
- Error handling should be included automatically
- JSON response formatting should be suggested
- HTTP status codes should be appropriate

---

## Hands-On Exercise 2.2: Data Processing Functions

### Objective
Generate complex data processing functions using natural language descriptions.

### Setup
Create a new file: `data_processor.py`

### Task 1: CSV Data Processing (5 minutes)
**Prompt Amazon Q:**
```
Create a Python function that reads a CSV file, filters rows where age > 25, and returns the average salary of filtered records
```

**Expected Output:**
- Function with proper CSV handling
- Age filtering logic
- Salary calculation
- Error handling for file operations

### Task 2: JSON Data Transformation (5 minutes)
**Prompt Amazon Q:**
```
Write a function that takes a list of user dictionaries and transforms them into a nested structure grouped by department and role
```

**Expected Output:**
- Nested dictionary creation
- Grouping logic
- Proper data structure handling

### Task 3: Data Validation (5 minutes)
**Prompt Amazon Q:**
```
Generate a Python class that validates user data with email format checking, password strength validation, and age range verification
```

**Expected Output:**
- Class with validation methods
- Regular expressions for email
- Password complexity rules
- Age boundary checks

---

## Advanced Completion Techniques

### Context Building
1. **Write descriptive comments** above code blocks
2. **Use consistent naming conventions**
3. **Import relevant libraries first**
4. **Define data structures early**

### Iterative Refinement
1. **Accept initial suggestion**
2. **Ask for modifications** in chat
3. **Use follow-up completions**
4. **Combine multiple suggestions**

### Multi-File Context
- Amazon Q considers other open files
- Maintains consistency across project
- Suggests imports from existing modules
- Follows established patterns

---

## Quality Assessment

### Good Completions Include
- ✅ Proper error handling
- ✅ Appropriate data types
- ✅ Consistent naming
- ✅ Relevant comments
- ✅ Language best practices

### When to Refine
- ❌ Logic doesn't match requirements
- ❌ Missing error handling
- ❌ Inefficient algorithms
- ❌ Security vulnerabilities
- ❌ Poor code structure

---

## Troubleshooting Completions

### No Suggestions Appearing
1. Check Amazon Q connection status
2. Try manual trigger (Alt+C/Option+C)
3. Ensure cursor is in appropriate position
4. Restart IDE if persistent

### Poor Quality Suggestions
1. Add more context in comments
2. Use more descriptive variable names
3. Import relevant libraries
4. Provide example data structures

### Incomplete Suggestions
1. Accept partial completion
2. Continue typing to trigger more
3. Use chat for complex requirements
4. Break down into smaller functions

---

## Key Takeaways

After Module 2, you should be able to:
- Effectively use Amazon Q's auto-completion features
- Generate code from natural language descriptions
- Build complete applications with minimal manual coding
- Understand when and how to refine AI suggestions
- Leverage context for better code generation

**Time Required:** 30 minutes  
**Difficulty:** Intermediate  
**Next:** Module 3 - Code Understanding and Documentation