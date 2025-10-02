"""
Exercise 1: Build Your First LangChain Pipeline

Task: Create a text processing pipeline using LCEL that:
1. Takes user input
2. Formats it with a prompt template
3. Processes it through multiple steps
4. Returns structured output

Time: 5 minutes
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.output_parsers import JsonOutputParser

def create_text_analyzer():
    """Create a text analysis pipeline"""
    
    # TODO: Create a prompt template that asks for text analysis
    prompt = PromptTemplate.from_template(
        "Analyze this text: {text}\nProvide insights about length, words, and sentiment."
    )
    
    # TODO: Create analysis functions
    def analyze_length(text):
        return len(text)
    
    def analyze_words(text):
        return len(text.split())
    
    def analyze_sentiment(text):
        # Simple sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'poor']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    # TODO: Create parallel analysis runnable
    analyzer = RunnableParallel(
        length=RunnableLambda(analyze_length),
        words=RunnableLambda(analyze_words),
        sentiment=RunnableLambda(analyze_sentiment)
    )
    
    # TODO: Create the complete chain
    # Format: input -> prompt -> analyzer -> formatter
    def format_results(analysis_dict):
        return {
            "analysis": analysis_dict,
            "summary": f"Text has {analysis_dict['words']} words, {analysis_dict['length']} characters, sentiment: {analysis_dict['sentiment']}"
        }
    
    chain = (
        {"text": lambda x: x}  # Pass input as 'text' key
        | prompt
        | RunnableLambda(lambda prompt_value: prompt_value.text.split("Analyze this text: ")[1].split("\nProvide")[0])
        | analyzer
        | RunnableLambda(format_results)
    )
    
    return chain

def test_analyzer():
    """Test the text analyzer"""
    
    analyzer = create_text_analyzer()
    
    test_texts = [
        "This is a great example of LangChain!",
        "I think this is a terrible implementation.",
        "LangChain provides powerful tools for developers."
    ]
    
    print("=== Text Analysis Results ===\n")
    
    for i, text in enumerate(test_texts, 1):
        print(f"Test {i}: '{text}'")
        result = analyzer.invoke(text)
        print(f"Result: {result['summary']}")
        print(f"Details: {result['analysis']}\n")

if __name__ == "__main__":
    test_analyzer()
    
    print("✅ Exercise 1 Complete!")
    print("\nChallenge: Modify the chain to:")
    print("• Add more analysis functions")
    print("• Include error handling")
    print("• Support batch processing")