# Security Best Practices with Amazon Q

## Comprehensive Security Framework

---

## OWASP Top 10 Prevention with Amazon Q

### 1. Injection Attacks Prevention

#### SQL Injection
```python
# Vulnerable Code
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute_query(query)

# Amazon Q Secure Fix
def get_user(user_id: int) -> Optional[Dict]:
    """Safely retrieve user by ID using parameterized queries."""
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID")
    
    query = "SELECT id, username, email FROM users WHERE id = ?"
    return execute_query(query, (user_id,))
```

#### Command Injection
```python
# Vulnerable Code
def backup_database(backup_name):
    os.system(f"mysqldump database > {backup_name}")

# Amazon Q Secure Fix
import subprocess
from pathlib import Path

def backup_database(backup_name: str) -> bool:
    """Safely backup database with input validation."""
    # Validate backup name
    if not backup_name or '..' in backup_name or '/' in backup_name:
        raise ValueError("Invalid backup name")
    
    backup_path = Path('/safe/backup/dir') / f"{backup_name}.sql"
    
    try:
        subprocess.run([
            'mysqldump', 
            '--single-transaction',
            'database'
        ], stdout=open(backup_path, 'w'), check=True)
        return True
    except subprocess.CalledProcessError:
        return False
```

### 2. Authentication Security

#### Secure Password Handling
```python
import bcrypt
import secrets
from datetime import datetime, timedelta

class SecureAuthenticator:
    """Secure authentication implementation."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt with salt."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash using constant-time comparison."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except ValueError:
            return False
    
    @staticmethod
    def generate_secure_token() -> str:
        """Generate cryptographically secure random token."""
        return secrets.token_urlsafe(32)
```

#### Session Management
```python
from flask import session
import redis
import json

class SecureSessionManager:
    """Secure session management with Redis backend."""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.session_timeout = 3600  # 1 hour
    
    def create_session(self, user_id: int) -> str:
        """Create secure session with expiration."""
        session_id = secrets.token_urlsafe(32)
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat()
        }
        
        self.redis.setex(
            f"session:{session_id}",
            self.session_timeout,
            json.dumps(session_data)
        )
        
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[Dict]:
        """Validate and refresh session."""
        if not session_id:
            return None
        
        session_data = self.redis.get(f"session:{session_id}")
        if not session_data:
            return None
        
        data = json.loads(session_data)
        
        # Update last activity
        data['last_activity'] = datetime.utcnow().isoformat()
        self.redis.setex(
            f"session:{session_id}",
            self.session_timeout,
            json.dumps(data)
        )
        
        return data
```

### 3. Cross-Site Scripting (XSS) Prevention

#### Input Sanitization
```python
import html
import bleach
from markupsafe import Markup

class XSSProtection:
    """XSS prevention utilities."""
    
    ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
    ALLOWED_ATTRIBUTES = {}
    
    @staticmethod
    def escape_html(text: str) -> str:
        """Escape HTML characters in user input."""
        if not isinstance(text, str):
            return ""
        return html.escape(text)
    
    @classmethod
    def sanitize_html(cls, html_content: str) -> str:
        """Sanitize HTML content allowing only safe tags."""
        return bleach.clean(
            html_content,
            tags=cls.ALLOWED_TAGS,
            attributes=cls.ALLOWED_ATTRIBUTES,
            strip=True
        )
    
    @staticmethod
    def safe_render(template_string: str, **context) -> Markup:
        """Safely render template with escaped context."""
        escaped_context = {
            key: html.escape(str(value)) if isinstance(value, str) else value
            for key, value in context.items()
        }
        return Markup(template_string.format(**escaped_context))
```

### 4. Secure File Upload

