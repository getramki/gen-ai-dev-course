# Exercise 1: Workspace Integration

## Objective
Master Amazon Q's workspace-level operations, multi-file context awareness, and custom rules implementation.

**Time:** 10 minutes  
**Difficulty:** Advanced

---

## Setup Instructions

### Create Multi-File Project Structure
```bash
mkdir advanced-ecommerce
cd advanced-ecommerce
mkdir -p {src/{models,services,api,utils},tests/{unit,integration},config,docs,.amazonq/rules}
```

---

## Part A: Multi-File Context Awareness (5 minutes)

### Task A1: Create Interconnected Project Files

**Create the core project structure:**

**File:** `src/models/base.py`
```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

class BaseModel(ABC):
    """Base model with common functionality"""
    
    def __init__(self):
        self.id: Optional[str] = None
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()
        self.version: int = 1
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate model data"""
        pass
    
    def generate_id(self) -> str:
        """Generate unique identifier"""
        return str(uuid.uuid4())
    
    def update_timestamp(self):
        """Update the last modified timestamp"""
        self.updated_at = datetime.utcnow()
        self.version += 1
```

**File:** `src/models/user.py`
```python
from typing import Optional, List, Dict, Any
from .base import BaseModel
import re

class User(BaseModel):
    """User model with validation and business logic"""
    
    def __init__(self, username: str, email: str, password_hash: str):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = True
        self.roles: List[str] = ['user']
        self.profile: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'roles': self.roles,
            'profile': self.profile,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'version': self.version
        }
    
    def validate(self) -> bool:
        # Username validation
        if not self.username or len(self.username) < 3:
            return False
        
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            return False
        
        return True
    
    def add_role(self, role: str):
        if role not in self.roles:
            self.roles.append(role)
            self.update_timestamp()
    
    def has_role(self, role: str) -> bool:
        return role in self.roles
```

**File:** `src/models/product.py`
```python
from decimal import Decimal
from typing import Optional, Dict, Any, List
from .base import BaseModel

class Product(BaseModel):
    """Product model with inventory and pricing logic"""
    
    def __init__(self, name: str, price: Decimal, category: str, description: str = ""):
        super().__init__()
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.stock_quantity = 0
        self.is_available = True
        self.tags: List[str] = []
        self.attributes: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'category': self.category,
            'description': self.description,
            'stock_quantity': self.stock_quantity,
            'is_available': self.is_available,
            'tags': self.tags,
            'attributes': self.attributes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'version': self.version
        }
    
    def validate(self) -> bool:
        if not self.name or len(self.name.strip()) == 0:
            return False
        
        if self.price <= 0:
            return False
        
        if not self.category:
            return False
        
        return True
    
    def update_stock(self, quantity: int):
        self.stock_quantity = max(0, self.stock_quantity + quantity)
        self.is_available = self.stock_quantity > 0
        self.update_timestamp()
    
    def is_in_stock(self, requested_quantity: int = 1) -> bool:
        return self.stock_quantity >= requested_quantity and self.is_available
```

**File:** `src/services/base_service.py`
```python
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, TypeVar, Generic
import logging

T = TypeVar('T')

class BaseService(ABC, Generic[T]):
    """Base service class with common operations"""
    
    def __init__(self, repository, logger_name: str):
        self.repository = repository
        self.logger = logging.getLogger(logger_name)
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> T:
        """Create new entity"""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    def update(self, entity_id: str, data: Dict[str, Any]) -> Optional[T]:
        """Update existing entity"""
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        pass
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        """Get all entities with pagination"""
        return self.repository.find_all(limit=limit, offset=offset)
    
    def search(self, criteria: Dict[str, Any]) -> List[T]:
        """Search entities by criteria"""
        return self.repository.find_by_criteria(criteria)
```

**Amazon Q Workspace Analysis Tasks:**

1. **Project Architecture Review:**
```
@workspace Analyze the current project structure and identify the design patterns being used. Suggest improvements for scalability and maintainability.
```

