"""
Topic 1.1: Introduction to LangChain Architecture (5 minutes)

Learning Goals:
- Understand LangChain ecosystem and philosophy
- Explore core components hierarchy
- Learn design patterns and abstractions
"""

from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def explore_langchain_architecture():
    """Demonstrate LangChain's modular architecture"""
    
    print("=== LangChain Architecture Overview ===\n")
    
    # 1. Core Philosophy: Everything is a Runnable
    print("1. Runnable Interface - Everything in LangChain implements Runnable:")
    
    # Simple runnable example
    class SimpleRunnable(Runnable):
        def invoke(self, input_data):
            return f"Processed: {input_data}"
    
    simple = SimpleRunnable()
    result = simple.invoke("Hello LangChain")
    print(f"   Result: {result}\n")
    
    # 2. Component Hierarchy
    print("2. LangChain Component Hierarchy:")
    print("   ├── langchain-core (Base abstractions)")
    print("   ├── langchain-community (Integrations)")
    print("   ├── langchain (Main package)")
    print("   └── langchain-aws (AWS-specific)\n")
    
    # 3. Key Design Patterns
    print("3. Key Design Patterns:")
    print("   • Composability: Chain components together")
    print("   • Abstraction: Unified interfaces for different providers")
    print("   • Streaming: Real-time data processing")
    print("   • Async Support: Non-blocking operations\n")

def demonstrate_composability():
    """Show how LangChain components compose together"""
    
    print("=== Composability Example ===\n")
    
    # Create a simple prompt template
    prompt = PromptTemplate.from_template("Explain {topic} in simple terms")
    parser = StrOutputParser()
    
    # Show component composition (without LLM for now)
    print("Components can be chained:")
    print("prompt | llm | parser")
    print("(We'll add the LLM in the next module)\n")
    
    # Demonstrate prompt formatting
    formatted = prompt.format(topic="machine learning")
    print(f"Formatted prompt: {formatted}")

if __name__ == "__main__":
    explore_langchain_architecture()
    demonstrate_composability()
    
    print("\n" + "="*50)
    print("✅ Topic 1.1 Complete!")
    print("Key Takeaways:")
    print("• LangChain uses Runnable interface for everything")
    print("• Modular architecture enables easy composition")
    print("• Design patterns focus on reusability and abstraction")
    print("="*50)