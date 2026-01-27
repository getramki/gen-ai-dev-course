"""
03 - Dynamic Model Configuration

This script demonstrates:
- Switching between models at runtime
- Adjusting parameters dynamically based on task
- Using different configurations for different purposes

Prerequisites:
- Completed 02-static-model.py
"""

from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, SystemMessage

class DynamicModelManager:
    """Manages different model configurations dynamically."""
    
    def __init__(self, region="us-east-1"):
        self.region = region
        self.model_id = "us.amazon.nova-pro-v1:0"
    
    def get_model(self, task_type: str) -> ChatBedrock:
        """
        Get a model configured for specific task type.
        
        Args:
            task_type: One of 'creative', 'analytical', 'conversational', 'concise'
        """
        configs = {
            'creative': {
                'temperature': 0.9,
                'max_tokens': 800,
                'top_p': 0.95
            },
            'analytical': {
                'temperature': 0.2,
                'max_tokens': 1000,
                'top_p': 0.5
            },
            'conversational': {
                'temperature': 0.7,
                'max_tokens': 500,
                'top_p': 0.85
            },
            'concise': {
                'temperature': 0.3,
                'max_tokens': 200,
                'top_p': 0.6
            }
        }
        
        config = configs.get(task_type, configs['conversational'])
        
        return ChatBedrock(
            model_id=self.model_id,
            region_name=self.region,
            model_kwargs=config
        )
    
    def adjust_temperature(self, base_temp: float, creativity_boost: float) -> ChatBedrock:
        """Dynamically adjust temperature based on user preference."""
        final_temp = min(1.0, max(0.0, base_temp + creativity_boost))
        
        return ChatBedrock(
            model_id=self.model_id,
            region_name=self.region,
            model_kwargs={
                'temperature': final_temp,
                'max_tokens': 500,
                'top_p': 0.8
            }
        )

# Example Usage
print("="*60)
print("Dynamic Model Configuration Examples")
print("="*60 + "\n")

manager = DynamicModelManager()

# Example 1: Creative Task
print("Example 1: Creative Writing Task")
print("-" * 60)
creative_model = manager.get_model('creative')
response = creative_model.invoke([
    HumanMessage(content="Write a creative tagline for a coffee shop.")
])
print(f"Response: {response.content}\n")

# Example 2: Analytical Task
print("Example 2: Analytical Task")
print("-" * 60)
analytical_model = manager.get_model('analytical')
response = analytical_model.invoke([
    HumanMessage(content="Calculate the compound interest on $1000 at 5% for 3 years.")
])
print(f"Response: {response.content}\n")

# Example 3: Conversational Task
print("Example 3: Conversational Task")
print("-" * 60)
conversational_model = manager.get_model('conversational')
response = conversational_model.invoke([
    HumanMessage(content="How's the weather today?")
])
print(f"Response: {response.content}\n")

# Example 4: Concise Task
print("Example 4: Concise Response Task")
print("-" * 60)
concise_model = manager.get_model('concise')
response = concise_model.invoke([
    HumanMessage(content="What is machine learning?")
])
print(f"Response: {response.content}\n")

# Example 5: Dynamic Temperature Adjustment
print("Example 5: Dynamic Temperature Adjustment")
print("-" * 60)
base_temp = 0.5
creativity_boost = 0.3
adjusted_model = manager.adjust_temperature(base_temp, creativity_boost)
print(f"Base temperature: {base_temp}")
print(f"Creativity boost: {creativity_boost}")
print(f"Final temperature: {base_temp + creativity_boost}")
response = adjusted_model.invoke([
    HumanMessage(content="Describe a sunset.")
])
print(f"Response: {response.content}\n")

print("="*60)
print("\n✓ Dynamic model configuration complete!")
print("\nWhat you learned:")
print("- How to switch models based on task type")
print("- How to adjust parameters dynamically")
print("- How to create a model manager class")
print("- When to use different configurations")
