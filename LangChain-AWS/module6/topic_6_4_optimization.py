"""
Module 6.4: Performance Optimization
Cost and speed optimization techniques for LangChain applications.
"""

import time
import asyncio
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache
import hashlib
import json

# Set up caching
set_llm_cache(InMemoryCache())

class OptimizedLangChainService:
    """Optimized LangChain service with performance enhancements."""
    
    def __init__(self):
        # Different model configurations for different use cases
        self.models = {
            'fast': ChatBedrock(
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                model_kwargs={"temperature": 0.1, "max_tokens": 500}
            ),
            'balanced': ChatBedrock(
                model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                model_kwargs={"temperature": 0.1, "max_tokens": 1000}
            ),
            'powerful': ChatBedrock(
                model_id="anthropic.claude-3-opus-20240229-v1:0",
                model_kwargs={"temperature": 0.1, "max_tokens": 2000}
            )
        }
        
        # Response cache
        self.response_cache = {}
        
        # Batch processing queue
        self.batch_queue = []
        self.batch_size = 5
    
    def _get_cache_key(self, input_text: str, task_type: str, model_type: str) -> str:
        """Generate cache key for request."""
        content = f"{input_text}:{task_type}:{model_type}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _select_optimal_model(self, task_type: str, complexity: str = "medium") -> str:
        """Select optimal model based on task requirements."""
        
        # Simple task routing
        if task_type in ["summarize", "classify", "extract"]:
            return "fast"  # Haiku for simple tasks
        elif task_type in ["analyze", "generate", "qa"]:
            if complexity == "high":
                return "powerful"  # Opus for complex tasks
            else:
                return "balanced"  # Sonnet for balanced tasks
        else:
            return "balanced"
    
    def process_optimized(self, input_text: str, task_type: str = "general", 
                         complexity: str = "medium", use_cache: bool = True) -> Dict[str, Any]:
        """Process request with optimization strategies."""
        
        start_time = time.time()
        
        # 1. Model Selection
        model_type = self._select_optimal_model(task_type, complexity)
        llm = self.models[model_type]
        
        # 2. Cache Check
        cache_key = self._get_cache_key(input_text, task_type, model_type)
        if use_cache and cache_key in self.response_cache:
            cached_result = self.response_cache[cache_key]
            return {
                "result": cached_result["result"],
                "model_used": model_type,
                "cached": True,
                "processing_time": time.time() - start_time,
                "cost_estimate": 0.0  # No cost for cached responses
            }
        
        # 3. Optimized Prompt
        optimized_prompt = self._create_optimized_prompt(task_type)
        chain = optimized_prompt | llm | StrOutputParser()
        
        # 4. Execute
        try:
            result = chain.invoke({"input": input_text})
            
            # 5. Cache Result
            if use_cache:
                self.response_cache[cache_key] = {
                    "result": result,
                    "timestamp": time.time()
                }
            
            # 6. Calculate metrics
            processing_time = time.time() - start_time
            cost_estimate = self._estimate_cost(input_text, result, model_type)
            
            return {
                "result": result,
                "model_used": model_type,
                "cached": False,
                "processing_time": processing_time,
                "cost_estimate": cost_estimate
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "model_used": model_type,
                "processing_time": time.time() - start_time
            }
    
    def _create_optimized_prompt(self, task_type: str) -> ChatPromptTemplate:
        """Create optimized prompts for different tasks."""
        
        # Optimized prompts that are concise but effective
        prompts = {
            "summarize": ChatPromptTemplate.from_template(
                "Summarize in 2-3 sentences:\n{input}"
            ),
            "analyze": ChatPromptTemplate.from_template(
                "Analyze key points:\n{input}\nProvide: main themes, sentiment, implications."
            ),
            "classify": ChatPromptTemplate.from_template(
                "Classify this content. Category and confidence:\n{input}"
            ),
            "extract": ChatPromptTemplate.from_template(
                "Extract key information as JSON:\n{input}"
            ),
            "qa": ChatPromptTemplate.from_template(
                "Answer concisely:\n{input}"
            ),
            "generate": ChatPromptTemplate.from_template(
                "Generate based on:\n{input}\nBe creative but concise."
            )
        }
        
        return prompts.get(task_type, prompts["qa"])
    
    def _estimate_cost(self, input_text: str, output_text: str, model_type: str) -> float:
        """Estimate cost based on token usage and model type."""
        
        # Rough token estimation (1 token ≈ 4 characters)
        input_tokens = len(input_text) / 4
        output_tokens = len(output_text) / 4
        
        # Cost per 1M tokens (approximate)
        costs = {
            'fast': {'input': 0.25, 'output': 1.25},      # Haiku
            'balanced': {'input': 3.0, 'output': 15.0},   # Sonnet
            'powerful': {'input': 15.0, 'output': 75.0}   # Opus
        }
        
        model_costs = costs.get(model_type, costs['balanced'])
        
        cost = (input_tokens / 1000000 * model_costs['input'] + 
                output_tokens / 1000000 * model_costs['output'])
        
        return cost
    
    def process_batch(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple requests efficiently."""
        
        start_time = time.time()
        results = []
        
        # Group by model type for batch processing
        model_groups = {}
        for i, request in enumerate(requests):
            model_type = self._select_optimal_model(
                request.get('task_type', 'general'),
                request.get('complexity', 'medium')
            )
            if model_type not in model_groups:
                model_groups[model_type] = []
            model_groups[model_type].append((i, request))
        
        # Process each group
        for model_type, group_requests in model_groups.items():
            llm = self.models[model_type]
            
            # Create parallel chains
            chains = []
            for _, request in group_requests:
                prompt = self._create_optimized_prompt(request.get('task_type', 'general'))
                chain = prompt | llm | StrOutputParser()
                chains.append(chain)
            
            # Execute in parallel
            parallel_chain = RunnableParallel({
                f"result_{i}": chain for i, (_, chain) in enumerate(zip(group_requests, chains))
            })
            
            try:
                parallel_results = parallel_chain.invoke({
                    f"result_{i}": {"input": req['input']} 
                    for i, (_, req) in enumerate(group_requests)
                })
                
                # Map results back
                for i, (original_index, request) in enumerate(group_requests):
                    result_key = f"result_{i}"
                    results.append({
                        "index": original_index,
                        "result": parallel_results[result_key],
                        "model_used": model_type,
                        "request": request
                    })
                    
            except Exception as e:
                # Handle errors for this group
                for original_index, request in group_requests:
                    results.append({
                        "index": original_index,
                        "error": str(e),
                        "model_used": model_type,
                        "request": request
                    })
        
        # Sort results by original index
        results.sort(key=lambda x: x["index"])
        
        total_time = time.time() - start_time
        
        return {
            "results": [r for r in results],
            "batch_processing_time": total_time,
            "requests_processed": len(requests)
        }
    
    async def process_async(self, input_text: str, task_type: str = "general") -> Dict[str, Any]:
        """Asynchronous processing for better concurrency."""
        
        def sync_process():
            return self.process_optimized(input_text, task_type)
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, sync_process)
        
        return result
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization statistics."""
        
        cache_size = len(self.response_cache)
        cache_hit_rate = 0  # Would need to track hits/misses in real implementation
        
        return {
            "cache_size": cache_size,
            "cache_hit_rate": cache_hit_rate,
            "models_available": list(self.models.keys()),
            "optimization_features": [
                "Model selection based on task complexity",
                "Response caching",
                "Batch processing",
                "Parallel execution",
                "Async processing",
                "Cost estimation"
            ]
        }

def demonstrate_optimization():
    """Demonstrate performance optimization techniques."""
    
    print("=== Performance Optimization Demo ===\n")
    
    service = OptimizedLangChainService()
    
    # 1. Single Request Optimization
    print("1. Single Request Optimization:")
    test_cases = [
        ("What is AI?", "qa", "low"),
        ("Analyze the impact of AI on society", "analyze", "high"),
        ("Summarize: AI is transforming industries", "summarize", "low")
    ]
    
    for input_text, task_type, complexity in test_cases:
        result = service.process_optimized(input_text, task_type, complexity)
        print(f"Task: {task_type} ({complexity} complexity)")
        print(f"Model: {result.get('model_used', 'unknown')}")
        print(f"Time: {result.get('processing_time', 0):.3f}s")
        print(f"Cost: ${result.get('cost_estimate', 0):.6f}")
        print(f"Cached: {result.get('cached', False)}")
        print()
    
    # 2. Batch Processing
    print("2. Batch Processing:")
    batch_requests = [
        {"input": "What is machine learning?", "task_type": "qa"},
        {"input": "Explain neural networks", "task_type": "qa"},
        {"input": "Benefits of cloud computing", "task_type": "summarize"},
        {"input": "Future of AI technology", "task_type": "analyze", "complexity": "high"}
    ]
    
    batch_result = service.process_batch(batch_requests)
    print(f"Processed {batch_result['requests_processed']} requests")
    print(f"Total time: {batch_result['batch_processing_time']:.3f}s")
    print(f"Average time per request: {batch_result['batch_processing_time']/len(batch_requests):.3f}s")
    print()
    
    # 3. Async Processing Demo
    print("3. Async Processing:")
    async def async_demo():
        tasks = [
            service.process_async("What is quantum computing?", "qa"),
            service.process_async("Explain blockchain", "qa"),
            service.process_async("Future of renewable energy", "analyze")
        ]
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        print(f"Processed {len(results)} requests concurrently")
        print(f"Total concurrent time: {total_time:.3f}s")
        
        return results
    
    # Run async demo
    try:
        asyncio.run(async_demo())
    except Exception as e:
        print(f"Async demo error: {e}")
    
    print()
    
    # 4. Optimization Statistics
    print("4. Optimization Statistics:")
    stats = service.get_optimization_stats()
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    demonstrate_optimization()