# Module 5: Security and Best Practices

**Duration:** 15 minutes  
**Objective:** Master Amazon Q's security analysis and code quality improvement capabilities

---

## Topic 5.1: Security Analysis (8 minutes)

### Understanding Security Analysis

Amazon Q can identify and help fix:
- **Input Validation Issues:** SQL injection, XSS, command injection
- **Authentication Flaws:** Weak passwords, insecure sessions, missing authorization
- **Data Exposure:** Sensitive data leaks, improper encryption, logging secrets
- **Configuration Issues:** Default credentials, insecure settings, exposed endpoints
- **Dependency Vulnerabilities:** Outdated packages, known CVEs

### Security Vulnerability Categories

#### Injection Attacks
```python
# Vulnerable to SQL injection
def get_user_by_id(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute_query(query)

# Amazon Q suggests:
def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = ?"
    return execute_query(query, (user_id,))
```

#### Cross-Site Scripting (XSS)
```python
# Vulnerable to XSS
def display_user_comment(comment):
    return f"<div>{comment}</div>"

# Amazon Q suggests:
import html
def display_user_comment(comment):
    escaped_comment = html.escape(comment)
    return f"<div>{escaped_comment}</div>"
```

#### Insecure Authentication
```python
# Weak authentication
def authenticate_user(username, password):
    user = get_user(username)
    return user.password == password

# Amazon Q suggests:
import bcrypt
def authenticate_user(username, password):
    user = get_user(username)
    return bcrypt.checkpw(password.encode('utf-8'), user.password_hash)
```

### Security Best Practices

#### Input Validation
- Validate all user inputs
- Use allowlists over denylists
- Implement proper data type checking
- Sanitize data before processing

#### Authentication & Authorization
- Use strong password policies
- Implement multi-factor authentication
- Apply principle of least privilege
- Secure session management

#### Data Protection
- Encrypt sensitive data at rest and in transit
- Use secure random number generation
- Implement proper key management
- Avoid logging sensitive information

#### Secure Configuration
- Change default credentials
- Disable unnecessary services
- Use HTTPS everywhere
- Implement proper error handling

### Amazon Q Security Prompts

#### Vulnerability Detection
```
"Analyze this code for security vulnerabilities"
"Check for SQL injection risks in this function"
"Identify potential XSS vulnerabilities"
"Review authentication implementation for security flaws"
```

#### Security Improvements
```
"Add input validation to prevent injection attacks"
"Implement secure password hashing"
"Add proper error handling without information disclosure"
"Suggest security headers for this web application"
```

---

## Topic 5.2: Code Quality Improvements (7 minutes)

### Code Quality Dimensions

#### Readability
- Clear naming conventions
- Consistent formatting
- Appropriate comments
- Logical code organization

#### Maintainability
- Modular design
- Low coupling, high cohesion
- Proper error handling
- Comprehensive testing

#### Performance
- Efficient algorithms
- Proper resource management
- Caching strategies
- Database optimization

#### Reliability
- Input validation
- Error recovery
- Graceful degradation
- Monitoring and logging

### Code Quality Patterns

#### Clean Code Principles
```python
# Poor quality
def calc(x, y, z):
    if z == 1:
        return x + y
    elif z == 2:
        return x - y
    else:
        return x * y

# Amazon Q suggests:
def calculate_result(operand1, operand2, operation_type):
    """Calculate result based on operation type.
    
    Args:
        operand1: First number
        operand2: Second number
        operation_type: 1=add, 2=subtract, 3=multiply
    
    Returns:
        Calculated result
    
    Raises:
        ValueError: If operation_type is invalid
    """
    operations = {
        1: lambda x, y: x + y,
        2: lambda x, y: x - y,
        3: lambda x, y: x * y
    }
    
    if operation_type not in operations:
        raise ValueError(f"Invalid operation type: {operation_type}")
    
    return operations[operation_type](operand1, operand2)
```

#### Error Handling Improvements
```python
# Poor error handling
def process_file(filename):
    f = open(filename)
    data = f.read()
    return data.upper()

# Amazon Q suggests:
def process_file(filename):
    """Process file content safely with proper error handling."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        return data.upper()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {filename}")
    except UnicodeDecodeError:
        raise ValueError(f"Invalid file encoding: {filename}")
```

### Testing and Validation

#### Unit Testing
```python
# Amazon Q can generate comprehensive tests
def test_calculate_result():
    """Test calculate_result function with various inputs."""
    # Test addition
    assert calculate_result(5, 3, 1) == 8
    
    # Test subtraction
    assert calculate_result(5, 3, 2) == 2
    
    # Test multiplication
    assert calculate_result(5, 3, 3) == 15
    
    # Test invalid operation
    with pytest.raises(ValueError):
        calculate_result(5, 3, 4)
```

