"""
Module 6.1: Advanced Chain Patterns
Complex orchestration and routing patterns for enterprise applications.
"""

from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough, RunnableLambda
from pydantic import BaseModel, Field
from typing import Dict, List, Any
import json

# Initialize ChatBedrock
llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.1, "max_tokens": 1000}
)

class TaskClassification(BaseModel):
    """Classification result for routing tasks."""
    task_type: str = Field(description="Type of task: analysis, generation, or qa")
    confidence: float = Field(description="Confidence score 0-1")
    reasoning: str = Field(description="Why this classification was chosen")

class AnalysisResult(BaseModel):
    """Structured analysis output."""
    summary: str = Field(description="Brief summary")
    key_points: List[str] = Field(description="Main points identified")
    sentiment: str = Field(description="Overall sentiment")

# 1. Conditional Routing Chain
def create_routing_chain():
    """Create a chain that routes requests based on content type."""
    
    # Classification prompt
    classifier_prompt = ChatPromptTemplate.from_template(
        "Classify this request into one of: analysis, generation, qa\n"
        "Request: {input}\n"
        "Respond with JSON containing task_type, confidence, and reasoning."
    )
    
    # Specialized prompts
    analysis_prompt = ChatPromptTemplate.from_template(
        "Analyze this content thoroughly:\n{input}\n"
        "Provide summary, key points, and sentiment in JSON format."
    )
    
    generation_prompt = ChatPromptTemplate.from_template(
        "Generate creative content based on:\n{input}\n"
        "Be creative and engaging."
    )
    
    qa_prompt = ChatPromptTemplate.from_template(
        "Answer this question directly and concisely:\n{input}"
    )
    
    # Create classifier
    classifier = (
        classifier_prompt 
        | llm 
        | PydanticOutputParser(pydantic_object=TaskClassification)
    )
    
    # Create specialized chains
    analysis_chain = analysis_prompt | llm | StrOutputParser()
    generation_chain = generation_prompt | llm | StrOutputParser()
    qa_chain = qa_prompt | llm | StrOutputParser()
    
    # Route based on classification
    def route_request(classification_result):
        task_type = classification_result.task_type
        if task_type == "analysis":
            return analysis_chain
        elif task_type == "generation":
            return generation_chain
        else:
            return qa_chain
    
    # Complete routing chain
    routing_chain = (
        {"input": RunnablePassthrough(), "classification": classifier}
        | RunnableLambda(lambda x: route_request(x["classification"]).invoke(x["input"]))
    )
    
    return routing_chain

# 2. Multi-Step Processing Chain
def create_multi_step_chain():
    """Create a chain with multiple processing steps."""
    
    # Step 1: Extract key information
    extraction_prompt = ChatPromptTemplate.from_template(
        "Extract key information from this text:\n{input}\n"
        "Return as JSON with: topic, entities, keywords"
    )
    
    # Step 2: Analyze extracted information
    analysis_prompt = ChatPromptTemplate.from_template(
        "Analyze this extracted information:\n{extracted}\n"
        "Provide insights and recommendations."
    )
    
    # Step 3: Generate summary
    summary_prompt = ChatPromptTemplate.from_template(
        "Create a comprehensive summary:\n"
        "Original: {input}\n"
        "Analysis: {analysis}\n"
        "Provide actionable summary."
    )
    
    # Chain steps together
    multi_step_chain = (
        {
            "input": RunnablePassthrough(),
            "extracted": extraction_prompt | llm | StrOutputParser()
        }
        | {
            "input": lambda x: x["input"],
            "extracted": lambda x: x["extracted"],
            "analysis": lambda x: (analysis_prompt | llm | StrOutputParser()).invoke({"extracted": x["extracted"]})
        }
        | summary_prompt | llm | StrOutputParser()
    )
    
    return multi_step_chain

