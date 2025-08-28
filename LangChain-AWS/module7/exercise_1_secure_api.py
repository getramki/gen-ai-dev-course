"""
Exercise 1: Secure Enterprise API
Build an authenticated and authorized LangChain service with enterprise security features.
"""

import jwt
import boto3
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from functools import wraps
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
import secrets
import json

class SecureEnterpriseAPI:
    """Enterprise-grade secure LangChain API."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.app = Flask(__name__)
        self.llm = ChatBedrock(
            model_id=config.get('model_id', 'anthropic.claude-3-sonnet-20240229-v1:0'),
            model_kwargs={'temperature': 0.1, 'max_tokens': 1000}
        )
        
        # Security components
        self.jwt_secret = config.get('jwt_secret', secrets.token_hex(32))
        self.users = {}  # In production, use proper user store
        self.audit_log = []
        self.rate_limits = {}
        
        # Setup routes
        self._setup_routes()
        self._create_default_users()
    
    def _create_default_users(self):
        """Create default users for demo."""
        self.users = {
            'admin': {
                'password_hash': hashlib.sha256('admin123'.encode()).hexdigest(),
                'roles': ['admin'],
                'permissions': ['llm:query', 'llm:admin', 'audit:read']
            },
            'analyst': {
                'password_hash': hashlib.sha256('analyst123'.encode()).hexdigest(),
                'roles': ['analyst'],
                'permissions': ['llm:query', 'llm:analyze']
            },
            'user': {
                'password_hash': hashlib.sha256('user123'.encode()).hexdigest(),
                'roles': ['user'],
                'permissions': ['llm:query']
            }
        }
    
    def _log_audit_event(self, user_id: str, action: str, resource: str, 
                        success: bool, details: Dict = None):
        """Log audit event."""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'success': success,
            'ip_address': request.remote_addr if request else 'system',
            'details': details or {}
        }
        self.audit_log.append(event)
    
    def _check_rate_limit(self, user_id: str, limit_per_minute: int = 10) -> bool:
        """Check rate limiting."""
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        
        if user_id not in self.rate_limits:
            self.rate_limits[user_id] = []
        
        # Clean old requests
        self.rate_limits[user_id] = [
            req_time for req_time in self.rate_limits[user_id] 
            if req_time > minute_ago
        ]
        
        # Check limit
        if len(self.rate_limits[user_id]) >= limit_per_minute:
            return False
        
        # Add current request
        self.rate_limits[user_id].append(now)
        return True
    
    def _setup_routes(self):
        """Setup Flask routes with security."""
        
        @self.app.route('/auth/login', methods=['POST'])
        def login():
            """User authentication endpoint."""
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                self._log_audit_event('unknown', 'login', 'auth', False, 
                                    {'reason': 'missing_credentials'})
                return jsonify({'error': 'Username and password required'}), 400
            
            # Verify credentials
            user = self.users.get(username)
            if not user:
                self._log_audit_event(username, 'login', 'auth', False, 
                                    {'reason': 'user_not_found'})
                return jsonify({'error': 'Invalid credentials'}), 401
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash != user['password_hash']:
                self._log_audit_event(username, 'login', 'auth', False, 
                                    {'reason': 'invalid_password'})
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Generate JWT token
            token_payload = {
                'user_id': username,
                'roles': user['roles'],
                'permissions': user['permissions'],
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            
            token = jwt.encode(token_payload, self.jwt_secret, algorithm='HS256')
            
            self._log_audit_event(username, 'login', 'auth', True)
            
            return jsonify({
                'token': token,
                'expires_in': 86400,  # 24 hours
                'user_id': username,
                'roles': user['roles']
            })
        
        @self.app.route('/query', methods=['POST'])
        @self._require_auth(['llm:query'])
        def process_query():
            """Process LLM query with authentication."""
            user_context = request.user_context
            user_id = user_context['user_id']
            
            # Rate limiting
            if not self._check_rate_limit(user_id):
                self._log_audit_event(user_id, 'query', 'llm', False, 
                                    {'reason': 'rate_limit_exceeded'})
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            data = request.get_json()
            query = data.get('query')
            
            if not query:
                return jsonify({'error': 'Query required'}), 400
            
            try:
                # Create secure prompt
                prompt = ChatPromptTemplate.from_template(
                    "User {user_id} with roles {roles} asks: {query}\n"
                    "Provide a helpful and secure response."
                )
                
                chain = prompt | self.llm
                result = chain.invoke({
                    'user_id': user_id,
                    'roles': ', '.join(user_context['roles']),
                    'query': query
                })
                
                self._log_audit_event(user_id, 'query', 'llm', True, 
                                    {'query_length': len(query)})
                
                return jsonify({
                    'success': True,
                    'response': result.content,
                    'user_id': user_id,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
            except Exception as e:
                self._log_audit_event(user_id, 'query', 'llm', False, 
                                    {'error': str(e)})
                return jsonify({'error': 'Processing failed'}), 500
        
        @self.app.route('/admin/audit', methods=['GET'])
        @self._require_auth(['audit:read'])
        def get_audit_logs():
            """Get audit logs (admin only)."""
            user_context = request.user_context
            user_id = user_context['user_id']
            
            # Get query parameters
            limit = min(int(request.args.get('limit', 50)), 1000)
            offset = int(request.args.get('offset', 0))
            
            # Filter logs
            filtered_logs = self.audit_log[offset:offset + limit]
            
            self._log_audit_event(user_id, 'read', 'audit_logs', True, 
                                {'logs_returned': len(filtered_logs)})
            
            return jsonify({
                'logs': filtered_logs,
                'total': len(self.audit_log),
                'limit': limit,
                'offset': offset
            })
        
        @self.app.route('/admin/users', methods=['GET'])
        @self._require_auth(['llm:admin'])
        def list_users():
            """List users (admin only)."""
            user_context = request.user_context
            user_id = user_context['user_id']
            
            # Return user info without passwords
            users_info = {}
            for username, user_data in self.users.items():
                users_info[username] = {
                    'roles': user_data['roles'],
                    'permissions': user_data['permissions']
                }
            
            self._log_audit_event(user_id, 'list', 'users', True)
            
            return jsonify({'users': users_info})
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint (no auth required)."""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': '1.0.0'
            })
    
    def _require_auth(self, required_permissions: List[str] = None):
        """Authentication and authorization decorator."""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Get token from header
                auth_header = request.headers.get('Authorization')
                if not auth_header or not auth_header.startswith('Bearer '):
                    return jsonify({'error': 'Authentication required'}), 401
                
                token = auth_header.split(' ')[1]
                
                try:
                    # Verify JWT token
                    payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
                    
                    # Check permissions
                    if required_permissions:
                        user_permissions = payload.get('permissions', [])
                        if not any(perm in user_permissions for perm in required_permissions):
                            return jsonify({'error': 'Insufficient permissions'}), 403
                    
                    # Add user context to request
                    request.user_context = payload
                    
                    return f(*args, **kwargs)
                    
                except jwt.ExpiredSignatureError:
                    return jsonify({'error': 'Token expired'}), 401
                except jwt.InvalidTokenError:
                    return jsonify({'error': 'Invalid token'}), 401
            
            return decorated_function
        return decorator
    
    def run(self, host='0.0.0.0', port=8000, debug=False):
        """Run the secure API."""
        print(f"Starting Secure Enterprise API on {host}:{port}")
        print("Default users:")
        for username, user_data in self.users.items():
            print(f"  {username}: roles={user_data['roles']}, permissions={user_data['permissions']}")
        
        self.app.run(host=host, port=port, debug=debug)

