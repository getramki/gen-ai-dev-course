# Exercise 1: Secure Enterprise API

## Objective
Build and deploy a secure, enterprise-grade LangChain API with comprehensive authentication, authorization, and audit capabilities.

## Time Estimate
15 minutes

## Prerequisites
- Completed previous modules
- Understanding of authentication concepts
- Basic knowledge of JWT and RBAC

## Step-by-Step Instructions

### Step 1: Understand the Security Architecture
1. **Review security components**:
   - JWT-based authentication with token expiration
   - Role-based access control (RBAC) with permissions
   - Rate limiting to prevent abuse
   - Comprehensive audit logging
   - Secure password hashing

2. **Examine the user roles**:
   - **Admin**: Full access including user management and audit logs
   - **Analyst**: LLM query and analysis capabilities
   - **User**: Basic LLM query access only

### Step 2: Run the Secure API Demo
```bash
cd module7
python exercise_1_secure_api.py
```

**Expected Output**:
- API configuration details
- Default user accounts with roles and permissions
- Security features overview
- Available endpoints with required permissions
- Usage examples and security considerations

### Step 3: Start the Secure API Server
```bash
python exercise_1_secure_api.py run
```

The server will start on `http://localhost:8000` with the following default users:
- **admin/admin123**: Full administrative access
- **analyst/analyst123**: Analysis and query access
- **user/user123**: Basic query access only

### Step 4: Test Authentication Flow
1. **Login as admin**:
   ```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
   ```

2. **Save the returned token** for subsequent requests:
   ```json
   {
     "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
     "expires_in": 86400,
     "user_id": "admin",
     "roles": ["admin"]
   }
   ```

3. **Test different user roles**:
   ```bash
   # Login as analyst
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "analyst", "password": "analyst123"}'
   
   # Login as regular user
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "user", "password": "user123"}'
   ```

### Step 5: Test Authorized Endpoints
1. **Process LLM query** (all authenticated users):
   ```bash
   curl -X POST http://localhost:8000/query \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{"query": "Explain quantum computing in simple terms"}'
   ```

2. **Access audit logs** (admin only):
   ```bash
   curl -X GET http://localhost:8000/admin/audit \
     -H "Authorization: Bearer <admin_token>"
   ```

3. **List users** (admin only):
   ```bash
   curl -X GET http://localhost:8000/admin/users \
     -H "Authorization: Bearer <admin_token>"
   ```

4. **Test unauthorized access**:
   ```bash
   # Try accessing admin endpoint with user token
   curl -X GET http://localhost:8000/admin/audit \
     -H "Authorization: Bearer <user_token>"
   ```

### Step 6: Test Security Features
1. **Rate limiting test**:
   ```bash
   # Send multiple requests quickly to trigger rate limiting
   for i in {1..15}; do
     curl -X POST http://localhost:8000/query \
       -H "Authorization: Bearer <your_token>" \
       -H "Content-Type: application/json" \
       -d '{"query": "Test query '$i'"}' &
   done
   wait
   ```

2. **Token expiration test**:
   ```bash
   # Use an expired or invalid token
   curl -X POST http://localhost:8000/query \
     -H "Authorization: Bearer invalid_token" \
     -H "Content-Type: application/json" \
     -d '{"query": "This should fail"}'
   ```

3. **Missing authentication test**:
   ```bash
   # Try accessing protected endpoint without token
   curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"query": "This should fail"}'
   ```

### Step 7: Monitor Audit Logs
1. **View audit logs** to see all security events:
   ```bash
   curl -X GET http://localhost:8000/admin/audit?limit=20 \
     -H "Authorization: Bearer <admin_token>"
   ```

2. **Analyze audit events**:
   - Login attempts (successful and failed)
   - Query processing events
   - Rate limiting violations
   - Permission denied events
   - Administrative actions

### Step 8: Enhance Security (Optional)
1. **Add input validation**:
   ```python
   from marshmallow import Schema, fields, ValidationError
   
   class QuerySchema(Schema):
       query = fields.Str(required=True, validate=lambda x: 1 <= len(x) <= 1000)
   
   # Use in route
   schema = QuerySchema()
   try:
       validated_data = schema.load(data)
   except ValidationError as err:
       return jsonify({'error': err.messages}), 400
   ```

2. **Add request sanitization**:
   ```python
   import html
   import re
   
   def sanitize_input(text: str) -> str:
       # HTML escape
       text = html.escape(text)
       # Remove potential SQL injection patterns
       text = re.sub(r'[;\'"\\]', '', text)
       return text
   ```

