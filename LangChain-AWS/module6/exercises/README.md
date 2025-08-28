# Module 6 Exercises: Advanced Patterns and Production

## Overview
This module contains two comprehensive exercises that demonstrate advanced LangChain patterns and production deployment strategies for enterprise-grade applications.

## Exercise Structure

### Exercise 1: Multi-Agent System
**File**: `exercise_1_multi_agent.py`  
**Instructions**: `exercise_1_instructions.md`  
**Duration**: 15 minutes

Build a coordinated system of AI agents that work together to solve complex tasks through role specialization and workflow orchestration.

**Key Features**:
- 5 specialized agent roles (Coordinator, Researcher, Analyst, Writer, Reviewer)
- Task dependency management and execution ordering
- Structured agent communication with JSON responses
- Workflow orchestration and monitoring
- Performance tracking and system status reporting

**Learning Outcomes**:
- Multi-agent system architecture
- Task coordination and dependency management
- Agent specialization patterns
- Workflow optimization strategies

### Exercise 2: Production Deployment
**File**: `exercise_2_production_deployment.py`  
**Instructions**: `exercise_2_instructions.md`  
**Duration**: 15 minutes

Deploy a scalable, production-ready LangChain service with comprehensive monitoring, health checks, and enterprise-grade features.

**Key Features**:
- Flask REST API with multiple endpoints
- Docker containerization with multi-stage builds
- Docker Compose orchestration with Nginx load balancer
- CloudWatch metrics integration
- Health checks and monitoring dashboards
- Batch processing and async capabilities

**Learning Outcomes**:
- Production API design and implementation
- Containerization and orchestration
- Monitoring and observability
- Load balancing and scaling strategies

## Prerequisites

### System Requirements
- Python 3.11+
- AWS account with Bedrock access
- Docker (for deployment exercises)
- 8GB+ RAM recommended

### Python Dependencies
```bash
pip install langchain-aws langchain-core flask boto3 pydantic
```

### Optional Dependencies
```bash
# For load testing
pip install locust

# For enhanced monitoring
pip install prometheus-client

# For async processing
pip install aiohttp asyncio
```

## Quick Start

### Running All Exercises
```bash
cd module6

# Exercise 1: Multi-Agent System
python exercise_1_multi_agent.py

# Exercise 2: Production Deployment (demo)
python exercise_2_production_deployment.py

# Exercise 2: Production Deployment (run server)
python exercise_2_production_deployment.py run
```

### Docker Deployment
```bash
# Build and run Exercise 2 with Docker
docker build -t langchain-api .
docker run -p 8000:8000 langchain-api

# Or use Docker Compose
docker-compose up -d
```

## Integration Patterns

### Combining Exercises
The exercises can be integrated to create a comprehensive production system:

```python
# Integration example: Multi-agent system as a service
from exercise_1_multi_agent import MultiAgentSystem
from exercise_2_production_deployment import ProductionLangChainAPI

class EnterpriseMultiAgentAPI(ProductionLangChainAPI):
    def __init__(self, config):
        super().__init__(config)
        self.multi_agent_system = MultiAgentSystem()
    
    def _process_complex_workflow(self, workflow_description):
        return self.multi_agent_system.execute_workflow(workflow_description)
```

### Scaling Patterns
1. **Horizontal Scaling**: Deploy multiple API instances behind a load balancer
2. **Agent Specialization**: Create domain-specific agent pools
3. **Async Processing**: Use message queues for long-running workflows
4. **Caching**: Implement Redis for agent response caching

## Performance Benchmarks

### Expected Performance Metrics
- **Single Request**: 1-3 seconds response time
- **Batch Processing**: 5-10 requests per batch, 2-5 seconds per batch
- **Multi-Agent Workflow**: 10-30 seconds for complete workflow
- **Throughput**: 10-50 requests per minute (depending on complexity)

### Optimization Strategies
1. **Model Selection**: Use appropriate models for task complexity
2. **Caching**: Cache frequent responses and agent outputs
3. **Parallel Processing**: Execute independent tasks concurrently
4. **Resource Management**: Monitor and optimize memory usage

