"""
Topic 3.4: Model Parameters and Configuration (7 minutes)

Learning Goals:
- Master temperature, top_p, and max_tokens parameters
- Optimize parameters for different use cases
- Understand parameter interactions and trade-offs
- Implement dynamic parameter adjustment
"""

from langchain_aws.chat_models import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
import json

def explore_temperature_effects():
    """Demonstrate temperature parameter effects"""
    
    print("=== Temperature Effects ===\n")
    
    temperatures = [0.1, 0.5, 0.9]
    prompt = "Write a creative story opening about a robot discovering emotions."
    
    for temp in temperatures:
        print(f"Temperature: {temp}")
        
        try:
            chat = ChatBedrock(
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                region_name="us-east-1",
                model_kwargs={
                    "max_tokens": 100,
                    "temperature": temp
                }
            )
            
            response = chat.invoke([HumanMessage(content=prompt)])
            print(f"Response: {response.content[:80]}...")
            
        except Exception as e:
            print(f"❌ Failed with temperature {temp}: {e}")
        
        print()

def explore_top_p_parameter():
    """Demonstrate top_p (nucleus sampling) effects"""
    
    print("=== Top-P Parameter ===\n")
    
    top_p_values = [0.1, 0.5, 0.9]
    prompt = "List three innovative uses for artificial intelligence."
    
    for top_p in top_p_values:
        print(f"Top-P: {top_p}")
        
        try:
            chat = ChatBedrock(
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                region_name="us-east-1",
                model_kwargs={
                    "max_tokens": 80,
                    "temperature": 0.7,
                    "top_p": top_p
                }
            )
            
            response = chat.invoke([HumanMessage(content=prompt)])
            print(f"Response: {response.content[:80]}...")
            
        except Exception as e:
            print(f"❌ Failed with top_p {top_p}: {e}")
        
        print()

def explore_max_tokens_impact():
    """Demonstrate max_tokens parameter impact"""
    
    print("=== Max Tokens Impact ===\n")
    
    token_limits = [50, 150, 300]
    prompt = "Explain the benefits of cloud computing in detail."
    
    for max_tokens in token_limits:
        print(f"Max Tokens: {max_tokens}")
        
        try:
            chat = ChatBedrock(
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                region_name="us-east-1",
                model_kwargs={
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                }
            )
            
            response = chat.invoke([HumanMessage(content=prompt)])
            print(f"Response length: {len(response.content)} characters")
            print(f"Content: {response.content[:100]}...")
            
        except Exception as e:
            print(f"❌ Failed with max_tokens {max_tokens}: {e}")
        
        print()

def demonstrate_parameter_combinations():
    """Show optimal parameter combinations for different use cases"""
    
    print("=== Parameter Combinations for Use Cases ===\n")
    
    use_cases = [
        {
            "name": "Factual Q&A",
            "params": {"temperature": 0.1, "top_p": 0.9, "max_tokens": 150},
            "prompt": "What is the capital of France?",
            "goal": "Accurate, consistent answers"
        },
        {
            "name": "Creative Writing",
            "params": {"temperature": 0.8, "top_p": 0.9, "max_tokens": 200},
            "prompt": "Write a poem about technology.",
            "goal": "Creative, varied responses"
        },
        {
            "name": "Code Generation",
            "params": {"temperature": 0.2, "top_p": 0.95, "max_tokens": 300},
            "prompt": "Write a Python function to sort a list.",
            "goal": "Accurate, functional code"
        },
        {
            "name": "Brainstorming",
            "params": {"temperature": 0.9, "top_p": 0.8, "max_tokens": 250},
            "prompt": "Generate ideas for a mobile app.",
            "goal": "Diverse, innovative ideas"
        }
    ]
    
    for use_case in use_cases:
        print(f"Use Case: {use_case['name']}")
        print(f"Goal: {use_case['goal']}")
        print(f"Parameters: {use_case['params']}")
        
        try:
            chat = ChatBedrock(
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                region_name="us-east-1",
                model_kwargs=use_case['params']
            )
            
            response = chat.invoke([HumanMessage(content=use_case['prompt'])])
            print(f"Result: {response.content[:100]}...")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print()