3. **Add session management**:
   ```python
   class SessionManager:
       def __init__(self):
           self.active_sessions = {}
       
       def create_session(self, user_id: str, token: str):
           self.active_sessions[token] = {
               'user_id': user_id,
               'created': datetime.utcnow(),
               'last_activity': datetime.utcnow()
           }
       
       def validate_session(self, token: str) -> bool:
           session = self.active_sessions.get(token)
           if not session:
               return False
           
           # Check for session timeout (e.g., 30 minutes of inactivity)
           if datetime.utcnow() - session['last_activity'] > timedelta(minutes=30):
               del self.active_sessions[token]
               return False
           
           session['last_activity'] = datetime.utcnow()
           return True
   ```

## Expected Output

### Successful Authentication
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJyb2xlcyI6WyJhZG1pbiJdLCJwZXJtaXNzaW9ucyI6WyJsbG06cXVlcnkiLCJsbG06YWRtaW4iLCJhdWRpdDpyZWFkIl0sImV4cCI6MTcwNTQwMjgwMCwiaWF0IjoxNzA1MzE2NDAwfQ.signature",
  "expires_in": 86400,
  "user_id": "admin",
  "roles": ["admin"]
}
```

### Successful Query Response
```json
{
  "success": true,
  "response": "Quantum computing is a revolutionary computing paradigm that leverages quantum mechanical phenomena...",
  "user_id": "admin",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Audit Log Entry
```json
{
  "logs": [
    {
      "timestamp": "2024-01-15T10:30:00.000Z",
      "user_id": "admin",
      "action": "login",
      "resource": "auth",
      "success": true,
      "ip_address": "127.0.0.1",
      "details": {}
    },
    {
      "timestamp": "2024-01-15T10:31:00.000Z",
      "user_id": "admin",
      "action": "query",
      "resource": "llm",
      "success": true,
      "ip_address": "127.0.0.1",
      "details": {"query_length": 45}
    }
  ],
  "total": 15,
  "limit": 50,
  "offset": 0
}
```

## Common Issues and Solutions

### Issue 1: Authentication Failures
**Problem**: Login requests return 401 Unauthorized
**Solution**: 
- Verify username and password are correct
- Check that Content-Type header is set to application/json
- Ensure request body is valid JSON

### Issue 2: Token Expired Errors
**Problem**: Valid requests return "Token expired" error
**Solution**:
- Check token expiration time (24 hours by default)
- Re-authenticate to get a new token
- Verify system clock is synchronized

### Issue 3: Permission Denied
**Problem**: User gets 403 Forbidden for certain endpoints
**Solution**:
- Check user roles and permissions
- Verify the endpoint requires the correct permission
- Use admin account for administrative endpoints

### Issue 4: Rate Limiting
**Problem**: Requests return 429 Too Many Requests
**Solution**:
- Wait for rate limit window to reset (1 minute)
- Reduce request frequency
- Implement exponential backoff in client

## Challenge Extensions

### Extension 1: Multi-Factor Authentication
Add MFA support:
```python
import pyotp

class MFAManager:
    def __init__(self):
        self.user_secrets = {}
    
    def setup_mfa(self, user_id: str) -> str:
        secret = pyotp.random_base32()
        self.user_secrets[user_id] = secret
        return pyotp.totp.TOTP(secret).provisioning_uri(
            user_id, issuer_name="LangChain Enterprise"
        )
    
    def verify_mfa(self, user_id: str, token: str) -> bool:
        secret = self.user_secrets.get(user_id)
        if not secret:
            return False
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
```

### Extension 2: OAuth 2.0 Integration
Integrate with external OAuth providers:
```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id='your-google-client-id',
    client_secret='your-google-client-secret',
    server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
    client_kwargs={'scope': 'openid email profile'}
)
```

### Extension 3: Advanced Audit Analytics
Add audit analytics:
```python
class AuditAnalytics:
    def analyze_security_events(self, events: List[Dict]) -> Dict:
        failed_logins = [e for e in events if e['action'] == 'login' and not e['success']]
        suspicious_ips = self._detect_suspicious_ips(events)
        
        return {
            'failed_login_attempts': len(failed_logins),
            'suspicious_ip_addresses': suspicious_ips,
            'risk_score': self._calculate_risk_score(events)
        }
```

## Completion Checklist
- [ ] Secure API runs successfully
- [ ] Authentication works for all user types
- [ ] Authorization properly restricts access
- [ ] Rate limiting prevents abuse
- [ ] Audit logging captures all events
- [ ] Security features tested and verified
- [ ] Error handling works correctly
- [ ] Token expiration handled properly

## Learning Outcomes
After completing this exercise, you will understand:
- JWT-based authentication implementation
- Role-based access control (RBAC) design
- API security best practices
- Audit logging and compliance requirements
- Rate limiting and abuse prevention
- Secure password handling
- Token management and expiration
- Enterprise security patterns

## Next Steps
- Proceed to Exercise 2: Compliance Dashboard
- Explore OAuth 2.0 integration
- Implement multi-factor authentication
- Add advanced threat detection
- Integrate with enterprise identity providers