#### Code Coverage
```
"Generate unit tests to achieve 90% code coverage"
"Add edge case tests for this function"
"Create integration tests for this API endpoint"
```

---

## Hands-On Exercise 5.1: Security Vulnerability Assessment

### Objective
Identify and fix security vulnerabilities using Amazon Q's security analysis.

### Task 1: Web Application Security (4 minutes)

**Create file:** `vulnerable_webapp.py`
```python
from flask import Flask, request, render_template_string, session
import sqlite3
import os
import subprocess

app = Flask(__name__)
app.secret_key = "secret"  # Hardcoded secret key

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    result = cursor.execute(query).fetchone()
    
    if result:
        session['user_id'] = result[0]
        return "Login successful"
    return "Login failed"

@app.route('/profile')
def profile():
    # Missing authentication check
    user_id = session.get('user_id')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    user = cursor.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
    
    return f"Welcome {user[1]}"

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # XSS vulnerability
    template = f"<h1>Search Results for: {query}</h1>"
    return render_template_string(template)

@app.route('/admin/execute')
def execute_command():
    # Command injection vulnerability
    cmd = request.args.get('cmd', 'ls')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return f"<pre>{result.stdout}</pre>"

@app.route('/file')
def read_file():
    # Path traversal vulnerability
    filename = request.args.get('file', 'default.txt')
    filepath = os.path.join('/app/files/', filename)
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except:
        return "File not found"

@app.route('/api/users/<user_id>')
def get_user_api(user_id):
    # Information disclosure
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        user = cursor.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
        
        return {
            'id': user[0],
            'username': user[1],
            'password': user[2],  # Exposing password
            'email': user[3],
            'ssn': user[4]  # Exposing SSN
        }
    except Exception as e:
        return {'error': str(e)}  # Information disclosure through errors
```

**Amazon Q Security Analysis Tasks:**

1. **Comprehensive Security Review:**
```
@vulnerable_webapp.py Perform a comprehensive security analysis of this web application and identify all vulnerabilities
```

2. **Specific Vulnerability Types:**
```
Identify SQL injection vulnerabilities in this code and suggest fixes
```

```
Find XSS vulnerabilities and recommend proper input sanitization
```

```
Check for authentication and authorization issues
```

```
Identify information disclosure problems and suggest remediation
```

### Task 2: API Security Issues (4 minutes)

**Create file:** `insecure_api.py`
```python
import jwt
import hashlib
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

# Insecure configurations
JWT_SECRET = "weak_secret"
ADMIN_PASSWORD = "admin123"

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # No input validation
    username = data['username']
    password = data['password']
    email = data['email']
    
    # Weak password hashing
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    # Store user (simulated)
    user_id = save_user(username, password_hash, email)
    
    return jsonify({'user_id': user_id, 'message': 'User created'})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Simulate user lookup
    user = get_user_by_username(username)
    
    if user and user['password'] == hashlib.md5(password.encode()).hexdigest():
        # Insecure JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'username': user['username'],
            'is_admin': user.get('is_admin', False),
            'exp': datetime.utcnow() + timedelta(days=365)  # Long expiration
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    # No authentication check
    users = get_all_users()
    
    # Returns sensitive data
    return jsonify(users)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    
    # No file type validation
    # No file size limits
    filename = file.filename
    file.save(f'/uploads/{filename}')  # Path traversal possible
    
    return jsonify({'message': 'File uploaded', 'filename': filename})

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    
    # Generate reset token
    reset_token = hashlib.md5(f"{email}{datetime.now()}".encode()).hexdigest()
    
    # Send reset email (simulated)
    send_reset_email(email, reset_token)
    
    # Information disclosure
    return jsonify({
        'message': 'Reset email sent',
        'reset_token': reset_token,  # Exposing token
        'user_exists': user_exists(email)  # User enumeration
    })

def get_user_by_username(username):
    # Simulated database lookup
    return {'id': 1, 'username': username, 'password': 'hashed_password'}

def save_user(username, password_hash, email):
    # Simulated user creation
    return 123

def get_all_users():
    # Returns all user data including sensitive info
    return [
        {'id': 1, 'username': 'admin', 'password': 'hash', 'ssn': '123-45-6789'},
        {'id': 2, 'username': 'user', 'password': 'hash', 'email': 'user@example.com'}
    ]

def user_exists(email):
    # Simulated user existence check
    return True

def send_reset_email(email, token):
    # Simulated email sending
    pass
```

**Amazon Q API Security Tasks:**
```
@insecure_api.py Analyze this API for security vulnerabilities and suggest comprehensive fixes
```

```
Identify authentication and authorization weaknesses in this API
```

```
Review password handling and suggest secure alternatives
```

```
Check for information disclosure issues and recommend fixes
```

---

## Hands-On Exercise 5.2: Code Quality Enhancement

### Objective
Improve code quality using Amazon Q's best practices recommendations.

