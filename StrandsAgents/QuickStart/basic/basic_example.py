#!/usr/bin/env python3
"""
StrandsAgents Basic Example
A simple demonstration of creating and using an agent with tools.
"""

from strands import Agent, tool

@tool(name="calculator", description="Perform mathematical calculations")
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

@tool(name="text_analyzer", description="Analyze text statistics")
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
    # Create agent with decorated tools
    agent = Agent(
        name="UtilityAgent",
        description="A utility agent that can calculate and analyze text",
        tools=[calculator, text_analyzer]
    )
    
    # Example interactions
    print("=== StrandsAgents Basic Example ===\n")
    
    # Math calculation
    print("1. Mathematical calculation:")
    agent("Calculate 25 * 4 + 10")
    print()
    
    # Text analysis
    print("2. Text analysis:")
    sample_text = "Hello world! This is a sample text for analysis. How are you?"
    agent(f"Analyze this text: {sample_text}")
    print()
    
    print("=== Example Complete ===")

if __name__ == "__main__":
    main()