2. **Cross-File Dependency Analysis:**
```
@workspace Review the relationships between models and services. Identify any circular dependencies or architectural issues.
```

3. **Consistency Assessment:**
```
@workspace Check all files for naming consistency, coding style, and adherence to Python best practices. Suggest standardizations.
```

### Task A2: Generate Integrated Components

**Amazon Q Integration Tasks:**

1. **Service Layer Generation:**
```
@workspace Create a UserService class that extends BaseService and integrates with the User model, following the established patterns and including proper error handling
```

2. **Repository Pattern Implementation:**
```
@workspace Generate repository classes for User and Product models that follow the repository pattern and integrate with the existing service architecture
```

3. **API Layer Creation:**
```
@workspace Create Flask API endpoints for user and product management that integrate with the existing services and follow RESTful conventions
```

**Expected Generated Components:**
- UserService with CRUD operations
- ProductService with inventory management
- UserRepository and ProductRepository
- API controllers with proper error handling
- Integration between all layers

---

## Part B: Custom Rules and Project Standards (5 minutes)

### Task B1: Define Project-Specific Rules

**Create Custom Rules File:**

**File:** `.amazonq/rules/coding-standards.md`
```markdown
# Advanced E-commerce Project Standards

## Architecture Principles
- Follow Domain-Driven Design (DDD) principles
- Implement Clean Architecture with clear layer separation
- Use dependency injection for all services
- Apply SOLID principles throughout the codebase

## Code Organization
- Models in `src/models/` with base class inheritance
- Services in `src/services/` implementing business logic
- Repositories in `src/repositories/` for data access
- API controllers in `src/api/` for HTTP handling
- Utilities in `src/utils/` for shared functionality

## Naming Conventions
- Classes: PascalCase (e.g., UserService, ProductRepository)
- Functions/Methods: snake_case (e.g., create_user, get_by_id)
- Constants: UPPER_SNAKE_CASE (e.g., MAX_RETRY_ATTEMPTS)
- Private methods: prefix with underscore (e.g., _validate_input)

## Error Handling Standards
- Create custom exception hierarchy
- Use specific exception types for different error categories
- Include correlation IDs in all error logs
- Never expose internal errors in API responses
- Implement proper error recovery mechanisms

## Testing Requirements
- Minimum 85% code coverage
- Unit tests for all business logic
- Integration tests for API endpoints
- Use pytest fixtures for test data setup
- Mock external dependencies in unit tests

## Documentation Standards
- All public methods must have comprehensive docstrings
- Include type hints for all parameters and return values
- Add usage examples for complex functionality
- Document any side effects or assumptions
- Maintain API documentation with OpenAPI specs

## Security Requirements
- Validate all input data
- Use parameterized queries for database operations
- Implement proper authentication and authorization
- Log all security-relevant events
- Follow OWASP security guidelines
```

**File:** `.amazonq/rules/api-standards.md`
```markdown
# API Development Standards

## RESTful Design
- Use proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Implement consistent URL patterns (/api/v1/resource/{id})
- Return appropriate HTTP status codes
- Use JSON for request/response bodies
- Implement proper pagination for list endpoints

## Request/Response Format
- Use consistent error response structure
- Include metadata in list responses (total, page, limit)
- Implement request validation with detailed error messages
- Support content negotiation (Accept headers)
- Include correlation IDs in all responses

## Authentication & Authorization
- Use JWT tokens for stateless authentication
- Implement role-based access control (RBAC)
- Add rate limiting to prevent abuse
- Log all authentication attempts
- Secure sensitive endpoints with proper authorization

## Performance Standards
- Implement response caching where appropriate
- Use database connection pooling
- Add request/response compression
- Implement async processing for long-running operations
- Monitor and log performance metrics
```

### Task B2: Apply Custom Rules

**Amazon Q Custom Rules Tasks:**

