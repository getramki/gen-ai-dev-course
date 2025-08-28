# Exercise 1: Security Vulnerability Assessment

## Objective
Master Amazon Q's security analysis capabilities by identifying and fixing real-world vulnerabilities.

**Time:** 8 minutes  
**Difficulty:** Intermediate to Advanced

---

## Setup Instructions

### Create Security Assessment Workspace
```bash
mkdir security-assessment
cd security-assessment
```

---

## Part A: Web Application Security Vulnerabilities (4 minutes)

### Task A1: Authentication and Session Security

**Create file:** `auth_vulnerabilities.py`
```python
from flask import Flask, request, session, redirect, url_for
import hashlib
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mysecret"  # Hardcoded secret key

# Global admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vulnerable SQL query - SQL Injection
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT id, username, password FROM users WHERE username = '{username}'"
        result = cursor.execute(query).fetchone()
        
        if result:
            stored_password = result[2]
            # Weak password comparison - timing attack vulnerable
            if password == stored_password:
                session['user_id'] = result[0]
                session['username'] = result[1]
                return redirect(url_for('dashboard'))
        
        # Information disclosure
        return f"Login failed for user: {username}"
    
    return '''
    <form method="post">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    '''

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    # Weak password hashing
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    # No input validation
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    try:
        # SQL Injection vulnerability
        cursor.execute(f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password_hash}', '{email}')")
        conn.commit()
        return "User registered successfully"
    except Exception as e:
        # Information disclosure through error messages
        return f"Registration failed: {str(e)}"

@app.route('/dashboard')
def dashboard():
    # Missing authentication check
    username = session.get('username', 'Guest')
    return f"Welcome to dashboard, {username}!"

@app.route('/admin')
def admin_panel():
    # Weak authorization check
    if session.get('username') == ADMIN_USERNAME:
        return "Admin panel - sensitive operations available"
    return "Access denied"

@app.route('/change_password', methods=['POST'])
def change_password():
    # No CSRF protection
    user_id = session.get('user_id')
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    
    # No password strength validation
    if len(new_password) < 3:
        return "Password too short"
    
    # Update password without verifying old password properly
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Weak password hashing
    new_hash = hashlib.md5(new_password.encode()).hexdigest()
    cursor.execute(f"UPDATE users SET password = '{new_hash}' WHERE id = {user_id}")
    conn.commit()
    
    return "Password changed successfully"

@app.route('/reset_password')
def reset_password():
    email = request.args.get('email')
    
    # User enumeration vulnerability
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    user = cursor.execute(f"SELECT id FROM users WHERE email = '{email}'").fetchone()
    
    if user:
        # Predictable reset token
        reset_token = hashlib.md5(f"{email}{datetime.now().date()}".encode()).hexdigest()
        return f"Reset token sent to {email}. Token: {reset_token}"
    else:
        return f"No user found with email: {email}"
```

**Amazon Q Security Analysis Tasks:**

1. **Authentication Vulnerabilities:**
```
@auth_vulnerabilities.py Identify all authentication and session security vulnerabilities in this code
```

2. **SQL Injection Analysis:**
```
Find all SQL injection vulnerabilities and suggest parameterized query fixes
```

3. **Password Security Issues:**
```
Analyze password handling security issues and recommend secure alternatives
```

4. **Session Management Problems:**
```
Identify session management vulnerabilities and suggest improvements
```

**Expected Vulnerabilities to Find:**
- Hardcoded secret key
- SQL injection in login and register
- Weak MD5 password hashing
- Missing authentication checks
- Information disclosure in error messages
- User enumeration in password reset
- No CSRF protection
- Predictable reset tokens
- Timing attack vulnerability

### Task A2: Input Validation and XSS Prevention

