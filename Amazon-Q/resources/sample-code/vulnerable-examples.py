# Vulnerable Code Examples for Module 5 Security Exercises

from flask import Flask, request, session, render_template_string, jsonify
import sqlite3
import hashlib
import subprocess
import os
import pickle
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "hardcoded_secret_key"  # Security Issue: Hardcoded secret

# Global variables with sensitive data
ADMIN_PASSWORD = "admin123"  # Security Issue: Weak password
DATABASE_URL = "postgresql://admin:password@localhost/db"  # Security Issue: Exposed credentials
API_KEYS = {
    "user1": "simple_api_key_123",
    "admin": "admin_api_key_456"
}

# SQL Injection Vulnerabilities
class VulnerableDatabase:
    """Database class with SQL injection vulnerabilities"""
    
    def __init__(self, db_path="vulnerable.db"):
        self.db_path = db_path
    
    def get_user_by_credentials(self, username, password):
        """Vulnerable to SQL injection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # SQL Injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        result = cursor.execute(query).fetchone()
        
        conn.close()
        return result
    
    def search_products(self, search_term):
        """Another SQL injection vulnerability"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Vulnerable dynamic query
        query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%' OR description LIKE '%{search_term}%'"
        results = cursor.execute(query).fetchall()
        
        conn.close()
        return results
    
    def update_user_profile(self, user_id, field, value):
        """SQL injection in UPDATE statement"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Dynamic field name - SQL injection risk
        query = f"UPDATE users SET {field} = '{value}' WHERE id = {user_id}"
        cursor.execute(query)
        conn.commit()
        conn.close()

# Authentication Vulnerabilities
class InsecureAuth:
    """Authentication system with multiple security flaws"""
    
    @staticmethod
    def hash_password(password):
        """Weak password hashing using MD5"""
        return hashlib.md5(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, stored_hash):
        """Vulnerable to timing attacks"""
        return InsecureAuth.hash_password(password) == stored_hash
    
    @staticmethod
    def generate_session_token(user_id):
        """Predictable session token generation"""
        return hashlib.md5(f"{user_id}{datetime.now().date()}".encode()).hexdigest()
    
    @staticmethod
    def create_jwt_token(user_data):
        """Insecure JWT configuration"""
        payload = {
            'user_id': user_data['id'],
            'username': user_data['username'],
            'is_admin': user_data.get('is_admin', False),
            'password': user_data['password'],  # Sensitive data in token
            'exp': datetime.utcnow() + timedelta(days=365)  # Long expiration
        }
        
        # Weak secret key
        return jwt.encode(payload, "weak_secret", algorithm='HS256')

# XSS Vulnerabilities
@app.route('/profile/<username>')
def user_profile(username):
    """Reflected XSS vulnerability"""
    # Direct insertion of user input without escaping
    return f"<h1>Welcome {username}!</h1><p>This is your profile page.</p>"

@app.route('/search')
def search():
    """XSS in search functionality"""
    query = request.args.get('q', '')
    
    # Vulnerable template rendering
    template = f"""
    <html>
        <head><title>Search Results</title></head>
        <body>
            <h1>Search Results for: {query}</h1>
            <p>You searched for: {query}</p>
            <script>
                var searchTerm = "{query}";  // XSS vulnerability
                console.log("Search term: " + searchTerm);
            </script>
        </body>
    </html>
    """
    return render_template_string(template)

@app.route('/comment', methods=['POST'])
def add_comment():
    """Stored XSS vulnerability"""
    comment = request.form.get('comment', '')
    author = request.form.get('author', '')
    
    # Store comment without sanitization
    with open('comments.html', 'a') as f:
        f.write(f'<div><strong>{author}</strong>: {comment}</div>\n')
    
    return f"Comment added: {comment}"

# Command Injection Vulnerabilities
@app.route('/ping')
def ping_host():
    """Command injection vulnerability"""
    host = request.args.get('host', 'localhost')
    
    # Direct command execution with user input
    result = subprocess.run(f"ping -c 4 {host}", shell=True, capture_output=True, text=True)
    
    return f"<pre>{result.stdout}</pre>"

@app.route('/backup')
def create_backup():
    """Another command injection example"""
    backup_name = request.args.get('name', 'default')
    
    # Vulnerable to command injection
    command = f"tar -czf /backups/{backup_name}.tar.gz /app/data"
    os.system(command)
    
    return f"Backup created: {backup_name}.tar.gz"

# File Upload Vulnerabilities
@app.route('/upload', methods=['POST'])
def upload_file():
    """Insecure file upload"""
    if 'file' not in request.files:
        return "No file uploaded"
    
    file = request.files['file']
    filename = file.filename
    
    # No validation of file type, size, or name
    # Path traversal vulnerability
    upload_path = f"/uploads/{filename}"
    file.save(upload_path)
    
    return f"File uploaded: {filename}"

# Path Traversal Vulnerabilities
@app.route('/download')
def download_file():
    """Path traversal vulnerability"""
    filename = request.args.get('file', 'default.txt')
    
    # No path validation - allows directory traversal
    try:
        with open(f"/app/files/{filename}", 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/logs')
def view_logs():
    """Another path traversal example"""
    log_file = request.args.get('log', 'app.log')
    
    # Vulnerable to path traversal
    log_path = f"/var/log/{log_file}"
    
    try:
        with open(log_path, 'r') as f:
            logs = f.read()
        return f"<pre>{logs}</pre>"
    except Exception as e:
        return f"Error reading log: {str(e)}"

# Insecure Deserialization
@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    """Insecure deserialization vulnerability"""
    data = request.get_data()
    
    try:
        # Dangerous: deserializing untrusted data
        obj = pickle.loads(data)
        return f"Deserialized: {obj}"
    except Exception as e:
        return f"Error: {str(e)}"

# Information Disclosure
@app.route('/debug')
def debug_info():
    """Information disclosure through debug endpoint"""
    debug_data = {
        'database_url': DATABASE_URL,
        'api_keys': API_KEYS,
        'secret_key': app.secret_key,
        'admin_password': ADMIN_PASSWORD,
        'environment_vars': dict(os.environ),
        'current_user': session.get('user_id'),
        'server_info': {
            'python_version': os.sys.version,
            'working_directory': os.getcwd(),
            'process_id': os.getpid()
        }
    }
    
    return jsonify(debug_data)

@app.route('/error_test')
def trigger_error():
    """Information disclosure through error messages"""
    try:
        # Intentionally cause an error
        result = 1 / 0
    except Exception as e:
        # Exposing internal error details
        return jsonify({
            'error': str(e),
            'type': type(e).__name__,
            'traceback': str(e.__traceback__),
            'locals': locals(),
            'globals_keys': list(globals().keys())
        })

# Weak Session Management
@app.route('/login', methods=['POST'])
def login():
    """Weak session management"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Weak authentication check
    if username == "admin" and password == ADMIN_PASSWORD:
        # Insecure session data
        session['user_id'] = 1
        session['username'] = username
        session['is_admin'] = True
        session['password'] = password  # Storing password in session
        session['login_time'] = datetime.now().isoformat()
        
        return "Login successful"
    
    # Information disclosure
    return f"Login failed for user: {username}"

