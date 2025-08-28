# Module 6: Advanced Features and Integration

**Duration:** 20 minutes  
**Objective:** Master Amazon Q's advanced features including workspace integration and specialized use cases

---

## Topic 6.1: Workspace Integration (10 minutes)

### Multi-File Context Awareness

Amazon Q understands your entire project context:
- **Cross-file references:** Imports, dependencies, and relationships
- **Project architecture:** Design patterns and code organization
- **Consistent naming:** Variable and function naming across files
- **Code patterns:** Established conventions and styles

### Workspace-Level Operations

#### Project Analysis
```
"@workspace analyze the overall architecture of this project"
"Review the entire codebase for consistency and best practices"
"Identify dependencies and relationships between modules"
"Suggest improvements for the project structure"
```

#### Cross-File Code Generation
```
"Generate a new service class that integrates with existing database models"
"Create API endpoints that follow the established patterns in this project"
"Add a new feature that works with the current authentication system"
```

#### Refactoring Across Files
```
"Refactor this function to be used across multiple modules"
"Extract common functionality into a shared utility module"
"Update all files to use the new configuration system"
```

### Custom Prompts and Rules

#### Creating Project-Specific Rules
Amazon Q can follow custom rules for your project:

**File:** `.amazonq/rules/coding-standards.md`
```markdown
# Project Coding Standards

## Naming Conventions
- Use snake_case for variables and functions
- Use PascalCase for classes
- Use UPPER_CASE for constants
- Prefix private methods with underscore

## Error Handling
- Always use specific exception types
- Include meaningful error messages
- Log errors with appropriate severity levels
- Never expose internal errors to users

## Documentation
- All public functions must have docstrings
- Include type hints for all parameters
- Add usage examples for complex functions
- Document any side effects or assumptions
```

#### Custom Prompt Templates
**File:** `~/.aws/amazonq/prompts/api-endpoint.md`
```markdown
# API Endpoint Generator

Create a REST API endpoint with the following requirements:
- Follow RESTful conventions
- Include input validation using marshmallow
- Add proper error handling and logging
- Include OpenAPI documentation
- Follow the project's authentication pattern
- Add unit tests with pytest

Endpoint details: {endpoint_description}
```

### Project Context Integration

#### Understanding Project Structure
Amazon Q analyzes:
- **Dependencies:** Requirements files, package.json, pom.xml
- **Configuration:** Config files, environment variables
- **Database schemas:** Migration files, model definitions
- **API documentation:** OpenAPI specs, README files
- **Testing patterns:** Test structure and conventions

#### Maintaining Consistency
```
"Ensure this new code follows the same patterns as existing modules"
"Update the imports to match the project's import style"
"Add logging that's consistent with other components"
"Follow the same error handling approach used elsewhere"
```

---

## Topic 6.2: Specialized Use Cases (10 minutes)

### Infrastructure as Code (IaC)

#### CloudFormation Templates
Amazon Q can generate and optimize AWS CloudFormation:

```yaml
# Example: Generate VPC with security best practices
Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-VPC"
```

#### Terraform Configuration
```hcl
# Example: Generate secure S3 bucket configuration
resource "aws_s3_bucket" "secure_bucket" {
  bucket = var.bucket_name

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_s3_bucket_encryption" "bucket_encryption" {
  bucket = aws_s3_bucket.secure_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

#### Kubernetes Manifests
```yaml
# Example: Generate deployment with best practices
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Database Operations

#### Schema Design
```sql
-- Generate optimized database schema
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

#### Query Optimization
```sql
-- Optimized query with proper indexing
SELECT u.id, u.username, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2023-01-01'
GROUP BY u.id, u.username
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC;
```

#### Migration Scripts
```python
# Alembic migration example
def upgrade():
    op.create_table('user_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_profiles_user_id', 'user_profiles', ['user_id'])
```

### Testing and Test Generation

#### Comprehensive Test Suites
```python
# Generate complete test suite
import pytest
from unittest.mock import Mock, patch
from myapp.services import UserService
from myapp.models import User