**Create file:** `input_validation_issues.py`
```python
from flask import Flask, request, render_template_string, jsonify
import subprocess
import os
import pickle
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # XSS vulnerability - unescaped user input
    template = f"""
    <html>
        <body>
            <h1>Search Results for: {query}</h1>
            <p>You searched for: {query}</p>
        </body>
    </html>
    """
    return render_template_string(template)

@app.route('/comment', methods=['POST'])
def add_comment():
    comment = request.form['comment']
    author = request.form['author']
    
    # Stored XSS vulnerability
    html_comment = f"""
    <div class="comment">
        <strong>{author}</strong>: {comment}
    </div>
    """
    
    # Save to file (simulated)
    with open('comments.html', 'a') as f:
        f.write(html_comment)
    
    return "Comment added successfully"

@app.route('/execute')
def execute_command():
    # Command injection vulnerability
    cmd = request.args.get('cmd', 'ls')
    
    # Dangerous: direct command execution
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    return f"<pre>Command: {cmd}\nOutput:\n{result.stdout}\nErrors:\n{result.stderr}</pre>"

@app.route('/file')
def read_file():
    # Path traversal vulnerability
    filename = request.args.get('file', 'default.txt')
    
    # No path validation
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded"
    
    file = request.files['file']
    filename = file.filename
    
    # No file type validation
    # No file size limits
    # Directory traversal possible
    upload_path = os.path.join('/uploads/', filename)
    file.save(upload_path)
    
    return f"File {filename} uploaded successfully"

@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    # Insecure deserialization
    data = request.get_data()
    
    try:
        # Dangerous: pickle deserialization of user data
        obj = pickle.loads(data)
        return f"Deserialized object: {obj}"
    except Exception as e:
        return f"Deserialization error: {str(e)}"

@app.route('/xml_parse', methods=['POST'])
def parse_xml():
    xml_data = request.get_data()
    
    # XXE vulnerability - XML External Entity
    try:
        root = ET.fromstring(xml_data)
        return f"XML parsed successfully: {root.tag}"
    except Exception as e:
        return f"XML parsing error: {str(e)}"

@app.route('/redirect')
def redirect_user():
    # Open redirect vulnerability
    url = request.args.get('url', '/')
    return f'<script>window.location.href="{url}";</script>'

@app.route('/api/eval', methods=['POST'])
def evaluate_expression():
    # Code injection vulnerability
    expression = request.json.get('expression', '1+1')
    
    try:
        # Extremely dangerous: eval of user input
        result = eval(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})
```

**Amazon Q Input Validation Tasks:**

1. **XSS Vulnerability Analysis:**
```
@input_validation_issues.py Identify all XSS vulnerabilities and suggest proper input sanitization
```

2. **Injection Attack Prevention:**
```
Find command injection and code injection vulnerabilities. How should these be fixed?
```

3. **File Upload Security:**
```
Analyze file upload security issues and recommend secure file handling practices
```

4. **Deserialization Vulnerabilities:**
```
Identify insecure deserialization issues and suggest safe alternatives
```

**Expected Vulnerabilities:**
- Reflected XSS in search function
- Stored XSS in comment system
- Command injection in execute endpoint
- Path traversal in file reading
- Unrestricted file upload
- Insecure pickle deserialization
- XXE vulnerability in XML parsing
- Open redirect vulnerability
- Code injection via eval()

---

## Part B: API Security Assessment (4 minutes)

### Task B1: REST API Security Issues

