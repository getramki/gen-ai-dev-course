# Exercise 2: Natural Language Code Generation

## Objective
Master converting natural language requirements into functional code using Amazon Q.

**Time:** 15 minutes  
**Difficulty:** Intermediate

---

## Exercise Overview

This exercise focuses on using conversational prompts to generate complete, functional code. You'll learn effective prompting techniques and iterative refinement.

---

## Part A: Data Processing Functions (5 minutes)

### Task A1: CSV Data Analysis
**Prompt Amazon Q with:**
```
Create a Python function that reads a CSV file containing employee data (name, department, salary, years_experience), filters employees with more than 5 years experience, and returns the average salary by department
```

**Expected Generated Code Structure:**
- CSV file reading with pandas or csv module
- Data filtering logic
- Grouping by department
- Average calculation
- Error handling for file operations

**Test the Generated Function:**
Create a sample CSV file `employees.csv`:
```csv
name,department,salary,years_experience
John Doe,Engineering,75000,7
Jane Smith,Marketing,65000,4
Bob Johnson,Engineering,85000,10
Alice Brown,Marketing,70000,8
```

### Task A2: JSON Data Transformation
**Prompt Amazon Q with:**
```
Write a Python function that takes a list of product dictionaries with fields (id, name, category, price, stock) and transforms it into a nested structure grouped by category, with each category containing products sorted by price descending
```

**Expected Output Structure:**
```python
{
    "Electronics": [
        {"id": 1, "name": "Laptop", "price": 1200, "stock": 5},
        {"id": 2, "name": "Phone", "price": 800, "stock": 10}
    ],
    "Books": [
        {"id": 3, "name": "Python Guide", "price": 45, "stock": 20}
    ]
}
```

**Test Data:**
```python
products = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 1200, "stock": 5},
    {"id": 2, "name": "Phone", "category": "Electronics", "price": 800, "stock": 10},
    {"id": 3, "name": "Python Guide", "category": "Books", "price": 45, "stock": 20}
]
```

---

## Part B: Algorithm Implementation (5 minutes)

### Task B1: Search Algorithm
**Prompt Amazon Q with:**
```
Implement a binary search algorithm in Python that works with a sorted list of dictionaries, searching by a specified key field, and returns the index of the found item or -1 if not found
```

**Expected Features:**
- Generic binary search implementation
- Dictionary key-based comparison
- Proper boundary handling
- Index return or -1 for not found

**Test Case:**
```python
data = [
    {"id": 1, "name": "Alice"},
    {"id": 3, "name": "Bob"},
    {"id": 5, "name": "Charlie"},
    {"id": 7, "name": "David"}
]
# Search for id=5 should return index 2
```

### Task B2: Sorting with Custom Logic
**Prompt Amazon Q with:**
```
Create a Python function that sorts a list of student dictionaries first by grade (descending), then by name (ascending), and handles missing grade values by treating them as 0
```

**Test Data:**
```python
students = [
    {"name": "John", "grade": 85},
    {"name": "Alice", "grade": 92},
    {"name": "Bob"},  # Missing grade
    {"name": "Carol", "grade": 85}
]
```

---

## Part C: Class and Object Generation (5 minutes)

### Task C1: Data Validation Class
**Prompt Amazon Q with:**
```
Generate a Python class called UserValidator that validates user registration data with methods to check email format using regex, password strength (minimum 8 characters, at least one uppercase, one lowercase, one digit), and age range (18-120), returning detailed error messages for each validation failure
```

**Expected Class Structure:**
- Email validation with regex
- Password complexity checking
- Age boundary validation
- Detailed error messaging
- Main validation method combining all checks

**Test Cases:**
```python
validator = UserValidator()
# Test valid data
result = validator.validate({
    "email": "user@example.com",
    "password": "SecurePass123",
    "age": 25
})

# Test invalid data
result = validator.validate({
    "email": "invalid-email",
    "password": "weak",
    "age": 15
})
```

### Task C2: Configuration Manager
**Prompt Amazon Q with:**
```
Create a Python class ConfigManager that loads configuration from JSON files, provides get/set methods with dot notation support (e.g., get('database.host')), validates required fields, and saves changes back to file with proper error handling
```

**Expected Features:**
- JSON file loading/saving
- Dot notation path traversal
- Required field validation
- Error handling for file operations
- Configuration update persistence

---

## Prompt Optimization Techniques

### Effective Prompt Structure

**Basic Pattern:**
```
[Action] a [Language] [Component] that [Functionality] with [Specific Requirements]
```

**Examples:**
- "Create a Python function that processes CSV data with error handling"
- "Write a JavaScript class for user authentication with JWT tokens"
- "Generate a Java method that validates email addresses using regex"

### Specificity Levels

**Level 1 - Basic:**
```
Create a sorting function
```

**Level 2 - Better:**
```
Create a Python function to sort a list of dictionaries
```

**Level 3 - Best:**
```
Create a Python function to sort a list of user dictionaries by age descending, then by name ascending, with null age handling
```

### Adding Context

**Include:**
- Expected input/output formats
- Error handling requirements
- Performance considerations
- Specific libraries or patterns
- Edge case handling

**Example:**
```
Create a Python function using pandas that reads a large CSV file (>1GB), processes it in chunks to avoid memory issues, filters rows based on multiple conditions, and exports results to a new CSV with progress tracking
```

---

## Iterative Refinement Process

### Step 1: Initial Generation
Start with a clear, specific prompt and generate the base code.

### Step 2: Review and Test
- Run the generated code
- Test with sample data
- Identify missing features or bugs

### Step 3: Refinement Prompts
**Examples:**
```
Add error handling for file not found
Add input validation for the parameters
Optimize the algorithm for better performance
Add logging to track processing steps
```

### Step 4: Integration
Combine refined pieces into final solution.

---

## Quality Assessment Checklist

### Generated Code Should Include:

**Functionality:**
- [ ] Meets all specified requirements
- [ ] Handles expected input formats
- [ ] Produces correct output
- [ ] Includes edge case handling

**Code Quality:**
- [ ] Proper error handling
- [ ] Clear variable names
- [ ] Appropriate comments
- [ ] Follows language conventions

**Robustness:**
- [ ] Input validation
- [ ] Graceful error recovery
- [ ] Resource cleanup
- [ ] Performance considerations

---

## Common Generation Patterns

### Data Processing
```
"Process [data type] from [source] and [transformation] with [output format]"
```

### Algorithm Implementation
```
"Implement [algorithm name] for [data structure] with [specific requirements]"
```

### Class Generation
```
"Create a [class name] class that [primary function] with methods for [specific operations]"
```

### API/Service Generation
```
"Build a [service type] that handles [operations] with [protocols/formats]"
```

---

## Troubleshooting Generation Issues

### Incomplete Code
**Problem:** Generated code is missing key functionality
**Solution:** Add more specific requirements in follow-up prompts

### Incorrect Logic
**Problem:** Code doesn't match requirements
**Solution:** Provide example input/output in the prompt

### Poor Error Handling
**Problem:** No validation or error checking
**Solution:** Explicitly request error handling and validation

### Performance Issues
**Problem:** Inefficient algorithms or memory usage
**Solution:** Specify performance requirements and constraints

---

## Success Criteria

You've mastered natural language code generation when:
- [ ] Can write effective, specific prompts
- [ ] Generate functionally correct code consistently
- [ ] Know how to refine and improve generated code
- [ ] Understand when to break complex requirements into smaller prompts
- [ ] Can combine multiple generated pieces into complete solutions

**Completion Time:** 15 minutes  
**Next:** Module 3 - Code Understanding and Documentation