# Missing Authorization
@app.route('/admin/users')
def admin_users():
    """Missing authorization check"""
    # No authentication or authorization check
    users = [
        {'id': 1, 'username': 'admin', 'password': 'hashed_password', 'ssn': '123-45-6789'},
        {'id': 2, 'username': 'user', 'password': 'another_hash', 'email': 'user@example.com'}
    ]
    
    return jsonify(users)

@app.route('/admin/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Critical operation without proper authorization"""
    # No authorization check for admin operation
    # Simulate user deletion
    return jsonify({'message': f'User {user_id} deleted'})

# CSRF Vulnerabilities
@app.route('/change_password', methods=['POST'])
def change_password():
    """CSRF vulnerability - no token validation"""
    user_id = session.get('user_id')
    new_password = request.form.get('new_password')
    
    if not user_id:
        return "Not logged in"
    
    # No CSRF token validation
    # Update password without additional verification
    hashed_password = InsecureAuth.hash_password(new_password)
    
    # Simulate password update
    return "Password changed successfully"

@app.route('/transfer_money', methods=['POST'])
def transfer_money():
    """CSRF vulnerability in financial operation"""
    from_account = session.get('account_id')
    to_account = request.form.get('to_account')
    amount = request.form.get('amount')
    
    # No CSRF protection on sensitive operation
    # Simulate money transfer
    return f"Transferred ${amount} from {from_account} to {to_account}"

# Weak Cryptography
class WeakCrypto:
    """Examples of weak cryptographic practices"""
    
    @staticmethod
    def encrypt_data(data, key="default_key"):
        """Weak encryption using simple XOR"""
        encrypted = ""
        for i, char in enumerate(data):
            encrypted += chr(ord(char) ^ ord(key[i % len(key)]))
        return encrypted.encode('base64')  # Deprecated base64 encoding
    
    @staticmethod
    def generate_api_key(user_id):
        """Predictable API key generation"""
        return hashlib.md5(f"api_key_{user_id}_{datetime.now().date()}".encode()).hexdigest()
    
    @staticmethod
    def create_password_reset_token(email):
        """Predictable reset token"""
        return hashlib.md5(f"{email}_{datetime.now().hour}".encode()).hexdigest()

# Race Condition Vulnerabilities
class VulnerableCounter:
    """Race condition in counter operations"""
    
    def __init__(self):
        self.count = 0
        self.balance = 1000
    
    def increment(self):
        """Race condition in increment"""
        temp = self.count
        # Simulate processing time
        import time
        time.sleep(0.001)
        self.count = temp + 1
    
    def withdraw(self, amount):
        """Race condition in balance check"""
        if self.balance >= amount:
            # Race condition window
            import time
            time.sleep(0.001)
            self.balance -= amount
            return True
        return False

# Business Logic Vulnerabilities
@app.route('/purchase', methods=['POST'])
def purchase_item():
    """Business logic vulnerability"""
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 1))
    
    # No validation of negative quantities
    # Could allow negative purchases (refunds without authorization)
    
    item_price = get_item_price(item_id)
    total_cost = item_price * quantity  # Negative quantity creates negative cost
    
    user_balance = get_user_balance(session.get('user_id'))
    
    if user_balance >= total_cost:  # Negative cost always passes
        # Process purchase
        update_user_balance(session.get('user_id'), user_balance - total_cost)
        return f"Purchase successful. Total: ${total_cost}"
    
    return "Insufficient funds"

