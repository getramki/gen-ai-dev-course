"""
Module 6.3: Monitoring and Observability
Comprehensive monitoring, logging, and debugging for LangChain applications.
"""

import time
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import BaseCallbackHandler
import boto3

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    request_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    tokens_used: int = 0
    cost_estimate: float = 0.0
    success: bool = True
    error_message: Optional[str] = None

class MonitoringCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for monitoring LangChain operations."""
    
    def __init__(self):
        self.metrics: List[RequestMetrics] = []
        self.current_request: Optional[RequestMetrics] = None
    
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs):
        """Called when chain starts."""
        request_id = kwargs.get('run_id', str(time.time()))
        self.current_request = RequestMetrics(
            request_id=str(request_id),
            start_time=datetime.utcnow()
        )
        logger.info(f"Chain started: {request_id}")
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs):
        """Called when chain ends successfully."""
        if self.current_request:
            self.current_request.end_time = datetime.utcnow()
            self.current_request.success = True
            self.metrics.append(self.current_request)
            
            duration = (self.current_request.end_time - self.current_request.start_time).total_seconds()
            logger.info(f"Chain completed: {self.current_request.request_id} in {duration:.2f}s")
    
    def on_chain_error(self, error: Exception, **kwargs):
        """Called when chain encounters an error."""
        if self.current_request:
            self.current_request.end_time = datetime.utcnow()
            self.current_request.success = False
            self.current_request.error_message = str(error)
            self.metrics.append(self.current_request)
            
            logger.error(f"Chain failed: {self.current_request.request_id} - {error}")
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        """Called when LLM starts."""
        logger.debug(f"LLM call started with {len(prompts)} prompts")
    
    def on_llm_end(self, response, **kwargs):
        """Called when LLM ends."""
        if self.current_request and hasattr(response, 'llm_output'):
            # Estimate token usage (simplified)
            self.current_request.tokens_used += len(str(response).split())
            # Estimate cost (Claude-3 Sonnet: ~$3/1M input tokens, ~$15/1M output tokens)
            self.current_request.cost_estimate += (self.current_request.tokens_used / 1000000) * 9
        
        logger.debug("LLM call completed")

class PerformanceMonitor:
    """Monitor performance metrics and system health."""
    
    def __init__(self):
        self.metrics_history: List[RequestMetrics] = []
        self.cloudwatch = None
        try:
            self.cloudwatch = boto3.client('cloudwatch')
        except Exception:
            logger.warning("CloudWatch not available - using local metrics only")
    
    def add_metrics(self, metrics: RequestMetrics):
        """Add metrics to history."""
        self.metrics_history.append(metrics)
        
        # Send to CloudWatch if available
        if self.cloudwatch:
            self._send_to_cloudwatch(metrics)
    
    def _send_to_cloudwatch(self, metrics: RequestMetrics):
        """Send metrics to CloudWatch."""
        try:
            metric_data = [
                {
                    'MetricName': 'RequestDuration',
                    'Value': (metrics.end_time - metrics.start_time).total_seconds() if metrics.end_time else 0,
                    'Unit': 'Seconds'
                },
                {
                    'MetricName': 'TokensUsed',
                    'Value': metrics.tokens_used,
                    'Unit': 'Count'
                },
                {
                    'MetricName': 'CostEstimate',
                    'Value': metrics.cost_estimate,
                    'Unit': 'None'
                },
                {
                    'MetricName': 'RequestSuccess' if metrics.success else 'RequestError',
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
            
            self.cloudwatch.put_metric_data(
                Namespace='LangChain/Monitoring',
                MetricData=metric_data
            )
        except Exception as e:
            logger.error(f"Failed to send metrics to CloudWatch: {e}")
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for the last N hours."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_metrics = [m for m in self.metrics_history if m.start_time > cutoff_time]
        
        if not recent_metrics:
            return {"message": "No metrics available"}
        
        successful_requests = [m for m in recent_metrics if m.success]
        failed_requests = [m for m in recent_metrics if not m.success]
        
        durations = [(m.end_time - m.start_time).total_seconds() 
                    for m in successful_requests if m.end_time]
        
        return {
            "total_requests": len(recent_metrics),
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / len(recent_metrics) * 100,
            "avg_duration": sum(durations) / len(durations) if durations else 0,
            "total_tokens": sum(m.tokens_used for m in recent_metrics),
            "total_cost_estimate": sum(m.cost_estimate for m in recent_metrics),
            "error_types": list(set(m.error_message for m in failed_requests if m.error_message))
        }

class DebugHelper:
    """Helper for debugging LangChain applications."""
    
    @staticmethod
    def trace_chain_execution(chain, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace chain execution with detailed logging."""
        callback_handler = MonitoringCallbackHandler()
        
        try:
            # Execute with monitoring
            result = chain.invoke(input_data, config={"callbacks": [callback_handler]})
            
            # Get metrics
            metrics = callback_handler.metrics[-1] if callback_handler.metrics else None
            
            return {
                "success": True,
                "result": result,
                "metrics": {
                    "duration": (metrics.end_time - metrics.start_time).total_seconds() if metrics and metrics.end_time else 0,
                    "tokens_used": metrics.tokens_used if metrics else 0,
                    "cost_estimate": metrics.cost_estimate if metrics else 0
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metrics": None
            }
    
    @staticmethod
    def validate_chain_components(chain) -> List[str]:
        """Validate chain components and return issues."""
        issues = []
        
        try:
            # Check if chain has required components
            if not hasattr(chain, 'invoke'):
                issues.append("Chain missing invoke method")
            
            # Test with minimal input
            test_result = chain.invoke({"input": "test"})
            if not test_result:
                issues.append("Chain returns empty result")
                
        except Exception as e:
            issues.append(f"Chain execution error: {e}")
        
        return issues

class MonitoredLangChainService:
    """LangChain service with comprehensive monitoring."""
    
    def __init__(self):
        self.llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            model_kwargs={"temperature": 0.1, "max_tokens": 1000}
        )
        self.monitor = PerformanceMonitor()
        self.callback_handler = MonitoringCallbackHandler()
    
    def process_with_monitoring(self, input_text: str, task_type: str = "general") -> Dict[str, Any]:
        """Process request with full monitoring."""
        
        # Create appropriate prompt
        prompts = {
            "summarize": "Summarize this text:\n{input}",
            "analyze": "Analyze this content:\n{input}",
            "general": "Respond to this request:\n{input}"
        }
        
        prompt_template = prompts.get(task_type, prompts["general"])
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        
        # Execute with monitoring
        result = DebugHelper.trace_chain_execution(chain, {"input": input_text})
        
        # Add metrics to monitor
        if result["metrics"]:
            metrics = RequestMetrics(
                request_id=f"req_{int(time.time())}",
                start_time=datetime.utcnow() - timedelta(seconds=result["metrics"]["duration"]),
                end_time=datetime.utcnow(),
                tokens_used=result["metrics"]["tokens_used"],
                cost_estimate=result["metrics"]["cost_estimate"],
                success=result["success"]
            )
            self.monitor.add_metrics(metrics)
        
        return result
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get service health status."""
        summary = self.monitor.get_performance_summary(hours=1)
        
        # Determine health status
        if summary.get("total_requests", 0) == 0:
            status = "unknown"
        elif summary.get("success_rate", 0) > 95:
            status = "healthy"
        elif summary.get("success_rate", 0) > 80:
            status = "degraded"
        else:
            status = "unhealthy"
        
        return {
            "status": status,
            "summary": summary,
            "timestamp": datetime.utcnow().isoformat()
        }

def demonstrate_monitoring():
    """Demonstrate monitoring and observability features."""
    
    print("=== Monitoring and Observability Demo ===\n")
    
    # 1. Initialize monitored service
    service = MonitoredLangChainService()
    
    # 2. Process some requests
    test_requests = [
        ("Explain quantum computing", "summarize"),
        ("What are the benefits of cloud computing?", "analyze"),
        ("Generate a haiku about technology", "general")
    ]
    
    print("1. Processing requests with monitoring:")
    for input_text, task_type in test_requests:
        result = service.process_with_monitoring(input_text, task_type)
        print(f"Task: {task_type}")
        print(f"Success: {result['success']}")
        if result['success'] and result['metrics']:
            print(f"Duration: {result['metrics']['duration']:.2f}s")
            print(f"Tokens: {result['metrics']['tokens_used']}")
            print(f"Cost: ${result['metrics']['cost_estimate']:.6f}")
        print()
    
    # 3. Get health status
    print("2. Service Health Status:")
    health = service.get_health_status()
    print(f"Status: {health['status']}")
    print(f"Summary: {json.dumps(health['summary'], indent=2)}")
    print()
    
    # 4. Debug chain validation
    print("3. Chain Validation:")
    prompt = ChatPromptTemplate.from_template("Test prompt: {input}")
    chain = prompt | service.llm | StrOutputParser()
    
    issues = DebugHelper.validate_chain_components(chain)
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("Chain validation passed")

if __name__ == "__main__":
    demonstrate_monitoring()