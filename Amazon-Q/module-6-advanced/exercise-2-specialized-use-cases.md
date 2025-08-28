# Exercise 2: Specialized Use Cases

## Objective
Master Amazon Q's capabilities for Infrastructure as Code, database operations, testing strategies, and DevOps integration.

**Time:** 10 minutes  
**Difficulty:** Advanced

---

## Setup Instructions

### Create Specialized Project Structure
```bash
mkdir specialized-systems
cd specialized-systems
mkdir -p {infrastructure/{aws,terraform,kubernetes},database/{schemas,migrations,queries},testing/{unit,integration,performance},devops/{ci-cd,monitoring,deployment}}
```

---

## Part A: Infrastructure as Code (3 minutes)

### Task A1: AWS CloudFormation Generation

**Amazon Q CloudFormation Tasks:**

1. **Complete Web Application Infrastructure:**
```
Generate a comprehensive CloudFormation template for a scalable web application including:
- VPC with public and private subnets across 3 AZs
- Application Load Balancer with SSL termination
- ECS Fargate cluster with auto-scaling
- RDS PostgreSQL with Multi-AZ deployment
- ElastiCache Redis cluster
- S3 bucket for static assets with CloudFront
- IAM roles and security groups with least privilege
- CloudWatch monitoring and alarms
```

2. **Microservices Infrastructure:**
```
Create CloudFormation templates for a microservices architecture with:
- API Gateway with custom domain and throttling
- Lambda functions with proper IAM roles
- DynamoDB tables with GSI and auto-scaling
- SQS queues for async processing
- SNS topics for event notifications
- Secrets Manager for sensitive configuration
- X-Ray tracing for distributed monitoring
```

**Expected CloudFormation Structure:**
```yaml
# Example output structure
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Scalable web application infrastructure'

Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
  
Resources:
  # VPC and Networking
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Sub '10.${Environment}.0.0/16'
      EnableDnsHostnames: true
      EnableDnsSupport: true
  
  # Security Groups
  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for Application Load Balancer
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
  
  # Application Load Balancer
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Type: application
      Scheme: internet-facing
      SecurityGroups:
        - !Ref ALBSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
```

### Task A2: Terraform Configuration

**Amazon Q Terraform Tasks:**

1. **Multi-Environment Infrastructure:**
```
Generate Terraform configuration for multi-environment deployment with:
- Modular structure for reusability
- Environment-specific variable files
- Remote state management with S3 backend
- Proper resource tagging strategy
- Data sources for existing resources
- Local values for computed configurations
```

2. **Kubernetes Cluster Setup:**
```
Create Terraform configuration for EKS cluster with:
- Managed node groups with different instance types
- IRSA (IAM Roles for Service Accounts) setup
- VPC CNI and CoreDNS add-ons
- Cluster autoscaler configuration
- AWS Load Balancer Controller
- External DNS for automatic DNS management
```

**Expected Terraform Structure:**
```hcl
# Example output structure
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

module "vpc" {
  source = "./modules/vpc"
  
  environment = var.environment
  cidr_block  = var.vpc_cidr
  
  tags = local.common_tags
}

module "eks" {
  source = "./modules/eks"
  
  cluster_name = "${var.project_name}-${var.environment}"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  
  tags = local.common_tags
}
```

### Task A3: Kubernetes Manifests

**Amazon Q Kubernetes Tasks:**

1. **Complete Application Deployment:**
```
Generate Kubernetes manifests for a microservices application including:
- Namespace with resource quotas and network policies
- Deployments with proper resource limits and health checks
- Services (ClusterIP, NodePort, LoadBalancer)
- Ingress with TLS termination and path-based routing
- ConfigMaps and Secrets for configuration
- HorizontalPodAutoscaler for auto-scaling
- PodDisruptionBudget for high availability
- ServiceMonitor for Prometheus monitoring
```

**Expected Kubernetes Structure:**
```yaml
# Example output structure
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-app
  labels:
    name: ecommerce-app
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: ecommerce-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: user-service:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
```

---

## Part B: Database Operations (3 minutes)

### Task B1: Schema Design and Optimization

**Amazon Q Database Schema Tasks:**

