"""
05 - Advanced Tools

This script demonstrates:
- Multiple complex tools
- Tools with error handling
- Tools that call external APIs (simulated)
- Tool chaining

Prerequisites:
- Completed 04-tools-basic.py
"""

from langchain_aws import ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
import json
import random

print("="*60)
print("Advanced Tools Examples")
print("="*60 + "\n")

# Initialize the model
llm = ChatBedrock(
    model_id="us.amazon.nova-pro-v1:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.3, "max_tokens": 1500}
)

# Advanced Tool 1: Weather Simulator (simulates API call)
print("Creating Tool 1: Weather Simulator")
def get_weather(city: str) -> str:
    """Get weather information for a city (simulated)."""
    try:
        # Simulate API call with random data
        weather_conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
        temp = random.randint(15, 30)
        condition = random.choice(weather_conditions)
        
        weather_data = {
            "city": city,
            "temperature": f"{temp}°C",
            "condition": condition,
            "humidity": f"{random.randint(40, 80)}%"
        }
        return json.dumps(weather_data, indent=2)
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

weather_tool = Tool(
    name="WeatherAPI",
    func=get_weather,
    description="Get current weather for a city. Input should be the city name."
)
print("✓ Weather tool created\n")

# Advanced Tool 2: Data Analyzer
print("Creating Tool 2: Data Analyzer")
def analyze_numbers(numbers_str: str) -> str:
    """Analyze a list of numbers and return statistics."""
    try:
        # Parse comma-separated numbers
        numbers = [float(x.strip()) for x in numbers_str.split(',')]
        
        if not numbers:
            return "No numbers provided"
        
        stats = {
            "count": len(numbers),
            "sum": sum(numbers),
            "average": sum(numbers) / len(numbers),
            "min": min(numbers),
            "max": max(numbers)
        }
        return json.dumps(stats, indent=2)
    except Exception as e:
        return f"Error analyzing numbers: {str(e)}. Please provide comma-separated numbers."

analyzer_tool = Tool(
    name="DataAnalyzer",
    func=analyze_numbers,
    description="Analyze a list of numbers. Input should be comma-separated numbers like '1,2,3,4,5'."
)
print("✓ Data analyzer tool created\n")

# Advanced Tool 3: Text Processor
print("Creating Tool 3: Text Processor")
def process_text(text: str) -> str:
    """Process text with various operations."""
    try:
        operations = {
            "original": text,
            "uppercase": text.upper(),
            "lowercase": text.lower(),
            "word_count": len(text.split()),
            "char_count": len(text),
            "reversed": text[::-1]
        }
        return json.dumps(operations, indent=2)
    except Exception as e:
        return f"Error processing text: {str(e)}"

text_processor_tool = Tool(
    name="TextProcessor",
    func=process_text,
    description="Process text with various operations (uppercase, lowercase, reverse, count). Input should be the text to process."
)
print("✓ Text processor tool created\n")

# Advanced Tool 4: Unit Converter
print("Creating Tool 4: Unit Converter")
def convert_units(conversion: str) -> str:
    """Convert between units. Format: 'value unit1 to unit2'"""
    try:
        parts = conversion.lower().split()
        if len(parts) != 4 or parts[2] != 'to':
            return "Format should be: 'value unit1 to unit2' (e.g., '100 celsius to fahrenheit')"
        
        value = float(parts[0])
        from_unit = parts[1]
        to_unit = parts[3]
        
        conversions = {
            ('celsius', 'fahrenheit'): lambda x: (x * 9/5) + 32,
            ('fahrenheit', 'celsius'): lambda x: (x - 32) * 5/9,
            ('km', 'miles'): lambda x: x * 0.621371,
            ('miles', 'km'): lambda x: x / 0.621371,
            ('kg', 'pounds'): lambda x: x * 2.20462,
            ('pounds', 'kg'): lambda x: x / 2.20462,
        }
        
        key = (from_unit, to_unit)
        if key in conversions:
            result = conversions[key](value)
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        else:
            return f"Conversion from {from_unit} to {to_unit} not supported"
    except Exception as e:
        return f"Error converting: {str(e)}"

converter_tool = Tool(
    name="UnitConverter",
    func=convert_units,
    description="Convert between units. Input format: 'value unit1 to unit2'. Supports: celsius/fahrenheit, km/miles, kg/pounds."
)
print("✓ Unit converter tool created\n")

# Create agent with all advanced tools
print("Creating agent with advanced tools...")
tools = [weather_tool, analyzer_tool, text_processor_tool, converter_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the available tools to answer questions."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=5
)
print("✓ Agent created\n")

# Test advanced tools
print("="*60)
print("Testing Advanced Tools")
print("="*60 + "\n")

# Test 1: Weather
print("Test 1: Weather Query")
print("-" * 60)
response = agent_executor.invoke({"input": "What's the weather like in London?"})
print(f"\nFinal Answer: {response['output']}\n")

# Test 2: Data Analysis
print("Test 2: Data Analysis")
print("-" * 60)
response = agent_executor.invoke({
    "input": "Analyze these numbers: 10, 20, 30, 40, 50"
})
print(f"\nFinal Answer: {response['output']}\n")

# Test 3: Unit Conversion
print("Test 3: Unit Conversion")
print("-" * 60)
response = agent_executor.invoke({
    "input": "Convert 100 celsius to fahrenheit"
})
print(f"\nFinal Answer: {response['output']}\n")

print("="*60)
print("\n✓ Advanced tools complete!")
print("\nWhat you learned:")
print("- How to create complex tools with error handling")
print("- How to simulate API calls in tools")
print("- How to parse and validate tool inputs")
print("- How to return structured data (JSON) from tools")
print("- How agents handle multiple complex tools")