def demonstrate_secure_api():
    """Demonstrate secure API functionality."""
    
    print("=== Secure Enterprise API Demo ===\n")
    
    # Configuration
    config = {
        'model_id': 'anthropic.claude-3-sonnet-20240229-v1:0',
        'jwt_secret': 'demo-secret-key-change-in-production'
    }
    
    # Initialize API
    api = SecureEnterpriseAPI(config)
    
    print("1. API Configuration:")
    print(f"Model: {config['model_id']}")
    print(f"JWT Secret: {config['jwt_secret'][:20]}...")
    print()
    
    print("2. Default Users Created:")
    for username, user_data in api.users.items():
        print(f"Username: {username}")
        print(f"  Roles: {user_data['roles']}")
        print(f"  Permissions: {user_data['permissions']}")
        print(f"  Password: {username}123")  # Demo only!
        print()
    
    print("3. Security Features:")
    features = [
        "JWT-based authentication",
        "Role-based access control (RBAC)",
        "Permission-based authorization",
        "Rate limiting (10 requests/minute)",
        "Comprehensive audit logging",
        "Secure password hashing",
        "Token expiration (24 hours)",
        "IP address logging"
    ]
    
    for feature in features:
        print(f"✓ {feature}")
    
    print()
    
    print("4. API Endpoints:")
    endpoints = [
        ("POST /auth/login", "User authentication", "None"),
        ("POST /query", "Process LLM queries", "llm:query"),
        ("GET /admin/audit", "View audit logs", "audit:read"),
        ("GET /admin/users", "List users", "llm:admin"),
        ("GET /health", "Health check", "None")
    ]
    
    print(f"{'Endpoint':<20} {'Description':<25} {'Required Permission'}")
    print("-" * 70)
    for endpoint, desc, perm in endpoints:
        print(f"{endpoint:<20} {desc:<25} {perm}")
    
    print()
    
    print("5. Usage Examples:")
    print("# Login as admin")
    print("curl -X POST http://localhost:8000/auth/login \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"username\": \"admin\", \"password\": \"admin123\"}'")
    print()
    
    print("# Query with token")
    print("curl -X POST http://localhost:8000/query \\")
    print("  -H 'Authorization: Bearer <token>' \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"query\": \"What is machine learning?\"}'")
    print()
    
    print("# Get audit logs (admin only)")
    print("curl -X GET http://localhost:8000/admin/audit \\")
    print("  -H 'Authorization: Bearer <admin_token>'")
    print()
    
    print("6. Security Considerations:")
    considerations = [
        "Change default passwords in production",
        "Use strong JWT secrets (32+ characters)",
        "Implement HTTPS in production",
        "Add input validation and sanitization",
        "Use proper user store (database)",
        "Implement session management",
        "Add request logging and monitoring",
        "Consider API versioning"
    ]
    
    for consideration in considerations:
        print(f"⚠️  {consideration}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        # Run the API server
        config = {
            'model_id': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'jwt_secret': 'demo-secret-key-change-in-production'
        }
        
        api = SecureEnterpriseAPI(config)
        api.run(debug=False)
    else:
        # Run demonstration
        demonstrate_secure_api()