1. **E-commerce Database Schema:**
```
Design a comprehensive e-commerce database schema with:
- Users, products, orders, payments, inventory tables
- Proper relationships with foreign keys and constraints
- Indexes for query optimization
- Partitioning strategy for large tables
- Audit trails for data changes
- Full-text search capabilities
- Data archiving strategy for old records
```

2. **Performance Optimization:**
```
Create optimized database schema with:
- Composite indexes for complex queries
- Materialized views for reporting
- Proper data types for storage efficiency
- Normalization vs denormalization decisions
- Sharding strategy for horizontal scaling
- Read replicas configuration
```

**Expected Schema Structure:**
```sql
-- Example output structure
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;

-- Full-text search index
CREATE INDEX idx_users_search ON users USING gin(to_tsvector('english', first_name || ' ' || last_name || ' ' || username));
```

### Task B2: Migration Scripts

**Amazon Q Migration Tasks:**

1. **Database Migration Strategy:**
```
Generate database migration scripts for:
- Adding new tables with proper constraints
- Modifying existing columns with data preservation
- Creating and dropping indexes safely
- Data migration between table structures
- Rollback procedures for failed migrations
- Zero-downtime deployment strategies
```

2. **Version Control Integration:**
```
Create migration system with:
- Sequential migration numbering
- Dependency tracking between migrations
- Automated rollback capabilities
- Migration status tracking
- Environment-specific migrations
- Data seeding for development/testing
```

### Task B3: Query Optimization

**Amazon Q Query Optimization Tasks:**

1. **Complex Query Optimization:**
```
Generate optimized queries for:
- Product search with filters and sorting
- Order history with pagination and aggregations
- Sales reporting with time-based grouping
- Inventory tracking with real-time updates
- User analytics with behavioral data
- Performance monitoring queries
```

**Expected Query Structure:**
```sql
-- Example optimized query
WITH product_stats AS (
    SELECT 
        p.id,
        p.name,
        p.category_id,
        AVG(r.rating) as avg_rating,
        COUNT(r.id) as review_count,
        SUM(oi.quantity) as total_sold
    FROM products p
    LEFT JOIN reviews r ON p.id = r.product_id
    LEFT JOIN order_items oi ON p.id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.id 
        AND o.status = 'completed'
        AND o.created_at >= CURRENT_DATE - INTERVAL '30 days'
    WHERE p.is_active = true
    GROUP BY p.id, p.name, p.category_id
)
SELECT 
    ps.*,
    c.name as category_name,
    RANK() OVER (PARTITION BY ps.category_id ORDER BY ps.total_sold DESC) as sales_rank
FROM product_stats ps
JOIN categories c ON ps.category_id = c.id
WHERE ps.avg_rating >= 4.0
ORDER BY ps.total_sold DESC, ps.avg_rating DESC
LIMIT 50;
```

---

## Part C: Testing Strategies (2 minutes)

### Task C1: Comprehensive Test Suite Generation

**Amazon Q Testing Tasks:**

1. **Multi-Layer Testing Strategy:**
```
Generate comprehensive test suite including:
- Unit tests for business logic with high coverage
- Integration tests for API endpoints and database operations
- Contract tests for service interactions
- End-to-end tests for critical user journeys
- Performance tests for load and stress testing
- Security tests for vulnerability assessment
```

2. **Test Data Management:**
```
Create test data management system with:
- Factory pattern for test object creation
- Fixtures for consistent test data setup
- Database seeding for integration tests
- Test data cleanup and isolation
- Parameterized tests for multiple scenarios
- Mock services for external dependencies
```

**Expected Test Structure:**
```python
# Example test structure
import pytest
from unittest.mock import Mock, patch
from factories import UserFactory, ProductFactory
from services import UserService, ProductService

class TestUserService:
    @pytest.fixture
    def user_service(self, mock_user_repository):
        return UserService(mock_user_repository)
    
    @pytest.fixture
    def mock_user_repository(self):
        return Mock()
    
    @pytest.mark.parametrize("username,email,expected", [
        ("validuser", "valid@example.com", True),
        ("", "valid@example.com", False),
        ("validuser", "invalid-email", False),
    ])
    def test_create_user_validation(self, user_service, username, email, expected):
        user_data = {
            'username': username,
            'email': email,
            'password': 'SecurePass123!'
        }
        
        if expected:
            user = user_service.create_user(user_data)
            assert user.username == username
        else:
            with pytest.raises(ValidationError):
                user_service.create_user(user_data)
```