#### File Upload Security
```python
import os
import magic
from werkzeug.utils import secure_filename
from PIL import Image

class SecureFileUpload:
    """Secure file upload handler."""
    
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    UPLOAD_FOLDER = '/secure/uploads'
    
    def __init__(self):
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
    
    def validate_file(self, file) -> bool:
        """Validate uploaded file for security."""
        # Check file size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        
        if size > self.MAX_FILE_SIZE:
            raise ValueError("File too large")
        
        # Check file extension
        filename = secure_filename(file.filename)
        if not filename:
            raise ValueError("Invalid filename")
        
        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise ValueError("File type not allowed")
        
        # Check MIME type
        file_content = file.read(1024)
        file.seek(0)
        
        mime_type = magic.from_buffer(file_content, mime=True)
        expected_mimes = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.pdf': 'application/pdf',
            '.txt': 'text/plain'
        }
        
        if mime_type != expected_mimes.get(ext):
            raise ValueError("File content doesn't match extension")
        
        return True
    
    def save_file(self, file) -> str:
        """Safely save uploaded file."""
        self.validate_file(file)
        
        # Generate secure filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        secure_name = f"{secrets.token_hex(16)}{ext}"
        
        filepath = os.path.join(self.UPLOAD_FOLDER, secure_name)
        
        # Save file
        file.save(filepath)
        
        # Additional security for images
        if ext in {'.jpg', '.jpeg', '.png', '.gif'}:
            self._sanitize_image(filepath)
        
        return secure_name
    
    def _sanitize_image(self, filepath: str):
        """Remove EXIF data and validate image."""
        try:
            with Image.open(filepath) as img:
                # Remove EXIF data
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(list(img.getdata()))
                clean_img.save(filepath)
        except Exception:
            os.remove(filepath)
            raise ValueError("Invalid image file")
```

---

## API Security Best Practices

### 1. JWT Token Security

#### Secure JWT Implementation
```python
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization

class SecureJWTManager:
    """Secure JWT token management."""
    
    def __init__(self, private_key_path: str, public_key_path: str):
        # Use RS256 instead of HS256 for better security
        with open(private_key_path, 'rb') as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), password=None
            )
        
        with open(public_key_path, 'rb') as f:
            self.public_key = serialization.load_pem_public_key(f.read())
    
    def create_token(self, user_id: int, roles: List[str]) -> str:
        """Create secure JWT token with short expiration."""
        payload = {
            'user_id': user_id,
            'roles': roles,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=15),  # Short expiration
            'jti': secrets.token_hex(16)  # Unique token ID
        }
        
        return jwt.encode(payload, self.private_key, algorithm='RS256')
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token, 
                self.public_key, 
                algorithms=['RS256'],
                options={'require': ['exp', 'iat', 'jti']}
            )
            return payload
        except jwt.InvalidTokenError:
            return None
```

### 2. Rate Limiting

#### API Rate Limiting
```python
import time
from collections import defaultdict
from functools import wraps

class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed under rate limit."""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[identifier].append(now)
        return True

def rate_limit(max_requests: int = 100, window_seconds: int = 3600):
    """Rate limiting decorator."""
    limiter = RateLimiter(max_requests, window_seconds)
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Get client identifier (IP, user ID, API key)
            identifier = request.remote_addr
            if 'user_id' in session:
                identifier = f"user:{session['user_id']}"
            
            if not limiter.is_allowed(identifier):
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            return f(*args, **kwargs)
        return wrapper
    return decorator
```

### 3. Input Validation

#### Comprehensive Input Validation
```python
from marshmallow import Schema, fields, validate, ValidationError
from typing import Any, Dict

class UserRegistrationSchema(Schema):
    """Schema for user registration validation."""
    
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(r'^[a-zA-Z0-9_]+$', error='Invalid characters')
        ]
    )
    
    email = fields.Email(required=True)
    
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, max=128),
            validate.Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
                error='Password must contain uppercase, lowercase, digit, and special character'
            )
        ]
    )
    
    age = fields.Int(
        required=True,
        validate=validate.Range(min=13, max=120)
    )

class InputValidator:
    """Centralized input validation."""
    
    @staticmethod
    def validate_json(data: Dict, schema_class: Schema) -> Dict:
        """Validate JSON data against schema."""
        schema = schema_class()
        try:
            return schema.load(data)
        except ValidationError as e:
            raise ValueError(f"Validation error: {e.messages}")
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        """Sanitize string input."""
        if not isinstance(text, str):
            raise ValueError("Input must be string")
        
        # Remove null bytes and control characters
        sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\t\n\r')
        
        # Truncate to max length
        return sanitized[:max_length]
```

---

## Database Security

### 1. Secure Database Operations

#### Parameterized Queries
```python
import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any

class SecureDatabase:
    """Secure database operations."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Get database connection with proper cleanup."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute parameterized query safely."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute parameterized update safely."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Safely get user by ID."""
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
        
        query = """
            SELECT id, username, email, created_at 
            FROM users 
            WHERE id = ? AND active = 1
        """
        
        results = self.execute_query(query, (user_id,))
        return results[0] if results else None
```

### 2. Data Encryption

