# Exercise 2: Production Deployment

## Objective
Deploy a scalable, production-ready LangChain service with comprehensive monitoring, health checks, and enterprise-grade features.

## Time Estimate
15 minutes

## Prerequisites
- Completed Exercise 1
- Docker installed (optional)
- AWS credentials configured
- Basic understanding of REST APIs

## Step-by-Step Instructions

### Step 1: Understand the Production Architecture
1. **Review the service components**:
   - Flask REST API with multiple endpoints
   - CloudWatch metrics integration
   - Health checks and monitoring
   - Error handling and logging
   - Batch processing capabilities

2. **Examine the deployment options**:
   - Local development server
   - Docker containerization
   - Docker Compose with Nginx
   - Kubernetes deployment (configuration provided)

### Step 2: Run the Production Service Locally
```bash
cd module6
python exercise_2_production_deployment.py
```

**Expected Output**:
- Configuration display
- Deployment files creation
- API initialization
- LLM connectivity test
- Deployment instructions

### Step 3: Test the API Endpoints
1. **Start the API server**:
   ```bash
   python exercise_2_production_deployment.py run
   ```

2. **Test health endpoint** (in another terminal):
   ```bash
   curl http://localhost:8000/health
   ```

3. **Test processing endpoint**:
   ```bash
   curl -X POST http://localhost:8000/process \
     -H "Content-Type: application/json" \
     -d '{"input": "Explain quantum computing", "task_type": "summarize"}'
   ```

4. **Test metrics endpoint**:
   ```bash
   curl http://localhost:8000/metrics
   ```

5. **Test batch processing**:
   ```bash
   curl -X POST http://localhost:8000/batch \
     -H "Content-Type: application/json" \
     -d '{
       "requests": [
         {"input": "What is AI?", "task_type": "qa"},
         {"input": "Explain machine learning", "task_type": "summarize"}
       ]
     }'
   ```

### Step 4: Deploy with Docker
1. **Build the Docker image**:
   ```bash
   docker build -t langchain-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 \
     -e MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0 \
     -e TEMPERATURE=0.1 \
     -v ~/.aws:/home/appuser/.aws:ro \
     langchain-api
   ```

3. **Test the containerized service**:
   ```bash
   curl http://localhost:8000/health
   ```

### Step 5: Deploy with Docker Compose
1. **Start the full stack**:
   ```bash
   docker-compose up -d
   ```

2. **Check service status**:
   ```bash
   docker-compose ps
   docker-compose logs langchain-api
   ```

3. **Test through Nginx proxy**:
   ```bash
   curl http://localhost/health
   curl -X POST http://localhost/process \
     -H "Content-Type: application/json" \
     -d '{"input": "Test message", "task_type": "general"}'
   ```

### Step 6: Monitor and Debug
1. **Check application logs**:
   ```bash
   docker-compose logs -f langchain-api
   ```

2. **Monitor metrics**:
   ```bash
   # Create a simple monitoring script
   while true; do
     curl -s http://localhost/metrics | jq '.'
     sleep 30
   done
   ```

3. **Health monitoring**:
   ```bash
   # Continuous health check
   watch -n 5 'curl -s http://localhost/health | jq ".status"'
   ```

### Step 7: Load Testing
1. **Install load testing tool**:
   ```bash
   pip install locust
   ```

2. **Create load test script** (`locustfile.py`):
   ```python
   from locust import HttpUser, task, between
   import json

   class LangChainUser(HttpUser):
       wait_time = between(1, 3)
       
       @task(3)
       def process_request(self):
           self.client.post("/process", json={
               "input": "What is artificial intelligence?",
               "task_type": "qa"
           })
       
       @task(1)
       def health_check(self):
           self.client.get("/health")
       
       @task(1)
       def get_metrics(self):
           self.client.get("/metrics")
   ```

3. **Run load test**:
   ```bash
   locust -f locustfile.py --host=http://localhost:8000
   ```

### Step 8: Production Optimizations
1. **Add environment-specific configuration**:
   ```python
   # config.py
   import os

   class Config:
       MODEL_ID = os.environ.get('MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
       TEMPERATURE = float(os.environ.get('TEMPERATURE', '0.1'))
       MAX_TOKENS = int(os.environ.get('MAX_TOKENS', '1000'))
       LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
       ENABLE_METRICS = os.environ.get('ENABLE_METRICS', 'true').lower() == 'true'
   ```

2. **Add request validation**:
   ```python
   from marshmallow import Schema, fields, ValidationError

   class ProcessRequestSchema(Schema):
       input = fields.Str(required=True, validate=lambda x: len(x) > 0)
       task_type = fields.Str(missing='general')
       max_tokens = fields.Int(missing=1000, validate=lambda x: 1 <= x <= 4000)
   ```