def implement_dynamic_parameter_adjustment():
    """Show dynamic parameter adjustment based on context"""
    
    print("=== Dynamic Parameter Adjustment ===\n")
    
    class AdaptiveChatBedrock:
        """ChatBedrock with adaptive parameters"""
        
        def __init__(self):
            self.base_params = {
                "max_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            }
        
        def get_params_for_task(self, task_type):
            """Get optimized parameters for specific task types"""
            
            task_params = {
                "factual": {"temperature": 0.1, "top_p": 0.9},
                "creative": {"temperature": 0.8, "top_p": 0.9},
                "analytical": {"temperature": 0.3, "top_p": 0.95},
                "conversational": {"temperature": 0.6, "top_p": 0.9}
            }
            
            params = self.base_params.copy()
            if task_type in task_params:
                params.update(task_params[task_type])
            
            return params
        
        def chat_with_task_type(self, message, task_type="conversational"):
            """Chat with task-specific parameters"""
            
            params = self.get_params_for_task(task_type)
            
            chat = ChatBedrock(
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                region_name="us-east-1",
                model_kwargs=params
            )
            
            return chat.invoke([HumanMessage(content=message)]), params
    
    # Test adaptive parameters
    adaptive_chat = AdaptiveChatBedrock()
    
    test_cases = [
        ("What is 2+2?", "factual"),
        ("Write a haiku about coding.", "creative"),
        ("Analyze the pros and cons of remote work.", "analytical")
    ]
    
    for message, task_type in test_cases:
        print(f"Task Type: {task_type}")
        print(f"Message: {message}")
        
        try:
            response, params = adaptive_chat.chat_with_task_type(message, task_type)
            print(f"Parameters used: {params}")
            print(f"Response: {response.content[:80]}...")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print()

def demonstrate_parameter_validation():
    """Show parameter validation and error handling"""
    
    print("=== Parameter Validation ===\n")
    
    def validate_parameters(params):
        """Validate ChatBedrock parameters"""
        
        errors = []
        
        # Temperature validation
        temp = params.get('temperature', 0.7)
        if not 0 <= temp <= 1:
            errors.append(f"Temperature {temp} must be between 0 and 1")
        
        # Top-p validation
        top_p = params.get('top_p', 0.9)
        if not 0 <= top_p <= 1:
            errors.append(f"Top-p {top_p} must be between 0 and 1")
        
        # Max tokens validation
        max_tokens = params.get('max_tokens', 200)
        if not 1 <= max_tokens <= 4096:
            errors.append(f"Max tokens {max_tokens} must be between 1 and 4096")
        
        return errors
    
    # Test parameter validation
    test_params = [
        {"temperature": 0.5, "top_p": 0.9, "max_tokens": 200},  # Valid
        {"temperature": 1.5, "top_p": 0.9, "max_tokens": 200},  # Invalid temp
        {"temperature": 0.5, "top_p": 1.5, "max_tokens": 200},  # Invalid top_p
        {"temperature": 0.5, "top_p": 0.9, "max_tokens": 5000}  # Invalid max_tokens
    ]
    
    for i, params in enumerate(test_params, 1):
        print(f"Test {i}: {params}")
        errors = validate_parameters(params)
        
        if errors:
            print("❌ Validation errors:")
            for error in errors:
                print(f"   • {error}")
        else:
            print("✅ Parameters valid")
        
        print()

def create_parameter_optimization_guide():
    """Create comprehensive parameter optimization guide"""
    
    print("=== Parameter Optimization Guide ===\n")
    
    guide = {
        "Temperature": {
            "range": "0.0 - 1.0",
            "effect": "Controls randomness and creativity",
            "recommendations": {
                "0.0-0.2": "Factual answers, code generation",
                "0.3-0.6": "Balanced responses, analysis",
                "0.7-0.9": "Creative writing, brainstorming",
                "0.9-1.0": "Maximum creativity, experimental"
            }
        },
        "Top-P": {
            "range": "0.0 - 1.0", 
            "effect": "Controls diversity of word choices",
            "recommendations": {
                "0.1-0.3": "Very focused, deterministic",
                "0.4-0.7": "Balanced diversity",
                "0.8-0.95": "Good diversity, recommended",
                "0.95-1.0": "Maximum diversity"
            }
        },
        "Max Tokens": {
            "range": "1 - 4096",
            "effect": "Limits response length",
            "recommendations": {
                "50-100": "Short answers, quick responses",
                "150-300": "Detailed explanations",
                "500-1000": "Long-form content",
                "1000+": "Comprehensive analysis"
            }
        }
    }
    
    for param, info in guide.items():
        print(f"📊 {param}")
        print(f"   Range: {info['range']}")
        print(f"   Effect: {info['effect']}")
        print("   Recommendations:")
        for range_val, use_case in info['recommendations'].items():
            print(f"     {range_val}: {use_case}")
        print()

if __name__ == "__main__":
    print("Module 3.4: Model Parameters and Configuration\n")
    
    # Demonstrations
    explore_temperature_effects()
    explore_top_p_parameter()
    explore_max_tokens_impact()
    demonstrate_parameter_combinations()
    implement_dynamic_parameter_adjustment()
    demonstrate_parameter_validation()
    create_parameter_optimization_guide()
    
    # Summary
    print("="*50)
    print("✅ Topic 3.4 Complete!")
    print("Key Takeaways:")
    print("• Temperature controls creativity vs consistency")
    print("• Top-p manages response diversity")
    print("• Max tokens limits response length and cost")
    print("• Different use cases need different parameters")
    print("• Dynamic adjustment improves performance")
    print("🚀 Module 3 Complete - Ready for exercises!")
    print("="*50)