class TestUserService:
    @pytest.fixture
    def user_service(self):
        return UserService()
    
    @pytest.fixture
    def sample_user_data(self):
        return {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!'
        }
    
    def test_create_user_success(self, user_service, sample_user_data):
        with patch('myapp.models.User.save') as mock_save:
            user = user_service.create_user(sample_user_data)
            assert user.username == sample_user_data['username']
            mock_save.assert_called_once()
    
    def test_create_user_duplicate_email(self, user_service, sample_user_data):
        with patch('myapp.models.User.get_by_email') as mock_get:
            mock_get.return_value = Mock()
            
            with pytest.raises(ValueError, match="Email already exists"):
                user_service.create_user(sample_user_data)
```

#### Integration Tests
```python
# API integration tests
def test_user_registration_flow(client, db):
    # Test complete user registration workflow
    response = client.post('/api/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'SecurePass123!'
    })
    
    assert response.status_code == 201
    assert 'user_id' in response.json
    
    # Verify user was created in database
    user = User.query.filter_by(email='new@example.com').first()
    assert user is not None
    assert user.username == 'newuser'
```

#### Performance Tests
```python
# Load testing with locust
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login before running tasks
        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        self.token = response.json()["token"]
    
    @task(3)
    def view_homepage(self):
        self.client.get("/")
    
    @task(1)
    def view_profile(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/profile", headers=headers)
```

### DevOps and CI/CD Integration

#### GitHub Actions Workflows
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=myapp --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

#### Docker Configuration
```dockerfile
# Multi-stage Docker build
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myapp:app"]
```

---

## Hands-On Exercise 6.1: Workspace Integration

### Objective
Master Amazon Q's workspace-level operations and project context awareness.

### Task 1: Project Analysis and Architecture Review (5 minutes)

**Setup Multi-File Project:**
```bash
mkdir ecommerce-project
cd ecommerce-project
mkdir -p {models,services,api,tests,config}
```

**Create project files:**

**File:** `models/user.py`
```python
from datetime import datetime
from typing import Optional

class User:
    def __init__(self, username: str, email: str, password_hash: str):
        self.id: Optional[int] = None
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.utcnow()
        self.is_active = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }
```

**File:** `models/product.py`
```python
from decimal import Decimal
from typing import Optional

class Product:
    def __init__(self, name: str, price: Decimal, category: str):
        self.id: Optional[int] = None
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = 0
        self.is_available = True
```

**File:** `services/user_service.py`
```python
from models.user import User
import bcrypt

class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_user(self, username: str, email: str, password: str) -> User:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User(username, email, password_hash.decode())
        # Save to database logic here
        return user
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        # Authentication logic here
        pass
```

**Amazon Q Workspace Tasks:**

1. **Project Architecture Analysis:**
```
@workspace Analyze the overall architecture of this e-commerce project and suggest improvements for scalability and maintainability
```

2. **Cross-File Integration:**
```
@workspace Create a new OrderService that integrates with the existing User and Product models, following the same patterns
```

3. **Consistency Review:**
```
@workspace Review all files for naming consistency and suggest standardizations across the project
```

### Task 2: Custom Rules and Patterns (5 minutes)

**Create Custom Rules:**

**File:** `.amazonq/rules/project-standards.md`
```markdown
# E-commerce Project Standards

## Architecture Patterns
- Use dependency injection for services
- Implement repository pattern for data access
- Follow MVC architecture for API endpoints
- Use factory pattern for model creation

## Error Handling
- Create custom exception classes
- Use structured logging with correlation IDs
- Return consistent error response format
- Never expose internal errors to API responses