# Helper functions for examples
def get_item_price(item_id):
    return 10.0  # Simplified

def get_user_balance(user_id):
    return 100.0  # Simplified

def update_user_balance(user_id, new_balance):
    pass  # Simplified

# Insecure Direct Object References
@app.route('/user/<int:user_id>/profile')
def get_user_profile(user_id):
    """Insecure direct object reference"""
    # No authorization check - any user can access any profile
    
    db = VulnerableDatabase()
    user = db.get_user_by_id(user_id)
    
    if user:
        return jsonify({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'ssn': user[3],  # Sensitive data exposure
            'credit_card': user[4]  # More sensitive data
        })
    
    return "User not found", 404

@app.route('/document/<int:doc_id>')
def get_document(doc_id):
    """Another IDOR example"""
    # No ownership verification
    document = get_document_by_id(doc_id)
    
    return jsonify({
        'id': document['id'],
        'title': document['title'],
        'content': document['content'],
        'owner_id': document['owner_id']
    })

def get_document_by_id(doc_id):
    return {'id': doc_id, 'title': 'Secret Document', 'content': 'Confidential content', 'owner_id': 123}

# XML External Entity (XXE) Vulnerability
@app.route('/xml_upload', methods=['POST'])
def process_xml():
    """XXE vulnerability"""
    xml_data = request.get_data()
    
    import xml.etree.ElementTree as ET
    
    try:
        # Vulnerable XML parsing - allows external entities
        root = ET.fromstring(xml_data)
        
        # Process XML data
        result = {}
        for child in root:
            result[child.tag] = child.text
        
        return jsonify(result)
    
    except Exception as e:
        return f"XML parsing error: {str(e)}"

# Server-Side Request Forgery (SSRF)
@app.route('/fetch_url')
def fetch_external_url():
    """SSRF vulnerability"""
    url = request.args.get('url')
    
    # No URL validation - allows internal network access
    import requests
    
    try:
        response = requests.get(url, timeout=5)
        return {
            'status_code': response.status_code,
            'content': response.text[:1000],  # Truncated content
            'headers': dict(response.headers)
        }
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

if __name__ == '__main__':
    # Insecure configuration
    app.run(
        host='0.0.0.0',  # Binds to all interfaces
        port=5000,
        debug=True,  # Debug mode in production
        ssl_context=None  # No HTTPS
    )