**Create file:** `insecure_api.py`
```python
from flask import Flask, request, jsonify
import jwt
import hashlib
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Insecure configuration
JWT_SECRET = "weak_secret_key"
API_KEYS = {
    "user123": "api_key_123",
    "admin": "admin_key"
}

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Hardcoded credentials
    if username == "admin" and password == "admin123":
        # Insecure JWT configuration
        token = jwt.encode({
            'user': username,
            'role': 'admin',
            'exp': datetime.utcnow() + timedelta(days=365)  # Long expiration
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'token': token,
            'secret': JWT_SECRET,  # Exposing secret
            'expires': '365 days'
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/users', methods=['GET'])
def get_users():
    # No authentication required
    # Returns sensitive data
    users = [
        {
            'id': 1,
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'hashed_password',  # Exposing password hash
            'ssn': '123-45-6789',  # Exposing SSN
            'api_key': 'user_api_key_123'
        },
        {
            'id': 2,
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'another_hash',
            'credit_card': '4111-1111-1111-1111'  # Exposing credit card
        }
    ]
    
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # No authorization check
    # SQL injection via URL parameter
    import sqlite3
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Vulnerable query
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = cursor.execute(query).fetchone()
    
    if result:
        return jsonify({
            'id': result[0],
            'username': result[1],
            'password_hash': result[2],  # Sensitive data exposure
            'email': result[3],
            'role': result[4]
        })
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/admin/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Weak API key authentication
    api_key = request.headers.get('X-API-Key')
    
    if api_key not in API_KEYS.values():
        return jsonify({'error': 'Invalid API key'}), 401
    
    # No role-based authorization
    # Simulate user deletion
    return jsonify({'message': f'User {user_id} deleted'})

@app.route('/api/upload', methods=['POST'])
def api_upload():
    # No authentication
    # No file type validation
    # No size limits
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    filename = file.filename
    
    # Path traversal vulnerability
    upload_path = f"/uploads/{filename}"
    file.save(upload_path)
    
    # Information disclosure
    return jsonify({
        'message': 'File uploaded',
        'filename': filename,
        'path': upload_path,
        'size': len(file.read())
    })

@app.route('/api/backup', methods=['POST'])
def create_backup():
    # No authentication
    backup_path = request.json.get('path', '/default/backup')
    
    # Command injection vulnerability
    import subprocess
    cmd = f"tar -czf backup.tar.gz {backup_path}"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return jsonify({
            'message': 'Backup created',
            'command': cmd,  # Information disclosure
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    # Exposing sensitive configuration
    config = {
        'database_url': 'postgresql://user:password@localhost/db',
        'api_keys': API_KEYS,
        'jwt_secret': JWT_SECRET,
        'admin_password': 'admin123',
        'aws_access_key': 'AKIAIOSFODNN7EXAMPLE',
        'aws_secret_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
    }
    
    return jsonify(config)

@app.route('/api/logs')
def get_logs():
    # No authentication
    # Information disclosure through logs
    
    log_file = request.args.get('file', 'app.log')
    
    try:
        # Path traversal vulnerability
        with open(f"/var/log/{log_file}", 'r') as f:
            logs = f.read()
        
        return jsonify({
            'logs': logs,
            'file': log_file
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

**Amazon Q API Security Tasks:**

1. **Authentication and Authorization:**
```
@insecure_api.py Analyze authentication and authorization mechanisms. What security flaws exist?
```

2. **Data Exposure Analysis:**
```
Identify all instances of sensitive data exposure in API responses
```

3. **Input Validation Issues:**
```
Find input validation vulnerabilities in API endpoints
```

4. **Configuration Security:**
```
Analyze configuration security issues and suggest improvements
```

**Expected API Security Issues:**
- Weak JWT secret and long expiration
- Hardcoded credentials
- No authentication on sensitive endpoints
- Sensitive data in API responses
- SQL injection in URL parameters
- Weak API key authentication
- No role-based authorization
- Command injection vulnerabilities
- Configuration data exposure
- Path traversal in file operations
- Information disclosure in error messages

---

## Security Fix Implementation

### Task: Implement Security Fixes

**Amazon Q Security Remediation Tasks:**

1. **Comprehensive Security Fixes:**
```
Provide secure implementations for all identified vulnerabilities with proper input validation, authentication, and authorization
```

2. **Security Headers and Configuration:**
```
Suggest security headers and secure configuration settings for the web application
```

3. **Secure Coding Guidelines:**
```
Create a security checklist based on the vulnerabilities found in this assessment
```

---

## Vulnerability Assessment Report

### Critical Vulnerabilities Found:
- [ ] SQL Injection attacks
- [ ] Cross-Site Scripting (XSS)
- [ ] Command Injection
- [ ] Insecure Deserialization
- [ ] Authentication Bypass
- [ ] Sensitive Data Exposure

### High-Risk Issues:
- [ ] Weak Password Hashing
- [ ] Missing Authorization Checks
- [ ] Path Traversal Attacks
- [ ] Information Disclosure
- [ ] Insecure Configuration

### Medium-Risk Issues:
- [ ] User Enumeration
- [ ] Open Redirect
- [ ] Missing CSRF Protection
- [ ] Weak Session Management

### Remediation Priority:
1. **Immediate:** Fix SQL injection and XSS vulnerabilities
2. **High:** Implement proper authentication and authorization
3. **Medium:** Add input validation and secure configuration
4. **Low:** Improve error handling and logging

---

## Success Criteria

You've mastered security assessment when you can:
- [ ] Identify common web application vulnerabilities
- [ ] Recognize API security issues
- [ ] Understand the impact of each vulnerability type
- [ ] Suggest appropriate security fixes
- [ ] Implement secure coding practices
- [ ] Create comprehensive security checklists

**Security Categories Covered:**
- ✅ Authentication and Session Management
- ✅ Input Validation and Injection Attacks
- ✅ Data Exposure and Privacy Issues
- ✅ Authorization and Access Control
- ✅ Configuration and Infrastructure Security

**Completion Time:** 8 minutes  
**Next:** Exercise 2 - Code Quality Enhancement