# 3. Parallel Processing Chain
def create_parallel_chain():
    """Create a chain that processes multiple aspects in parallel."""
    
    # Different analysis perspectives
    technical_prompt = ChatPromptTemplate.from_template(
        "Analyze from technical perspective:\n{input}"
    )
    
    business_prompt = ChatPromptTemplate.from_template(
        "Analyze from business perspective:\n{input}"
    )
    
    user_prompt = ChatPromptTemplate.from_template(
        "Analyze from user experience perspective:\n{input}"
    )
    
    # Synthesis prompt
    synthesis_prompt = ChatPromptTemplate.from_template(
        "Synthesize these different perspectives:\n"
        "Technical: {technical}\n"
        "Business: {business}\n"
        "User: {user}\n"
        "Provide unified analysis."
    )
    
    # Parallel processing
    parallel_chain = (
        {
            "technical": technical_prompt | llm | StrOutputParser(),
            "business": business_prompt | llm | StrOutputParser(),
            "user": user_prompt | llm | StrOutputParser()
        }
        | synthesis_prompt | llm | StrOutputParser()
    )
    
    return parallel_chain

# 4. Error Handling Chain
def create_robust_chain():
    """Create a chain with comprehensive error handling."""
    
    def safe_invoke(chain, input_data):
        """Safely invoke a chain with error handling."""
        try:
            return {"success": True, "result": chain.invoke(input_data)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Primary chain
    primary_prompt = ChatPromptTemplate.from_template(
        "Process this request: {input}"
    )
    primary_chain = primary_prompt | llm | StrOutputParser()
    
    # Fallback chain
    fallback_prompt = ChatPromptTemplate.from_template(
        "Provide a simple response to: {input}"
    )
    fallback_chain = fallback_prompt | llm | StrOutputParser()
    
    # Robust chain with fallback
    def robust_process(input_data):
        # Try primary chain
        result = safe_invoke(primary_chain, input_data)
        if result["success"]:
            return result["result"]
        
        # Try fallback
        fallback_result = safe_invoke(fallback_chain, input_data)
        if fallback_result["success"]:
            return f"Fallback response: {fallback_result['result']}"
        
        return "Unable to process request. Please try again."
    
    return RunnableLambda(robust_process)

# 5. Chain Composition Examples
def demonstrate_advanced_patterns():
    """Demonstrate various advanced chain patterns."""
    
    print("=== Advanced Chain Patterns Demo ===\n")
    
    # 1. Routing Chain
    print("1. Conditional Routing:")
    routing_chain = create_routing_chain()
    
    test_inputs = [
        "Analyze the sentiment of this product review: Great product, love it!",
        "Generate a creative story about a robot",
        "What is the capital of France?"
    ]
    
    for input_text in test_inputs:
        try:
            result = routing_chain.invoke(input_text)
            print(f"Input: {input_text[:50]}...")
            print(f"Output: {result[:100]}...\n")
        except Exception as e:
            print(f"Error: {e}\n")
    
    # 2. Multi-Step Chain
    print("2. Multi-Step Processing:")
    multi_step_chain = create_multi_step_chain()
    
    sample_text = "Our company launched a new AI product that increased efficiency by 40% but received mixed customer feedback."
    
    try:
        result = multi_step_chain.invoke(sample_text)
        print(f"Multi-step result: {result[:200]}...\n")
    except Exception as e:
        print(f"Error: {e}\n")
    
    # 3. Parallel Chain
    print("3. Parallel Processing:")
    parallel_chain = create_parallel_chain()
    
    try:
        result = parallel_chain.invoke(sample_text)
        print(f"Parallel analysis: {result[:200]}...\n")
    except Exception as e:
        print(f"Error: {e}\n")
    
    # 4. Robust Chain
    print("4. Error Handling:")
    robust_chain = create_robust_chain()
    
    try:
        result = robust_chain.invoke("Test error handling")
        print(f"Robust result: {result[:100]}...\n")
    except Exception as e:
        print(f"Error: {e}\n")

if __name__ == "__main__":
    demonstrate_advanced_patterns()