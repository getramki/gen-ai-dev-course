"""
Topic 1.3: LangChain Expression Language (LCEL) Basics (5 minutes)

Learning Goals:
- Master LCEL syntax and operators
- Understand pipe operations and data flow
- Learn Runnable interface patterns
"""

from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def explore_lcel_syntax():
    """Demonstrate LCEL syntax and basic operations"""
    
    print("=== LCEL Syntax Basics ===\n")
    
    # 1. Pipe Operator |
    print("1. Pipe Operator (|) - Sequential composition:")
    
    def add_prefix(text):
        return f"PREFIX: {text}"
    
    def add_suffix(text):
        return f"{text} :SUFFIX"
    
    # Create runnables
    prefix_runnable = RunnableLambda(add_prefix)
    suffix_runnable = RunnableLambda(add_suffix)
    
    # Chain with pipe operator
    chain = prefix_runnable | suffix_runnable
    result = chain.invoke("Hello LCEL")
    print(f"   Input: 'Hello LCEL'")
    print(f"   Output: '{result}'\n")

def explore_parallel_execution():
    """Demonstrate parallel execution with RunnableParallel"""
    
    print("=== Parallel Execution ===\n")
    
    def get_length(text):
        return len(text)
    
    def get_words(text):
        return len(text.split())
    
    def get_upper(text):
        return text.upper()
    
    # Create parallel runnable
    parallel = RunnableParallel(
        length=RunnableLambda(get_length),
        words=RunnableLambda(get_words),
        upper=RunnableLambda(get_upper)
    )
    
    result = parallel.invoke("LangChain is powerful")
    print("Parallel processing results:")
    for key, value in result.items():
        print(f"   {key}: {value}")
    print()

def explore_passthrough_patterns():
    """Demonstrate RunnablePassthrough for data flow"""
    
    print("=== Passthrough Patterns ===\n")
    
    # Using RunnablePassthrough to maintain original input
    def analyze_text(text):
        return {
            "analysis": f"Text has {len(text)} characters",
            "original": text
        }
    
    # Chain that preserves input
    chain = RunnablePassthrough.assign(
        analysis=RunnableLambda(lambda x: f"Length: {len(x)}")
    )
    
    result = chain.invoke("LCEL example")
    print("Passthrough with assignment:")
    print(f"   Input preserved: {result}")
    print()

def demonstrate_complex_lcel():
    """Show more complex LCEL composition"""
    
    print("=== Complex LCEL Composition ===\n")
    
    # Create prompt template
    prompt = PromptTemplate.from_template("Analyze: {text}")
    
    # Create processing functions
    def extract_info(formatted_prompt):
        # Simulate extracting info from prompt
        return {
            "prompt": formatted_prompt,
            "length": len(formatted_prompt),
            "type": "analysis_request"
        }
    
    def format_response(info_dict):
        return f"Response: {info_dict['type']} ({info_dict['length']} chars)"
    
    # Complex chain composition
    chain = (
        {"text": RunnablePassthrough()}
        | prompt
        | RunnableLambda(extract_info)
        | RunnableLambda(format_response)
    )
    
    result = chain.invoke("LangChain LCEL")
    print("Complex chain result:")
    print(f"   {result}\n")

def explore_lcel_benefits():
    """Explain LCEL benefits and use cases"""
    
    print("=== LCEL Benefits ===\n")
    
    print("Key advantages of LCEL:")
    print("• Readable: Code reads like data flow")
    print("• Composable: Easy to combine components")
    print("• Streaming: Built-in streaming support")
    print("• Parallel: Automatic parallelization")
    print("• Async: Native async/await support")
    print("• Debugging: Clear execution traces\n")
    
    print("Common LCEL patterns:")
    print("• prompt | llm | parser")
    print("• RunnableParallel for concurrent tasks")
    print("• RunnablePassthrough for data preservation")
    print("• Conditional logic with RunnableBranch")

if __name__ == "__main__":
    explore_lcel_syntax()
    explore_parallel_execution()
    explore_passthrough_patterns()
    demonstrate_complex_lcel()
    explore_lcel_benefits()
    
    print("="*50)
    print("✅ Topic 1.3 Complete!")
    print("Key Takeaways:")
    print("• LCEL uses | operator for sequential composition")
    print("• RunnableParallel enables concurrent execution")
    print("• RunnablePassthrough preserves data flow")
    print("• LCEL provides readable, composable chains")
    print("="*50)