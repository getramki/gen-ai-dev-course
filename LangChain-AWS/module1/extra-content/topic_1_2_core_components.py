"""
Topic 1.2: Core Components: LLMs, Prompts, and Chains (6 minutes)

Learning Goals:
- Master prompt templates and engineering
- Understand LLM abstraction layer
- Learn chain composition basics
"""

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda

def explore_prompt_templates():
    """Demonstrate different types of prompt templates"""
    
    print("=== Prompt Templates ===\n")
    
    # 1. Basic Prompt Template
    basic_prompt = PromptTemplate.from_template(
        "You are a {role}. Answer this question: {question}"
    )
    
    formatted = basic_prompt.format(
        role="Python expert",
        question="What is a decorator?"
    )
    print("1. Basic Prompt Template:")
    print(f"   {formatted}\n")
    
    # 2. Chat Prompt Template
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful {role}"),
        ("user", "{question}")
    ])
    
    chat_formatted = chat_prompt.format_messages(
        role="coding assistant",
        question="Explain list comprehensions"
    )
    print("2. Chat Prompt Template:")
    for msg in chat_formatted:
        print(f"   {msg.type}: {msg.content}")
    print()

def explore_output_parsers():
    """Demonstrate output parsing capabilities"""
    
    print("=== Output Parsers ===\n")
    
    # 1. String Parser
    str_parser = StrOutputParser()
    print("1. String Parser - extracts text content")
    
    # 2. JSON Parser
    json_parser = JsonOutputParser()
    print("2. JSON Parser - parses structured output")
    
    # Example JSON parsing
    json_text = '{"name": "Python", "type": "programming language"}'
    parsed = json_parser.parse(json_text)
    print(f"   Parsed JSON: {parsed}\n")

def demonstrate_chain_basics():
    """Show basic chain composition without LLM"""
    
    print("=== Chain Composition Basics ===\n")
    
    # Create components
    prompt = PromptTemplate.from_template("Topic: {topic}\nFormat: {format}")
    
    # Custom processing function
    def process_prompt(prompt_text):
        return f"Processed: {prompt_text[:50]}..."
    
    # Create a simple chain using RunnableLambda
    processor = RunnableLambda(process_prompt)
    
    # Compose the chain
    chain = prompt | processor
    
    print("Chain: prompt | processor")
    result = chain.invoke({
        "topic": "LangChain fundamentals",
        "format": "bullet points"
    })
    print(f"Result: {result}\n")

def explore_llm_abstraction():
    """Explain LLM abstraction concepts"""
    
    print("=== LLM Abstraction Layer ===\n")
    
    print("LangChain provides unified interface for:")
    print("• OpenAI GPT models")
    print("• Anthropic Claude")
    print("• AWS Bedrock models")
    print("• Local models (Ollama, etc.)")
    print("• Custom implementations\n")
    
    print("Common LLM interface methods:")
    print("• invoke() - Single completion")
    print("• stream() - Streaming responses")
    print("• batch() - Multiple inputs")
    print("• ainvoke() - Async completion\n")

if __name__ == "__main__":
    explore_prompt_templates()
    explore_output_parsers()
    demonstrate_chain_basics()
    explore_llm_abstraction()
    
    print("="*50)
    print("✅ Topic 1.2 Complete!")
    print("Key Takeaways:")
    print("• Prompt templates enable dynamic content generation")
    print("• Output parsers structure LLM responses")
    print("• Chains compose components using | operator")
    print("• LLM abstraction provides unified interface")
    print("="*50)