#### Sensitive Data Encryption
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class DataEncryption:
    """Encrypt sensitive data at rest."""
    
    def __init__(self, password: str):
        # Derive key from password
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
        self.salt = salt
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data."""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    @staticmethod
    def hash_pii(data: str) -> str:
        """One-way hash for PII (for searching)."""
        return hashlib.sha256(data.encode()).hexdigest()
```

---

## Security Headers and Configuration

### 1. Flask Security Headers

#### Comprehensive Security Headers
```python
from flask import Flask, request, g
import secrets

def configure_security_headers(app: Flask):
    """Configure comprehensive security headers."""
    
    @app.before_request
    def security_headers():
        # Generate nonce for CSP
        g.nonce = secrets.token_hex(16)
    
    @app.after_request
    def apply_security_headers(response):
        # Content Security Policy
        csp = (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{g.nonce}'; "
            f"style-src 'self' 'unsafe-inline'; "
            f"img-src 'self' data: https:; "
            f"font-src 'self'; "
            f"connect-src 'self'; "
            f"frame-ancestors 'none'"
        )
        response.headers['Content-Security-Policy'] = csp
        
        # Other security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Remove server information
        response.headers.pop('Server', None)
        
        return response
```

### 2. CORS Configuration

#### Secure CORS Setup
```python
from flask_cors import CORS

def configure_cors(app: Flask):
    """Configure CORS securely."""
    
    # Restrictive CORS configuration
    CORS(app, 
         origins=['https://yourdomain.com'],  # Specific origins only
         methods=['GET', 'POST', 'PUT', 'DELETE'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True,
         max_age=3600)
```

---

## Security Monitoring and Logging

### 1. Security Event Logging

#### Comprehensive Security Logging
```python
import logging
from datetime import datetime
from typing import Optional

class SecurityLogger:
    """Security event logging."""
    
    def __init__(self):
        self.logger = logging.getLogger('security')
        handler = logging.FileHandler('security.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_login_attempt(self, username: str, success: bool, ip_address: str):
        """Log login attempts."""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(
            f"LOGIN_{status} - User: {username}, IP: {ip_address}"
        )
    
    def log_permission_denied(self, user_id: int, resource: str, ip_address: str):
        """Log unauthorized access attempts."""
        self.logger.warning(
            f"PERMISSION_DENIED - User: {user_id}, Resource: {resource}, IP: {ip_address}"
        )
    
    def log_suspicious_activity(self, description: str, user_id: Optional[int], ip_address: str):
        """Log suspicious activities."""
        self.logger.error(
            f"SUSPICIOUS_ACTIVITY - {description}, User: {user_id}, IP: {ip_address}"
        )
```

### 2. Intrusion Detection

#### Basic Intrusion Detection
```python
from collections import defaultdict
import time

class IntrusionDetector:
    """Basic intrusion detection system."""
    
    def __init__(self):
        self.failed_attempts = defaultdict(list)
        self.blocked_ips = set()
        self.max_attempts = 5
        self.block_duration = 3600  # 1 hour
    
    def record_failed_login(self, ip_address: str) -> bool:
        """Record failed login and check if IP should be blocked."""
        now = time.time()
        
        # Clean old attempts
        self.failed_attempts[ip_address] = [
            attempt for attempt in self.failed_attempts[ip_address]
            if now - attempt < 300  # 5 minutes window
        ]
        
        # Add current attempt
        self.failed_attempts[ip_address].append(now)
        
        # Check if should block
        if len(self.failed_attempts[ip_address]) >= self.max_attempts:
            self.blocked_ips.add(ip_address)
            return True
        
        return False
    
    def is_blocked(self, ip_address: str) -> bool:
        """Check if IP is currently blocked."""
        return ip_address in self.blocked_ips
```

---

## Security Testing with Amazon Q

### 1. Security Test Generation

#### Amazon Q Security Testing Prompts
```
"Generate security tests for this authentication system including SQL injection, XSS, and CSRF tests"

"Create penetration testing scenarios for this API endpoint"

"Generate test cases for input validation bypass attempts"

"Create security regression tests for the identified vulnerabilities"
```

### 2. Vulnerability Assessment

#### Automated Security Review
```
"Perform a comprehensive security review of this web application code"

"Identify potential security vulnerabilities in this API implementation"

"Check this code for OWASP Top 10 vulnerabilities"

"Analyze this authentication system for security weaknesses"
```

By following these comprehensive security best practices and leveraging Amazon Q's security analysis capabilities, developers can build more secure applications and protect against common vulnerabilities and attacks.