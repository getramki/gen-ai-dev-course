"""
Module 7.1: Authentication and Authorization
Enterprise security patterns for LangChain applications.
"""

import jwt
import boto3
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from functools import wraps
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
import hashlib
import secrets

class AuthenticationManager:
    """Manages authentication and authorization for LangChain services."""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.cognito = boto3.client('cognito-idp')
        self.iam = boto3.client('iam')
    
    def generate_jwt_token(self, user_id: str, permissions: list, expires_hours: int = 24) -> str:
        """Generate JWT token with user permissions."""
        payload = {
            'user_id': user_id,
            'permissions': permissions,
            'exp': datetime.utcnow() + timedelta(hours=expires_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def check_permission(self, user_permissions: list, required_permission: str) -> bool:
        """Check if user has required permission."""
        return required_permission in user_permissions or 'admin' in user_permissions

def require_auth(required_permission: str = None):
    """Decorator for requiring authentication and authorization."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract token from request headers (simplified)
            token = kwargs.get('auth_token')
            if not token:
                return {'error': 'Authentication required', 'status': 401}
            
            # Verify token
            auth_manager = AuthenticationManager('your-secret-key')
            payload = auth_manager.verify_jwt_token(token)
            if not payload:
                return {'error': 'Invalid token', 'status': 401}
            
            # Check permissions
            if required_permission:
                if not auth_manager.check_permission(payload['permissions'], required_permission):
                    return {'error': 'Insufficient permissions', 'status': 403}
            
            # Add user context to kwargs
            kwargs['user_context'] = payload
            return func(*args, **kwargs)
        return wrapper
    return decorator

class SecureLangChainService:
    """Secure LangChain service with authentication and authorization."""
    
    def __init__(self, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            model_kwargs={"temperature": 0.1, "max_tokens": 1000}
        )
        self.audit_log = []
    
    def _log_access(self, user_id: str, action: str, resource: str, success: bool):
        """Log access attempts for audit purposes."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'success': success,
            'ip_address': 'simulated_ip'  # In real implementation, get from request
        }
        self.audit_log.append(log_entry)
    
    @require_auth('llm:query')
    def process_query(self, query: str, auth_token: str = None, user_context: Dict = None) -> Dict[str, Any]:
        """Process LLM query with authentication."""
        user_id = user_context['user_id']
        
        try:
            # Create secure prompt
            prompt = ChatPromptTemplate.from_template(
                "User {user_id} asks: {query}\nProvide a helpful response."
            )
            
            chain = prompt | self.llm
            result = chain.invoke({'user_id': user_id, 'query': query})
            
            # Log successful access
            self._log_access(user_id, 'query', 'llm', True)
            
            return {
                'success': True,
                'result': result.content,
                'user_id': user_id
            }
            
        except Exception as e:
            # Log failed access
            self._log_access(user_id, 'query', 'llm', False)
            return {'success': False, 'error': str(e)}
    
    @require_auth('admin')
    def get_audit_logs(self, auth_token: str = None, user_context: Dict = None) -> Dict[str, Any]:
        """Get audit logs (admin only)."""
        return {
            'success': True,
            'logs': self.audit_log[-10:],  # Last 10 entries
            'total_entries': len(self.audit_log)
        }

class RoleBasedAccessControl:
    """Role-based access control system."""
    
    def __init__(self):
        self.roles = {
            'user': ['llm:query', 'profile:read'],
            'analyst': ['llm:query', 'llm:analyze', 'data:read'],
            'admin': ['admin', 'llm:query', 'llm:analyze', 'data:read', 'data:write', 'user:manage']
        }
        self.user_roles = {}
    
    def assign_role(self, user_id: str, role: str):
        """Assign role to user."""
        if role in self.roles:
            self.user_roles[user_id] = role
    
    def get_user_permissions(self, user_id: str) -> list:
        """Get permissions for user based on role."""
        role = self.user_roles.get(user_id, 'user')
        return self.roles.get(role, [])

class DataEncryption:
    """Data encryption utilities for sensitive information."""
    
    def __init__(self, kms_key_id: str = None):
        self.kms = boto3.client('kms') if kms_key_id else None
        self.kms_key_id = kms_key_id
    
    def encrypt_sensitive_data(self, data: str) -> Dict[str, str]:
        """Encrypt sensitive data using AWS KMS."""
        if self.kms and self.kms_key_id:
            try:
                response = self.kms.encrypt(
                    KeyId=self.kms_key_id,
                    Plaintext=data.encode('utf-8')
                )
                return {
                    'encrypted_data': response['CiphertextBlob'].hex(),
                    'key_id': self.kms_key_id
                }
            except Exception as e:
                # Fallback to simple encoding (not secure for production)
                return {
                    'encrypted_data': data.encode('utf-8').hex(),
                    'key_id': 'fallback'
                }
        else:
            # Simple encoding for demo (not secure)
            return {
                'encrypted_data': data.encode('utf-8').hex(),
                'key_id': 'demo'
            }
    
    def decrypt_sensitive_data(self, encrypted_data: str, key_id: str) -> str:
        """Decrypt sensitive data."""
        if self.kms and key_id != 'fallback' and key_id != 'demo':
            try:
                response = self.kms.decrypt(
                    CiphertextBlob=bytes.fromhex(encrypted_data)
                )
                return response['Plaintext'].decode('utf-8')
            except Exception:
                pass
        
        # Fallback decoding
        try:
            return bytes.fromhex(encrypted_data).decode('utf-8')
        except Exception:
            return "Decryption failed"

def demonstrate_enterprise_auth():
    """Demonstrate enterprise authentication and authorization."""
    
    print("=== Enterprise Authentication Demo ===\n")
    
    # 1. Setup authentication
    auth_manager = AuthenticationManager('demo-secret-key')
    rbac = RoleBasedAccessControl()
    
    # Assign roles
    rbac.assign_role('user123', 'analyst')
    rbac.assign_role('admin456', 'admin')
    
    # Generate tokens
    user_permissions = rbac.get_user_permissions('user123')
    admin_permissions = rbac.get_user_permissions('admin456')
    
    user_token = auth_manager.generate_jwt_token('user123', user_permissions)
    admin_token = auth_manager.generate_jwt_token('admin456', admin_permissions)
    
    print("1. Token Generation:")
    print(f"User token: {user_token[:50]}...")
    print(f"Admin token: {admin_token[:50]}...")
    print()
    
    # 2. Secure service
    service = SecureLangChainService(auth_manager)
    
    print("2. Authenticated Queries:")
    
    # User query
    user_result = service.process_query(
        "What is machine learning?",
        auth_token=user_token
    )
    print(f"User query success: {user_result['success']}")
    if user_result['success']:
        print(f"Response: {user_result['result'][:100]}...")
    print()
    
    # Admin audit log access
    admin_result = service.get_audit_logs(auth_token=admin_token)
    print(f"Admin audit access: {admin_result['success']}")
    print(f"Log entries: {admin_result.get('total_entries', 0)}")
    print()
    
    # 3. Data encryption
    print("3. Data Encryption:")
    encryption = DataEncryption()
    
    sensitive_data = "User personal information: John Doe, john@example.com"
    encrypted = encryption.encrypt_sensitive_data(sensitive_data)
    decrypted = encryption.decrypt_sensitive_data(encrypted['encrypted_data'], encrypted['key_id'])
    
    print(f"Original: {sensitive_data}")
    print(f"Encrypted: {encrypted['encrypted_data'][:50]}...")
    print(f"Decrypted: {decrypted}")
    print()
    
    # 4. Permission testing
    print("4. Permission Testing:")
    test_permissions = ['llm:query', 'admin', 'data:write']
    user_perms = rbac.get_user_permissions('user123')
    
    for perm in test_permissions:
        has_perm = auth_manager.check_permission(user_perms, perm)
        print(f"User has '{perm}': {has_perm}")

if __name__ == "__main__":
    demonstrate_enterprise_auth()