### Task 1: Code Refactoring (3 minutes)

**Create file:** `poor_quality_code.py`
```python
import json
import requests

def process_data(data):
    result = []
    for item in data:
        if item['type'] == 'A':
            processed = item['value'] * 2
        elif item['type'] == 'B':
            processed = item['value'] + 10
        elif item['type'] == 'C':
            processed = item['value'] / 2
        else:
            processed = item['value']
        
        if processed > 100:
            status = 'high'
        elif processed > 50:
            status = 'medium'
        else:
            status = 'low'
        
        result.append({
            'id': item['id'],
            'processed_value': processed,
            'status': status
        })
    
    return result

def fetch_user_data(user_ids):
    users = []
    for user_id in user_ids:
        try:
            response = requests.get(f'https://api.example.com/users/{user_id}')
            if response.status_code == 200:
                user_data = response.json()
                users.append(user_data)
        except:
            pass
    return users

def calculate_stats(numbers):
    total = 0
    count = 0
    max_val = numbers[0]
    min_val = numbers[0]
    
    for num in numbers:
        total += num
        count += 1
        if num > max_val:
            max_val = num
        if num < min_val:
            min_val = num
    
    avg = total / count
    
    return {
        'total': total,
        'count': count,
        'average': avg,
        'maximum': max_val,
        'minimum': min_val
    }

class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, name, email, age):
        user = {
            'id': len(self.users) + 1,
            'name': name,
            'email': email,
            'age': age
        }
        self.users.append(user)
        return user
    
    def get_user(self, user_id):
        for user in self.users:
            if user['id'] == user_id:
                return user
        return None
    
    def update_user(self, user_id, name=None, email=None, age=None):
        user = self.get_user(user_id)
        if user:
            if name:
                user['name'] = name
            if email:
                user['email'] = email
            if age:
                user['age'] = age
        return user
    
    def delete_user(self, user_id):
        for i, user in enumerate(self.users):
            if user['id'] == user_id:
                del self.users[i]
                return True
        return False
```

**Amazon Q Quality Improvement Tasks:**

1. **Code Structure and Design:**
```
@poor_quality_code.py Refactor this code to improve readability, maintainability, and follow best practices
```

2. **Error Handling:**
```
Add proper error handling and input validation to all functions
```

3. **Performance Optimization:**
```
Identify performance issues and suggest optimizations
```

4. **Design Patterns:**
```
Apply appropriate design patterns to improve code structure
```

### Task 2: Testing and Documentation (4 minutes)

**Amazon Q Tasks for Enhanced Code:**

1. **Generate Unit Tests:**
```
Generate comprehensive unit tests for the refactored code with edge cases and error conditions
```

2. **Add Documentation:**
```
Add comprehensive docstrings and type hints to all functions and classes
```

3. **Code Review Checklist:**
```
Create a code review checklist based on the improvements made to this code
```

---

## Security Best Practices Checklist

### Input Validation
- [ ] Validate all user inputs
- [ ] Use parameterized queries
- [ ] Implement proper data type checking
- [ ] Sanitize output data

### Authentication & Authorization
- [ ] Use strong password policies
- [ ] Implement secure session management
- [ ] Apply principle of least privilege
- [ ] Add multi-factor authentication

### Data Protection
- [ ] Encrypt sensitive data
- [ ] Use secure random generation
- [ ] Implement proper key management
- [ ] Avoid logging secrets

### Error Handling
- [ ] Don't expose sensitive information in errors
- [ ] Log security events
- [ ] Implement graceful error recovery
- [ ] Use generic error messages for users

### Configuration Security
- [ ] Change default credentials
- [ ] Use environment variables for secrets
- [ ] Implement security headers
- [ ] Regular security updates

---

## Code Quality Standards

### Readability
- [ ] Clear and descriptive naming
- [ ] Consistent code formatting
- [ ] Appropriate comments and documentation
- [ ] Logical code organization

### Maintainability
- [ ] Modular design with single responsibility
- [ ] Low coupling between components
- [ ] High cohesion within modules
- [ ] Comprehensive error handling

### Testing
- [ ] Unit tests with good coverage
- [ ] Integration tests for workflows
- [ ] Edge case and error condition tests
- [ ] Performance and security tests

### Performance
- [ ] Efficient algorithms and data structures
- [ ] Proper resource management
- [ ] Appropriate caching strategies
- [ ] Database query optimization

---

## Key Takeaways

After Module 5, you should be able to:
- Identify and fix common security vulnerabilities
- Apply security best practices in code development
- Improve code quality through refactoring
- Generate comprehensive tests and documentation
- Implement proper error handling and validation
- Use Amazon Q for security analysis and code review

**Time Required:** 15 minutes  
**Difficulty:** Intermediate to Advanced  
**Next:** Module 6 - Advanced Features and Integration