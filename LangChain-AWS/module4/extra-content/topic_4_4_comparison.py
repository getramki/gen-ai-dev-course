"""
Topic 4.4: Comparing ChatBedrock vs ChatBedrockConverse (7 minutes)

Learning Goals:
- Compare performance characteristics of both chat models
- Understand feature differences and use case optimization
- Make informed decisions for production deployments
- Establish migration strategies between models
"""

from langchain_aws.chat_models import ChatBedrock, ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import time
import asyncio
from typing import Dict, List

def setup_comparison_models():
    """Initialize both ChatBedrock and ChatBedrockConverse for comparison"""
    
    print("=== Model Comparison Setup ===\n")
    
    models = {}
    
    # Setup ChatBedrock
    try:
        models['chatbedrock'] = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "max_tokens": 200,
                "temperature": 0.7
            }
        )
        print("✅ ChatBedrock initialized")
    except Exception as e:
        print(f"❌ ChatBedrock failed: {e}")
        models['chatbedrock'] = None
    
    # Setup ChatBedrockConverse
    try:
        models['chatconverse'] = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=200,
            temperature=0.7
        )
        print("✅ ChatBedrockConverse initialized")
    except Exception as e:
        print(f"❌ ChatBedrockConverse failed: {e}")
        models['chatconverse'] = None
    
    print()
    return models

def compare_initialization_patterns():
    """Compare initialization approaches between models"""
    
    print("=== Initialization Comparison ===\n")
    
    print("ChatBedrock Initialization:")
    print("```python")
    print("ChatBedrock(")
    print("    model_id='anthropic.claude-3-haiku-20240307-v1:0',")
    print("    region_name='us-east-1',")
    print("    model_kwargs={")
    print("        'max_tokens': 200,")
    print("        'temperature': 0.7")
    print("    }")
    print(")")
    print("```")
    print("• Parameters in model_kwargs dictionary")
    print("• More verbose but flexible configuration")
    print("• Compatible with all LangChain versions")
    print()
    
    print("ChatBedrockConverse Initialization:")
    print("```python")
    print("ChatBedrockConverse(")
    print("    model_id='anthropic.claude-3-haiku-20240307-v1:0',")
    print("    region_name='us-east-1',")
    print("    max_tokens=200,")
    print("    temperature=0.7")
    print(")")
    print("```")
    print("• Direct parameter specification")
    print("• Cleaner, more intuitive syntax")
    print("• Optimized for conversation use cases")
    print()

