"""
Module 6.2: Production Architecture
Scalable deployment patterns and infrastructure for LangChain applications.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionLangChainService:
    """Production-ready LangChain service with proper architecture."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm = self._initialize_llm()
        self.cloudwatch = boto3.client('cloudwatch')
        self._setup_monitoring()
    
    def _initialize_llm(self) -> ChatBedrock:
        """Initialize LLM with production settings."""
        return ChatBedrock(
            model_id=self.config.get('model_id', 'anthropic.claude-3-sonnet-20240229-v1:0'),
            model_kwargs={
                'temperature': self.config.get('temperature', 0.1),
                'max_tokens': self.config.get('max_tokens', 1000)
            },
            region_name=self.config.get('region', 'us-east-1')
        )
    
    def _setup_monitoring(self):
        """Setup CloudWatch monitoring."""
        self.metrics = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_error': 0,
            'avg_response_time': 0
        }
    
    def _log_metric(self, metric_name: str, value: float, unit: str = 'Count'):
        """Log metric to CloudWatch."""
        try:
            self.cloudwatch.put_metric_data(
                Namespace='LangChain/Production',
                MetricData=[
                    {
                        'MetricName': metric_name,
                        'Value': value,
                        'Unit': unit,
                        'Timestamp': datetime.utcnow()
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Failed to log metric {metric_name}: {e}")
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process request with full production monitoring."""
        start_time = datetime.utcnow()
        request_id = request.get('request_id', 'unknown')
        
        try:
            # Log request start
            logger.info(f"Processing request {request_id}")
            self.metrics['requests_total'] += 1
            
            # Validate input
            if not self._validate_request(request):
                raise ValueError("Invalid request format")
            
            # Process with chain
            result = self._execute_chain(request)
            
            # Log success
            self.metrics['requests_success'] += 1
            self._log_metric('RequestsSuccess', 1)
            
            # Calculate response time
            response_time = (datetime.utcnow() - start_time).total_seconds()
            self._log_metric('ResponseTime', response_time, 'Seconds')
            
            logger.info(f"Request {request_id} completed in {response_time:.2f}s")
            
            return {
                'success': True,
                'result': result,
                'request_id': request_id,
                'response_time': response_time
            }
            
        except Exception as e:
            # Log error
            self.metrics['requests_error'] += 1
            self._log_metric('RequestsError', 1)
            
            logger.error(f"Request {request_id} failed: {e}")
            
            return {
                'success': False,
                'error': str(e),
                'request_id': request_id
            }
    
    def _validate_request(self, request: Dict[str, Any]) -> bool:
        """Validate incoming request."""
        required_fields = ['input', 'task_type']
        return all(field in request for field in required_fields)
    
    def _execute_chain(self, request: Dict[str, Any]) -> str:
        """Execute the appropriate chain based on request."""
        task_type = request['task_type']
        input_text = request['input']
        
        # Select prompt based on task type
        prompts = {
            'summarize': "Summarize this text concisely:\n{input}",
            'analyze': "Analyze this content:\n{input}",
            'generate': "Generate content based on:\n{input}",
            'qa': "Answer this question:\n{input}"
        }
        
        prompt_template = prompts.get(task_type, prompts['qa'])
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # Execute chain
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({'input': input_text})

# AWS Lambda Handler
def lambda_handler(event, context):
    """AWS Lambda handler for serverless deployment."""
    
    # Initialize service
    config = {
        'model_id': os.environ.get('MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0'),
        'temperature': float(os.environ.get('TEMPERATURE', '0.1')),
        'max_tokens': int(os.environ.get('MAX_TOKENS', '1000')),
        'region': os.environ.get('AWS_REGION', 'us-east-1')
    }
    
    service = ProductionLangChainService(config)
    
    try:
        # Parse request
        if 'body' in event:
            request_data = json.loads(event['body'])
        else:
            request_data = event
        
        # Add request ID
        request_data['request_id'] = context.aws_request_id if context else 'local'
        
        # Process request
        result = service.process_request(request_data)
        
        # Return response
        return {
            'statusCode': 200 if result['success'] else 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"Lambda handler error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': False,
                'error': 'Internal server error'
            })
        }

# Docker Configuration
DOCKERFILE_CONTENT = """
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# FastAPI Application
FASTAPI_APP = """
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

app = FastAPI(title="LangChain Production Service")

# Initialize service
config = {
    'model_id': 'anthropic.claude-3-sonnet-20240229-v1:0',
    'temperature': 0.1,
    'max_tokens': 1000
}
service = ProductionLangChainService(config)

class RequestModel(BaseModel):
    input: str
    task_type: str
    request_id: str = None

@app.post("/process")
async def process_request(request: RequestModel):
    try:
        result = service.process_request(request.dict())
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=400, detail=result['error'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "langchain-production"}

@app.get("/metrics")
async def get_metrics():
    return service.metrics

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

# Kubernetes Deployment
K8S_DEPLOYMENT = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langchain-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: langchain-service
  template:
    metadata:
      labels:
        app: langchain-service
    spec:
      containers:
      - name: langchain-service
        image: langchain-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_ID
          value: "anthropic.claude-3-sonnet-20240229-v1:0"
        - name: TEMPERATURE
          value: "0.1"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: langchain-service
spec:
  selector:
    app: langchain-service
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
"""

def demonstrate_production_patterns():
    """Demonstrate production architecture patterns."""
    
    print("=== Production Architecture Demo ===\n")
    
    # 1. Production Service
    print("1. Production Service Configuration:")
    config = {
        'model_id': 'anthropic.claude-3-sonnet-20240229-v1:0',
        'temperature': 0.1,
        'max_tokens': 500,
        'region': 'us-east-1'
    }
    
    service = ProductionLangChainService(config)
    
    # Test request
    test_request = {
        'input': 'Explain machine learning in simple terms',
        'task_type': 'summarize',
        'request_id': 'test-001'
    }
    
    try:
        result = service.process_request(test_request)
        print(f"Service result: {result['success']}")
        if result['success']:
            print(f"Response time: {result['response_time']:.2f}s")
            print(f"Result preview: {result['result'][:100]}...")
        print()
    except Exception as e:
        print(f"Service error: {e}\n")
    
    # 2. Metrics
    print("2. Service Metrics:")
    for metric, value in service.metrics.items():
        print(f"{metric}: {value}")
    print()
    
    # 3. Configuration Files
    print("3. Deployment Configurations Generated:")
    print("- Dockerfile for containerization")
    print("- FastAPI application for REST API")
    print("- Kubernetes deployment for orchestration")
    print("- Lambda handler for serverless")

if __name__ == "__main__":
    demonstrate_production_patterns()