1. **Generate Code Following Standards:**
```
Following the coding standards in .amazonq/rules/, create a complete OrderService with order processing logic, payment integration, and inventory management
```

2. **API Implementation with Standards:**
```
Using the API standards defined in .amazonq/rules/, create RESTful endpoints for order management with proper validation, error handling, and documentation
```

3. **Testing Suite Generation:**
```
Generate comprehensive test suites following the testing requirements in the project standards, including unit tests, integration tests, and fixtures
```

### Task B3: Custom Prompt Templates

**Create Custom Prompt:**

**File:** `~/.aws/amazonq/prompts/service-generator.md`
```markdown
# Service Class Generator

Generate a service class with the following specifications:

## Requirements
- Extend BaseService<T> where T is the model type
- Implement all abstract methods from BaseService
- Add business logic specific to the domain entity
- Include proper error handling with custom exceptions
- Add comprehensive logging with correlation IDs
- Implement input validation for all operations
- Follow the project's coding standards and naming conventions

## Additional Features
- Add caching for frequently accessed data
- Implement audit logging for all modifications
- Add metrics collection for performance monitoring
- Include batch operations where applicable
- Support soft delete functionality

## Testing Requirements
- Generate corresponding unit tests with pytest
- Include test fixtures for model instances
- Mock repository dependencies
- Test all error conditions and edge cases
- Achieve minimum 85% code coverage

Service Details: {service_description}
Model Type: {model_type}
Special Requirements: {special_requirements}
```

**Amazon Q Custom Prompt Tasks:**

1. **Use Custom Prompt:**
```
@service-generator Create a PaymentService for processing payments with integration to external payment gateways, fraud detection, and transaction logging
```

2. **Generate with Template:**
```
Using the service-generator prompt, create an InventoryService that manages product stock levels, handles reservations, and tracks inventory movements
```

---

## Workspace Integration Verification

### Task: Verify Integration Quality

**Amazon Q Verification Tasks:**

1. **Cross-File Consistency Check:**
```
@workspace Verify that all generated services, repositories, and API endpoints follow consistent patterns and integrate properly with existing code
```

2. **Architecture Validation:**
```
@workspace Validate that the overall architecture follows Clean Architecture principles and identify any violations or improvements needed
```

3. **Dependency Analysis:**
```
@workspace Analyze all dependencies between components and suggest improvements for loose coupling and high cohesion
```

4. **Code Quality Assessment:**
```
@workspace Review the entire codebase for code quality issues, potential bugs, and adherence to the defined coding standards
```

---

## Integration Patterns Demonstrated

### 1. Layered Architecture
- **Models:** Domain entities with business rules
- **Services:** Business logic and orchestration
- **Repositories:** Data access abstraction
- **API:** HTTP interface and request handling

### 2. Dependency Injection
- Services depend on repository interfaces
- Controllers depend on service interfaces
- Easy testing with mock implementations

### 3. Cross-Cutting Concerns
- Logging integrated across all layers
- Error handling with custom exceptions
- Validation at appropriate boundaries
- Audit trails for all operations

### 4. Consistency Patterns
- Base classes for common functionality
- Consistent naming conventions
- Standardized error handling
- Uniform API response formats

---

## Success Criteria

You've mastered workspace integration when you can:
- [ ] Generate code that integrates seamlessly with existing project structure
- [ ] Create custom rules that enforce project standards
- [ ] Use Amazon Q to maintain consistency across multiple files
- [ ] Leverage workspace context for intelligent code generation
- [ ] Apply architectural patterns consistently throughout the project
- [ ] Generate comprehensive test suites that follow project standards

**Integration Quality Indicators:**
- ✅ All generated code follows established patterns
- ✅ Cross-file references are correctly maintained
- ✅ Custom rules are consistently applied
- ✅ Architecture principles are preserved
- ✅ Code quality standards are met
- ✅ Test coverage meets project requirements

**Completion Time:** 10 minutes  
**Next:** Exercise 2 - Specialized Use Cases