## Troubleshooting Guide

### Common Issues

#### Exercise 1: Multi-Agent System
**Issue**: Agent tasks fail with JSON parsing errors
**Solution**: 
- Check prompt formatting and JSON structure
- Verify Pydantic model definitions
- Add error handling for malformed responses

**Issue**: Workflow execution hangs
**Solution**:
- Check task dependencies for circular references
- Verify agent assignment and availability
- Add timeout mechanisms

#### Exercise 2: Production Deployment
**Issue**: Docker build fails
**Solution**:
- Verify requirements.txt completeness
- Check Python version compatibility
- Ensure AWS credentials are properly configured

**Issue**: Health checks fail
**Solution**:
- Verify AWS Bedrock permissions
- Check model availability and region settings
- Test LLM connectivity independently

### Debug Commands
```bash
# Check Docker logs
docker-compose logs -f langchain-api

# Test API endpoints
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"input": "test", "task_type": "qa"}'

# Monitor system resources
docker stats

# Check AWS credentials
aws bedrock list-foundation-models --region us-east-1
```

## Advanced Configurations

### Environment Variables
```bash
# Model Configuration
export MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
export TEMPERATURE=0.1
export MAX_TOKENS=1000

# AWS Configuration
export AWS_REGION=us-east-1
export AWS_PROFILE=default

# Application Configuration
export LOG_LEVEL=INFO
export ENABLE_METRICS=true
export BATCH_SIZE=5
```

### Production Settings
```python
# config/production.py
PRODUCTION_CONFIG = {
    'model_id': 'anthropic.claude-3-sonnet-20240229-v1:0',
    'temperature': 0.05,  # Lower for consistency
    'max_tokens': 2000,   # Higher for complex tasks
    'timeout': 30,        # Request timeout
    'retry_attempts': 3,  # Retry failed requests
    'cache_ttl': 3600,    # Cache responses for 1 hour
    'max_batch_size': 10, # Limit batch processing
    'enable_monitoring': True,
    'log_level': 'INFO'
}
```

## Success Criteria

### Exercise 1 Success Indicators
- [ ] All 5 agent types function correctly
- [ ] Workflow executes with proper task ordering
- [ ] Dependencies are resolved correctly
- [ ] System status reports accurate metrics
- [ ] Final output is coherent and comprehensive

### Exercise 2 Success Indicators
- [ ] API server starts without errors
- [ ] All endpoints respond correctly
- [ ] Health checks pass consistently
- [ ] Metrics are collected and reported
- [ ] Docker deployment works successfully
- [ ] Load testing shows acceptable performance

### Integration Success Indicators
- [ ] Multi-agent workflows can be triggered via API
- [ ] Production monitoring captures agent metrics
- [ ] System scales under load
- [ ] Error handling works across all components
- [ ] Documentation is complete and accurate

## Next Steps

### Advanced Topics to Explore
1. **Kubernetes Deployment**: Scale to production with K8s
2. **Service Mesh**: Implement Istio for advanced traffic management
3. **Observability**: Add Prometheus, Grafana, and Jaeger tracing
4. **Security**: Implement authentication, authorization, and encryption
5. **CI/CD**: Automate testing and deployment pipelines

### Real-World Applications
1. **Enterprise Document Processing**: Multi-agent document analysis
2. **Customer Service Automation**: Intelligent routing and response
3. **Content Generation Pipeline**: Automated content creation workflow
4. **Research and Analysis Platform**: Coordinated research agents
5. **Code Review System**: Multi-agent code analysis and improvement

## Resources

### Documentation Links
- [LangChain Production Guide](https://python.langchain.com/docs/guides/productionization)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)

### Community Resources
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [AWS Bedrock Examples](https://github.com/aws-samples/amazon-bedrock-samples)
- [Production ML Systems](https://github.com/eugeneyan/applied-ml)

This completes the Module 6 exercises, providing comprehensive coverage of advanced LangChain patterns and production deployment strategies.