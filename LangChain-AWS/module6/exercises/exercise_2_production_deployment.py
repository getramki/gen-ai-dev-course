"""
Exercise 2: Production Deployment
Deploy a scalable LangChain service with monitoring, health checks, and production-ready features.
"""

import os
import json
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
from flask import Flask, request, jsonify
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProductionLangChainAPI:
    """Production-ready LangChain API service."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.app = Flask(__name__)
        self.llm = self._initialize_llm()
        self.metrics = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_error': 0,
            'avg_response_time': 0,
            'uptime_start': datetime.utcnow()
        }
        self._setup_routes()
        self._setup_monitoring()
    
    def _initialize_llm(self) -> ChatBedrock:
        """Initialize LLM with production configuration."""
        try:
            return ChatBedrock(
                model_id=self.config.get('model_id', 'anthropic.claude-3-sonnet-20240229-v1:0'),
                model_kwargs={
                    'temperature': self.config.get('temperature', 0.1),
                    'max_tokens': self.config.get('max_tokens', 1000)
                },
                region_name=self.config.get('region', 'us-east-1')
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
    
    def _setup_monitoring(self):
        """Setup CloudWatch monitoring if available."""
        try:
            self.cloudwatch = boto3.client('cloudwatch', region_name=self.config.get('region', 'us-east-1'))
            logger.info("CloudWatch monitoring enabled")
        except Exception as e:
            logger.warning(f"CloudWatch not available: {e}")
            self.cloudwatch = None
    
    def _log_metric(self, metric_name: str, value: float, unit: str = 'Count'):
        """Log metric to CloudWatch."""
        if self.cloudwatch:
            try:
                self.cloudwatch.put_metric_data(
                    Namespace='LangChain/Production',
                    MetricData=[{
                        'MetricName': metric_name,
                        'Value': value,
                        'Unit': unit,
                        'Timestamp': datetime.utcnow()
                    }]
                )
            except Exception as e:
                logger.error(f"Failed to log metric {metric_name}: {e}")
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            try:
                # Test LLM connectivity
                test_prompt = ChatPromptTemplate.from_template("Say 'OK'")
                test_chain = test_prompt | self.llm | StrOutputParser()
                test_result = test_chain.invoke({})
                
                uptime = (datetime.utcnow() - self.metrics['uptime_start']).total_seconds()
                
                return jsonify({
                    'status': 'healthy',
                    'timestamp': datetime.utcnow().isoformat(),
                    'uptime_seconds': uptime,
                    'llm_status': 'connected' if 'OK' in test_result else 'degraded',
                    'version': self.config.get('version', '1.0.0')
                }), 200
                
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                return jsonify({
                    'status': 'unhealthy',
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                }), 503
        
        @self.app.route('/metrics', methods=['GET'])
        def get_metrics():
            """Metrics endpoint."""
            uptime = (datetime.utcnow() - self.metrics['uptime_start']).total_seconds()
            success_rate = (self.metrics['requests_success'] / max(self.metrics['requests_total'], 1)) * 100
            
            return jsonify({
                'requests_total': self.metrics['requests_total'],
                'requests_success': self.metrics['requests_success'],
                'requests_error': self.metrics['requests_error'],
                'success_rate_percent': round(success_rate, 2),
                'avg_response_time_seconds': self.metrics['avg_response_time'],
                'uptime_seconds': uptime
            })
        
        @self.app.route('/process', methods=['POST'])
        def process_request():
            """Main processing endpoint."""
            start_time = time.time()
            request_id = f"req_{int(time.time() * 1000)}"
            
            try:
                # Update metrics
                self.metrics['requests_total'] += 1
                
                # Validate request
                data = request.get_json()
                if not data or 'input' not in data:
                    return jsonify({
                        'success': False,
                        'error': 'Missing required field: input',
                        'request_id': request_id
                    }), 400
                
                # Process request
                result = self._process_llm_request(data)
                
                # Calculate response time
                response_time = time.time() - start_time
                self.metrics['avg_response_time'] = (
                    (self.metrics['avg_response_time'] * (self.metrics['requests_total'] - 1) + response_time) 
                    / self.metrics['requests_total']
                )
                
                if result['success']:
                    self.metrics['requests_success'] += 1
                    self._log_metric('RequestSuccess', 1)
                else:
                    self.metrics['requests_error'] += 1
                    self._log_metric('RequestError', 1)
                
                self._log_metric('ResponseTime', response_time, 'Seconds')
                
                logger.info(f"Request {request_id} processed in {response_time:.3f}s")
                
                return jsonify({
                    **result,
                    'request_id': request_id,
                    'response_time': response_time
                })
                
            except Exception as e:
                self.metrics['requests_error'] += 1
                self._log_metric('RequestError', 1)
                
                logger.error(f"Request {request_id} failed: {e}")
                
                return jsonify({
                    'success': False,
                    'error': 'Internal server error',
                    'request_id': request_id
                }), 500
        
        @self.app.route('/batch', methods=['POST'])
        def batch_process():
            """Batch processing endpoint."""
            start_time = time.time()
            
            try:
                data = request.get_json()
                if not data or 'requests' not in data:
                    return jsonify({
                        'success': False,
                        'error': 'Missing required field: requests'
                    }), 400
                
                requests_data = data['requests']
                if not isinstance(requests_data, list):
                    return jsonify({
                        'success': False,
                        'error': 'requests must be a list'
                    }), 400
                
                # Process batch
                results = []
                for i, req_data in enumerate(requests_data):
                    if 'input' not in req_data:
                        results.append({
                            'success': False,
                            'error': f'Missing input in request {i}',
                            'index': i
                        })
                        continue
                    
                    result = self._process_llm_request(req_data)
                    result['index'] = i
                    results.append(result)
                
                batch_time = time.time() - start_time
                successful = sum(1 for r in results if r.get('success', False))
                
                return jsonify({
                    'success': True,
                    'results': results,
                    'batch_size': len(requests_data),
                    'successful_count': successful,
                    'batch_processing_time': batch_time
                })
                
            except Exception as e:
                logger.error(f"Batch processing failed: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Batch processing error'
                }), 500
    
    def _process_llm_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process individual LLM request."""
        try:
            input_text = data['input']
            task_type = data.get('task_type', 'general')
            
            # Create appropriate prompt
            prompts = {
                'summarize': "Summarize this text concisely:\n{input}",
                'analyze': "Analyze this content:\n{input}",
                'generate': "Generate content based on:\n{input}",
                'qa': "Answer this question:\n{input}",
                'general': "Respond to this request:\n{input}"
            }
            
            prompt_template = prompts.get(task_type, prompts['general'])
            prompt = ChatPromptTemplate.from_template(prompt_template)
            
            # Execute chain
            chain = prompt | self.llm | StrOutputParser()
            result = chain.invoke({'input': input_text})
            
            return {
                'success': True,
                'result': result,
                'task_type': task_type
            }
            
        except Exception as e:
            logger.error(f"LLM processing error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run(self, host='0.0.0.0', port=8000, debug=False):
        """Run the Flask application."""
        logger.info(f"Starting LangChain Production API on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

# Docker configuration files
DOCKERFILE = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "exercise_2_production_deployment.py"]
"""

REQUIREMENTS_TXT = """
flask==2.3.3
langchain-aws==0.1.7
langchain-core==0.2.11
boto3==1.34.131
gunicorn==21.2.0
"""

DOCKER_COMPOSE = """
version: '3.8'

services:
  langchain-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
      - TEMPERATURE=0.1
      - MAX_TOKENS=1000
      - AWS_REGION=us-east-1
    volumes:
      - ~/.aws:/home/appuser/.aws:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - langchain-api
    restart: unless-stopped
"""

NGINX_CONF = """
events {
    worker_connections 1024;
}

http {
    upstream langchain_api {
        server langchain-api:8000;
    }

    server {
        listen 80;
        
        location / {
            proxy_pass http://langchain_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
        
        location /health {
            proxy_pass http://langchain_api/health;
            access_log off;
        }
    }
}
"""

def create_deployment_files():
    """Create deployment configuration files."""
    
    files = {
        'Dockerfile': DOCKERFILE,
        'requirements.txt': REQUIREMENTS_TXT,
        'docker-compose.yml': DOCKER_COMPOSE,
        'nginx.conf': NGINX_CONF
    }
    
    for filename, content in files.items():
        with open(filename, 'w') as f:
            f.write(content.strip())
        print(f"Created {filename}")

def demonstrate_production_deployment():
    """Demonstrate production deployment setup."""
    
    print("=== Production Deployment Demo ===\n")
    
    # Configuration
    config = {
        'model_id': os.environ.get('MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0'),
        'temperature': float(os.environ.get('TEMPERATURE', '0.1')),
        'max_tokens': int(os.environ.get('MAX_TOKENS', '1000')),
        'region': os.environ.get('AWS_REGION', 'us-east-1'),
        'version': '1.0.0'
    }
    
    print("1. Configuration:")
    print(json.dumps(config, indent=2))
    print()
    
    # Create deployment files
    print("2. Creating deployment files...")
    create_deployment_files()
    print()
    
    # Initialize API
    print("3. Initializing Production API...")
    try:
        api = ProductionLangChainAPI(config)
        print("✓ API initialized successfully")
        
        # Test internal processing
        test_request = {
            'input': 'What is machine learning?',
            'task_type': 'qa'
        }
        
        result = api._process_llm_request(test_request)
        print(f"✓ LLM processing test: {'Success' if result['success'] else 'Failed'}")
        
        if result['success']:
            print(f"  Result preview: {result['result'][:100]}...")
        
    except Exception as e:
        print(f"✗ API initialization failed: {e}")
        return
    
    print()
    
    # Show deployment instructions
    print("4. Deployment Instructions:")
    print("   Local Development:")
    print("   python exercise_2_production_deployment.py")
    print()
    print("   Docker Deployment:")
    print("   docker build -t langchain-api .")
    print("   docker run -p 8000:8000 langchain-api")
    print()
    print("   Docker Compose (with Nginx):")
    print("   docker-compose up -d")
    print()
    print("   Kubernetes Deployment:")
    print("   kubectl apply -f k8s-deployment.yaml")
    print()
    
    # Show API endpoints
    print("5. Available Endpoints:")
    endpoints = [
        ("GET /health", "Health check and service status"),
        ("GET /metrics", "Performance metrics and statistics"),
        ("POST /process", "Single request processing"),
        ("POST /batch", "Batch request processing")
    ]
    
    for endpoint, description in endpoints:
        print(f"   {endpoint:<15} - {description}")
    
    print()
    print("6. Monitoring Features:")
    features = [
        "CloudWatch metrics integration",
        "Structured logging with request IDs",
        "Health checks with LLM connectivity test",
        "Performance metrics tracking",
        "Error rate monitoring",
        "Response time tracking"
    ]
    
    for feature in features:
        print(f"   ✓ {feature}")

if __name__ == "__main__":
    if len(os.sys.argv) > 1 and os.sys.argv[1] == 'run':
        # Run the API server
        config = {
            'model_id': os.environ.get('MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0'),
            'temperature': float(os.environ.get('TEMPERATURE', '0.1')),
            'max_tokens': int(os.environ.get('MAX_TOKENS', '1000')),
            'region': os.environ.get('AWS_REGION', 'us-east-1'),
            'version': '1.0.0'
        }
        
        api = ProductionLangChainAPI(config)
        api.run(debug=False)
    else:
        # Run demonstration
        demonstrate_production_deployment()