### Task C2: Performance and Load Testing

**Amazon Q Performance Testing Tasks:**

1. **Load Testing Suite:**
```
Generate performance tests using Locust for:
- API endpoint load testing with realistic user behavior
- Database performance testing under concurrent load
- Memory and CPU usage monitoring during tests
- Bottleneck identification and reporting
- Scalability testing with increasing load
- Stress testing to find breaking points
```

---

## Part D: DevOps Integration (2 minutes)

### Task D1: CI/CD Pipeline Generation

**Amazon Q DevOps Tasks:**

1. **GitHub Actions Workflow:**
```
Create comprehensive CI/CD pipeline with:
- Multi-stage builds (test, build, deploy)
- Parallel job execution for faster builds
- Environment-specific deployments
- Automated testing at each stage
- Security scanning and vulnerability assessment
- Artifact management and versioning
- Rollback capabilities for failed deployments
```

2. **Monitoring and Observability:**
```
Generate monitoring setup with:
- Application metrics collection with Prometheus
- Log aggregation with ELK stack
- Distributed tracing with Jaeger
- Health checks and alerting rules
- Dashboard creation with Grafana
- SLA monitoring and reporting
```

**Expected CI/CD Structure:**
```yaml
# Example GitHub Actions workflow
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

---

## Integration Verification Tasks

### Task: End-to-End Integration Testing

**Amazon Q Integration Verification:**

1. **Infrastructure Validation:**
```
@workspace Validate that all generated infrastructure components (CloudFormation, Terraform, Kubernetes) work together and follow best practices for security and scalability
```

2. **Database Integration Check:**
```
Verify that the database schema, migrations, and queries integrate properly with the application code and support the required performance characteristics
```

3. **Testing Strategy Validation:**
```
Review the generated test suites to ensure they provide comprehensive coverage and integrate with the CI/CD pipeline for automated quality assurance
```

4. **DevOps Pipeline Assessment:**
```
Analyze the CI/CD pipeline to ensure it supports the complete development lifecycle from code commit to production deployment with proper monitoring and rollback capabilities
```

---

## Specialized Use Case Patterns

### 1. Infrastructure as Code Patterns
- **Modular Design:** Reusable components across environments
- **Environment Parity:** Consistent infrastructure across dev/staging/prod
- **Security by Default:** Least privilege and defense in depth
- **Monitoring Integration:** Built-in observability and alerting

### 2. Database Design Patterns
- **Performance Optimization:** Proper indexing and query optimization
- **Scalability Planning:** Partitioning and sharding strategies
- **Data Integrity:** Constraints and validation at database level
- **Migration Safety:** Zero-downtime deployment strategies

### 3. Testing Patterns
- **Test Pyramid:** Unit tests > Integration tests > E2E tests
- **Test Data Management:** Factories, fixtures, and cleanup
- **Continuous Testing:** Automated testing in CI/CD pipeline
- **Performance Testing:** Load testing integrated into development cycle

### 4. DevOps Patterns
- **GitOps:** Infrastructure and application deployment through Git
- **Observability:** Metrics, logs, and traces for system health
- **Security Integration:** Security scanning and compliance checks
- **Automated Recovery:** Self-healing systems and automated rollbacks

---

## Success Criteria

You've mastered specialized use cases when you can:
- [ ] Generate production-ready infrastructure code with best practices
- [ ] Design optimized database schemas and queries
- [ ] Create comprehensive testing strategies for all application layers
- [ ] Implement complete CI/CD pipelines with monitoring and observability
- [ ] Integrate all components into a cohesive system architecture
- [ ] Apply security and performance best practices across all domains

**Specialization Quality Indicators:**
- ✅ Infrastructure follows cloud best practices and security standards
- ✅ Database design supports performance and scalability requirements
- ✅ Testing strategy provides comprehensive coverage and fast feedback
- ✅ CI/CD pipeline enables reliable and frequent deployments
- ✅ Monitoring and observability provide actionable insights
- ✅ All components integrate seamlessly for end-to-end functionality

**Completion Time:** 10 minutes  
**Next:** Module 7 - Practical Project Integration