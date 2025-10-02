#!/usr/bin/env python3
"""
StrandsAgents Basic Example
A simple demonstration of creating and using an agent with tools.
"""

from strands import Agent, tool

def calculator(expression: str) -> str:
    """Calculate mathematical expressions safely"""
    try:
        # Basic safety check - only allow numbers and basic operators
        allowed_chars = set('0123456789+-*/().')
        if not all(c in allowed_chars or c.isspace() for c in expression):
            return "Error: Invalid characters in expression"
        
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

def text_analyzer(text: str) -> str:
    """Analyze text and return basic statistics"""
    words = text.split()
    chars = len(text)
    sentences = text.count('.') + text.count('!') + text.count('?')
    
    return f"""Text Analysis:
- Characters: {chars}
- Words: {len(words)}
- Sentences: {sentences}
- Average word length: {chars/len(words):.1f} chars"""

def main():
    # Create tools
    calc_tool = tool(
        name="calculator",
        description="Perform mathematical calculations",
        function=calculator
    )
    
    analyzer_tool = tool(
        name="text_analyzer", 
        description="Analyze text statistics",
        function=text_analyzer
    )
    
    # Create agent with multiple tools
    agent = Agent(
        name="UtilityAgent",
        description="A utility agent that can calculate and analyze text",
        tools=[calc_tool, analyzer_tool]
    )
    
    # Example interactions
    print("=== StrandsAgents Basic Example ===\n")
    
    # Math calculation
    print("1. Mathematical calculation:")
    response = agent.run("Calculate 25 * 4 + 10")
    print(f"Response: {response}\n")
    
    # Text analysis
    print("2. Text analysis:")
    sample_text = "Hello world! This is a sample text for analysis. How are you?"
    response = agent.run(f"Analyze this text: {sample_text}")
    print(f"Response: {response}\n")
    
    print("=== Example Complete ===")

if __name__ == "__main__":
    main()