def benchmark_performance(models):
    """Benchmark performance differences between models"""
    
    print("=== Performance Benchmark ===\n")
    
    if not all(models.values()):
        print("❌ Both models not available for benchmarking")
        return
    
    test_cases = [
        {
            "name": "Simple Query",
            "messages": [HumanMessage(content="What is Python?")]
        },
        {
            "name": "Complex Query",
            "messages": [
                SystemMessage(content="You are a technical expert."),
                HumanMessage(content="Explain the differences between synchronous and asynchronous programming with examples.")
            ]
        },
        {
            "name": "Multi-turn Conversation",
            "messages": [
                SystemMessage(content="You are a helpful tutor."),
                HumanMessage(content="What is machine learning?"),
                AIMessage(content="Machine learning is a subset of AI that enables computers to learn from data."),
                HumanMessage(content="Can you give me a practical example?")
            ]
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        print(f"Testing: {test_case['name']}")
        results[test_case['name']] = {}
        
        for model_name, model in models.items():
            if model is None:
                continue
                
            try:
                # Measure response time
                start_time = time.time()
                response = model.invoke(test_case['messages'])
                end_time = time.time()
                
                duration = end_time - start_time
                response_length = len(response.content)
                
                results[test_case['name']][model_name] = {
                    'duration': duration,
                    'response_length': response_length,
                    'success': True
                }
                
                print(f"   {model_name}: {duration:.2f}s, {response_length} chars")
                
            except Exception as e:
                results[test_case['name']][model_name] = {
                    'error': str(e),
                    'success': False
                }
                print(f"   {model_name}: ❌ {e}")
        
        print()
    
    return results

def compare_streaming_capabilities(models):
    """Compare streaming performance between models"""
    
    print("=== Streaming Comparison ===\n")
    
    if not all(models.values()):
        print("❌ Both models not available for streaming comparison")
        return
    
    test_message = HumanMessage(content="Explain the benefits of cloud computing in detail with examples.")
    
    streaming_results = {}
    
    for model_name, model in models.items():
        if model is None:
            continue
            
        print(f"Testing {model_name} streaming:")
        
        try:
            chunks = []
            start_time = time.time()
            first_chunk_time = None
            
            for chunk in model.stream([test_message]):
                if chunk.content:
                    if first_chunk_time is None:
                        first_chunk_time = time.time()
                    chunks.append(chunk.content)
            
            end_time = time.time()
            
            total_duration = end_time - start_time
            first_chunk_latency = first_chunk_time - start_time if first_chunk_time else 0
            total_content = "".join(chunks)
            
            streaming_results[model_name] = {
                'total_duration': total_duration,
                'first_chunk_latency': first_chunk_latency,
                'chunk_count': len(chunks),
                'total_length': len(total_content),
                'streaming_rate': len(total_content) / total_duration if total_duration > 0 else 0
            }
            
            print(f"   Total duration: {total_duration:.2f}s")
            print(f"   First chunk: {first_chunk_latency:.2f}s")
            print(f"   Chunks: {len(chunks)}")
            print(f"   Rate: {len(total_content) / total_duration:.1f} chars/sec")
            
        except Exception as e:
            print(f"   ❌ Streaming failed: {e}")
            streaming_results[model_name] = {'error': str(e)}
        
        print()
    
    return streaming_results

def analyze_feature_differences():
    """Analyze feature differences between models"""
    
    print("=== Feature Analysis ===\n")
    
    feature_comparison = {
        "Configuration": {
            "ChatBedrock": "model_kwargs dictionary, more verbose",
            "ChatBedrockConverse": "Direct parameters, cleaner syntax"
        },
        "Conversation Handling": {
            "ChatBedrock": "Standard LangChain message handling",
            "ChatBedrockConverse": "Enhanced conversation state management"
        },
        "Memory Management": {
            "ChatBedrock": "Manual implementation required",
            "ChatBedrockConverse": "Built-in conversation optimizations"
        },
        "Streaming": {
            "ChatBedrock": "Full streaming support with fine control",
            "ChatBedrockConverse": "Optimized streaming for conversations"
        },
        "Parameter Control": {
            "ChatBedrock": "Maximum flexibility and control",
            "ChatBedrockConverse": "Simplified, conversation-focused"
        },
        "Use Case Optimization": {
            "ChatBedrock": "General-purpose, maximum flexibility",
            "ChatBedrockConverse": "Conversation-specific optimizations"
        }
    }
    
    for feature, comparison in feature_comparison.items():
        print(f"🔍 {feature}:")
        for model, description in comparison.items():
            print(f"   {model}: {description}")
        print()

def create_decision_matrix():
    """Create decision matrix for choosing between models"""
    
    print("=== Decision Matrix ===\n")
    
    decision_factors = {
        "Use ChatBedrock When": [
            "Building non-conversational applications (Q&A, content generation)",
            "Need maximum parameter control and flexibility",
            "Working with complex custom configurations",
            "Integrating with existing ChatBedrock implementations",
            "Require compatibility with older LangChain versions",
            "Building streaming-heavy applications with custom logic"
        ],
        "Use ChatBedrockConverse When": [
            "Building conversational AI applications",
            "Need simplified configuration and setup",
            "Want enhanced multi-turn conversation support",
            "Prefer cleaner, more intuitive API",
            "Building chat interfaces and dialogue systems",
            "Need conversation-specific optimizations"
        ],
        "Performance Considerations": [
            "Both models use the same underlying Claude models",
            "Performance differences are minimal for single queries",
            "ChatBedrockConverse may have slight advantages for conversations",
            "Choose based on features, not performance",
            "Test both with your specific use case"
        ],
        "Migration Strategy": [
            "ChatBedrock → ChatBedrockConverse: Update initialization syntax",
            "Move model_kwargs parameters to direct parameters",
            "Test conversation handling improvements",
            "Validate streaming behavior changes",
            "Update error handling for new API patterns"
        ]
    }
    
    for category, factors in decision_factors.items():
        print(f"🎯 {category}:")
        for factor in factors:
            print(f"   • {factor}")
        print()

def demonstrate_migration_example():
    """Show practical migration example"""
    
    print("=== Migration Example ===\n")
    
    print("Before (ChatBedrock):")
    print("```python")
    print("from langchain_aws.chat_models import ChatBedrock")
    print("")
    print("chat = ChatBedrock(")
    print("    model_id='anthropic.claude-3-haiku-20240307-v1:0',")
    print("    region_name='us-east-1',")
    print("    model_kwargs={")
    print("        'max_tokens': 200,")
    print("        'temperature': 0.7,")
    print("        'top_p': 0.9")
    print("    }")
    print(")")
    print("```")
    print()
    
    print("After (ChatBedrockConverse):")
    print("```python")
    print("from langchain_aws.chat_models import ChatBedrockConverse")
    print("")
    print("chat = ChatBedrockConverse(")
    print("    model_id='anthropic.claude-3-haiku-20240307-v1:0',")
    print("    region_name='us-east-1',")
    print("    max_tokens=200,")
    print("    temperature=0.7,")
    print("    top_p=0.9")
    print(")")
    print("```")
    print()
    
    print("Key Changes:")
    print("• Import ChatBedrockConverse instead of ChatBedrock")
    print("• Move parameters from model_kwargs to direct parameters")
    print("• No other code changes required")
    print("• Test conversation handling improvements")

def generate_recommendation_framework():
    """Generate framework for model selection"""
    
    print("=== Recommendation Framework ===\n")
    
    print("🔍 Evaluation Questions:")
    questions = [
        "Is your primary use case conversational AI?",
        "Do you need maximum parameter control flexibility?",
        "Are you building on existing ChatBedrock code?",
        "Do you prefer simpler, cleaner APIs?",
        "Is conversation state management important?",
        "Do you need custom streaming implementations?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question}")
    
    print()
    
    print("📊 Scoring Guide:")
    print("• Conversational use case: +2 points for ChatBedrockConverse")
    print("• Maximum flexibility needed: +2 points for ChatBedrock")
    print("• Existing ChatBedrock code: +1 point for ChatBedrock")
    print("• Prefer simple APIs: +1 point for ChatBedrockConverse")
    print("• Conversation state important: +2 points for ChatBedrockConverse")
    print("• Custom streaming needed: +1 point for ChatBedrock")
    print()
    
    print("🎯 Recommendation:")
    print("• Score > 3 for ChatBedrockConverse: Use ChatBedrockConverse")
    print("• Score > 3 for ChatBedrock: Use ChatBedrock")
    print("• Tie or close: Test both with your specific use case")

if __name__ == "__main__":
    print("Module 4.4: Comparing ChatBedrock vs ChatBedrockConverse\n")
    
    # Setup and comparisons
    models = setup_comparison_models()
    compare_initialization_patterns()
    
    # Performance benchmarks
    perf_results = benchmark_performance(models)
    streaming_results = compare_streaming_capabilities(models)
    
    # Analysis and recommendations
    analyze_feature_differences()
    create_decision_matrix()
    demonstrate_migration_example()
    generate_recommendation_framework()
    
    # Summary
    print("="*50)
    print("✅ Topic 4.4 Complete!")
    print("Key Takeaways:")
    print("• Both models use same underlying Claude capabilities")
    print("• Choose based on use case, not performance")
    print("• ChatBedrockConverse optimized for conversations")
    print("• ChatBedrock provides maximum flexibility")
    print("• Migration between models is straightforward")
    print("🚀 Module 4 Complete - Ready for exercises!")
    print("="*50)