3. **Add rate limiting**:
   ```python
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address

   limiter = Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["100 per hour"]
   )

   @app.route('/process', methods=['POST'])
   @limiter.limit("10 per minute")
   def process_request():
       # ... existing code
   ```

## Expected Output

### Successful Deployment
```
=== Production Deployment Demo ===

1. Configuration:
{
  "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
  "temperature": 0.1,
  "max_tokens": 1000,
  "region": "us-east-1",
  "version": "1.0.0"
}

2. Creating deployment files...
Created Dockerfile
Created requirements.txt
Created docker-compose.yml
Created nginx.conf

3. Initializing Production API...
✓ API initialized successfully
✓ LLM processing test: Success
  Result preview: Machine learning is a subset of artificial intelligence that enables computers to learn...

4. Deployment Instructions:
   Local Development:
   python exercise_2_production_deployment.py run

   Docker Deployment:
   docker build -t langchain-api .
   docker run -p 8000:8000 langchain-api

   Docker Compose (with Nginx):
   docker-compose up -d

5. Available Endpoints:
   GET /health      - Health check and service status
   GET /metrics     - Performance metrics and statistics
   POST /process    - Single request processing
   POST /batch      - Batch request processing

6. Monitoring Features:
   ✓ CloudWatch metrics integration
   ✓ Structured logging with request IDs
   ✓ Health checks with LLM connectivity test
   ✓ Performance metrics tracking
   ✓ Error rate monitoring
   ✓ Response time tracking
```

### API Response Examples
```json
// Health Check Response
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "uptime_seconds": 3600,
  "llm_status": "connected",
  "version": "1.0.0"
}

// Process Response
{
  "success": true,
  "result": "Quantum computing is a revolutionary computing paradigm...",
  "task_type": "summarize",
  "request_id": "req_1705315800000",
  "response_time": 2.345
}

// Metrics Response
{
  "requests_total": 150,
  "requests_success": 147,
  "requests_error": 3,
  "success_rate_percent": 98.0,
  "avg_response_time_seconds": 1.85,
  "uptime_seconds": 7200
}
```

## Common Issues and Solutions

### Issue 1: Docker Build Failures
**Problem**: Docker build fails with dependency errors
**Solution**: 
- Ensure requirements.txt is complete
- Check Python version compatibility
- Verify AWS credentials are properly mounted

### Issue 2: Health Check Failures
**Problem**: Health endpoint returns unhealthy status
**Solution**:
- Check AWS Bedrock permissions
- Verify model ID is correct and available
- Check network connectivity to AWS services

### Issue 3: High Response Times
**Problem**: API responses are slow
**Solution**:
- Monitor CloudWatch metrics
- Optimize model selection based on task complexity
- Implement response caching
- Consider using faster models for simple tasks

### Issue 4: Memory Issues
**Problem**: Container runs out of memory
**Solution**:
- Increase Docker memory limits
- Implement request queuing
- Add memory monitoring
- Optimize model loading

## Challenge Extensions

### Extension 1: Auto-scaling
Implement auto-scaling based on metrics:
```yaml
# kubernetes-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: langchain-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: langchain-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Extension 2: Circuit Breaker
Add circuit breaker pattern for resilience:
```python
from pybreaker import CircuitBreaker

llm_breaker = CircuitBreaker(fail_max=5, reset_timeout=60)

@llm_breaker
def call_llm(chain, input_data):
    return chain.invoke(input_data)
```

### Extension 3: Distributed Tracing
Add distributed tracing with OpenTelemetry:
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
```

## Completion Checklist
- [ ] Production API runs successfully locally
- [ ] All endpoints respond correctly
- [ ] Docker image builds and runs
- [ ] Docker Compose stack deploys successfully
- [ ] Health checks pass consistently
- [ ] Metrics are collected and reported
- [ ] Load testing completed
- [ ] Monitoring and logging verified
- [ ] Production optimizations implemented (optional)

## Learning Outcomes
After completing this exercise, you will understand:
- Production-ready API design and implementation
- Containerization and orchestration with Docker
- Health monitoring and metrics collection
- Load balancing and reverse proxy configuration
- Error handling and resilience patterns
- Performance monitoring and optimization
- Deployment strategies and best practices

## Next Steps
- Explore Kubernetes deployment options
- Implement advanced monitoring with Prometheus/Grafana
- Add authentication and authorization
- Implement API versioning and backward compatibility
- Set up CI/CD pipelines for automated deployment