## Testing Requirements
- Minimum 80% code coverage
- Use pytest fixtures for test data
- Mock external dependencies
- Include integration tests for API endpoints
```

**Amazon Q Custom Rules Tasks:**

1. **Apply Project Standards:**
```
Following the project standards in .amazonq/rules/, create a new PaymentService with proper error handling and testing
```

2. **Generate Consistent Code:**
```
Create API endpoints for user management that follow the established patterns and standards
```

---

## Hands-On Exercise 6.2: Specialized Use Cases

### Objective
Master Amazon Q's capabilities for Infrastructure as Code, database operations, and testing.

### Task 1: Infrastructure as Code Generation (5 minutes)

**Amazon Q IaC Tasks:**

1. **AWS CloudFormation:**
```
Generate a CloudFormation template for a secure web application infrastructure including VPC, subnets, security groups, ALB, and ECS service with best practices
```

2. **Terraform Configuration:**
```
Create Terraform configuration for a multi-environment setup (dev, staging, prod) with S3 backend, proper tagging, and security configurations
```

3. **Kubernetes Deployment:**
```
Generate Kubernetes manifests for deploying a microservices application with proper resource limits, health checks, and service mesh configuration
```

### Task 2: Database Schema and Operations (5 minutes)

**Amazon Q Database Tasks:**

1. **Schema Design:**
```
Design a complete database schema for the e-commerce project including users, products, orders, payments with proper relationships, indexes, and constraints
```

2. **Migration Scripts:**
```
Create database migration scripts to add a new inventory tracking system to the existing schema
```

3. **Query Optimization:**
```
Generate optimized queries for common e-commerce operations like product search, order history, and sales reporting with proper indexing strategies
```

---

## Advanced Integration Patterns

### 1. Microservices Architecture

#### Service Communication
```python
# Event-driven communication
from dataclasses import dataclass
from typing import Dict, Any
import json

@dataclass
class DomainEvent:
    event_type: str
    aggregate_id: str
    data: Dict[str, Any]
    version: int = 1

class EventPublisher:
    def __init__(self, message_broker):
        self.broker = message_broker
    
    def publish(self, event: DomainEvent):
        message = {
            'event_type': event.event_type,
            'aggregate_id': event.aggregate_id,
            'data': event.data,
            'version': event.version,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.broker.publish(
            topic=f"events.{event.event_type}",
            message=json.dumps(message)
        )
```

#### API Gateway Integration
```python
# AWS Lambda handler for API Gateway
import json
from typing import Dict, Any

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    try:
        # Extract request data
        http_method = event['httpMethod']
        path = event['path']
        body = json.loads(event.get('body', '{}'))
        
        # Route to appropriate handler
        if path == '/users' and http_method == 'POST':
            result = create_user(body)
        elif path.startswith('/users/') and http_method == 'GET':
            user_id = path.split('/')[-1]
            result = get_user(user_id)
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Not found'})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
```

### 2. Monitoring and Observability

#### Structured Logging
```python
import logging
import json
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        
        handler = logging.StreamHandler()
        handler.setFormatter(self.JsonFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'service': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            }
            
            if hasattr(record, 'correlation_id'):
                log_entry['correlation_id'] = record.correlation_id
            
            if hasattr(record, 'user_id'):
                log_entry['user_id'] = record.user_id
            
            return json.dumps(log_entry)
    
    def info(self, message: str, **kwargs):
        extra = {k: v for k, v in kwargs.items()}
        self.logger.info(message, extra=extra)
```

#### Metrics Collection
```python
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active database connections')

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            REQUEST_COUNT.labels(method='POST', endpoint='/api/users', status='200').inc()
            return result
        except Exception as e:
            REQUEST_COUNT.labels(method='POST', endpoint='/api/users', status='500').inc()
            raise
        finally:
            REQUEST_DURATION.observe(time.time() - start_time)
    
    return wrapper
```

---

## Integration Best Practices

### 1. Configuration Management
- Use environment-specific configuration files
- Implement configuration validation
- Support configuration hot-reloading
- Secure sensitive configuration data

### 2. Error Handling and Resilience
- Implement circuit breaker patterns
- Add retry mechanisms with exponential backoff
- Use bulkhead isolation for critical resources
- Implement graceful degradation

### 3. Security Integration
- Implement OAuth 2.0/OpenID Connect
- Use API rate limiting and throttling
- Add request/response validation
- Implement audit logging

### 4. Performance Optimization
- Implement caching strategies
- Use connection pooling
- Add database query optimization
- Implement async processing where appropriate

---

## Key Takeaways

After Module 6, you should be able to:
- Leverage Amazon Q's workspace-level context awareness
- Create custom rules and prompts for project consistency
- Generate Infrastructure as Code with best practices
- Design and optimize database schemas and queries
- Create comprehensive testing strategies
- Integrate Amazon Q into DevOps workflows
- Apply advanced architectural patterns

**Time Required:** 20 minutes  
**Difficulty:** Advanced  
**Next:** Module 7 - Practical Project Integration