"""
Topic 5.1: Building a Document Q&A System (8 minutes)

Learning Goals:
- Implement PDF document loading and processing
- Master text chunking strategies for optimal retrieval
- Build question-answering pipelines with context
- Create production-ready document Q&A systems
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os
from typing import List, Dict

def setup_document_qa_system():
    """Initialize components for document Q&A system"""
    
    print("=== Document Q&A System Setup ===\n")
    
    try:
        # Initialize ChatBedrockConverse
        chat = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=400,
            temperature=0.3  # Lower temperature for factual responses
        )
        
        print("✅ ChatBedrockConverse initialized for document Q&A")
        return chat
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return None

def create_sample_document():
    """Create a sample document for testing"""
    
    print("=== Creating Sample Document ===\n")
    
    sample_content = """
# LangChain with AWS Bedrock Guide

## Introduction
LangChain is a powerful framework for building applications with large language models (LLMs). 
When combined with AWS Bedrock, it provides access to high-quality foundation models like Claude, 
Titan, and others through a unified interface.

## Key Features
- **Model Abstraction**: Unified interface across different LLM providers
- **Chain Composition**: Build complex workflows by chaining components
- **Memory Management**: Maintain conversation context across interactions
- **Document Processing**: Load, split, and process various document types

## AWS Bedrock Integration
AWS Bedrock provides serverless access to foundation models from leading AI companies:
- Anthropic Claude models for conversational AI
- Amazon Titan models for text generation and embeddings
- Stability AI models for image generation
- Cohere models for text analysis and generation

## Best Practices
1. Choose appropriate models based on use case requirements
2. Implement proper error handling and retry logic
3. Monitor token usage and costs
4. Use streaming for better user experience
5. Implement proper security and access controls

## Common Use Cases
- Chatbots and conversational AI
- Document question-answering systems
- Content generation and summarization
- Code generation and analysis
- Multi-modal applications with text and images
"""
    
    # Create sample document file
    doc_path = "sample_documents/langchain_guide.txt"
    os.makedirs("sample_documents", exist_ok=True)
    
    try:
        with open(doc_path, 'w') as f:
            f.write(sample_content)
        
        print(f"✅ Sample document created: {doc_path}")
        return doc_path
        
    except Exception as e:
        print(f"❌ Failed to create sample document: {e}")
        return None

def demonstrate_text_splitting():
    """Demonstrate different text splitting strategies"""
    
    print("=== Text Splitting Strategies ===\n")
    
    # Create sample document
    doc_path = create_sample_document()
    if not doc_path:
        return None
    
    # Load document content
    with open(doc_path, 'r') as f:
        text = f.read()
    
    # Strategy 1: Character-based splitting
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    
    char_chunks = char_splitter.split_text(text)
    
    print("1. Character-based Splitting:")
    print(f"   Original length: {len(text)} characters")
    print(f"   Number of chunks: {len(char_chunks)}")
    print(f"   Average chunk size: {sum(len(chunk) for chunk in char_chunks) / len(char_chunks):.0f} chars")
    print(f"   Sample chunk: {char_chunks[0][:100]}...")
    print()
    
    # Strategy 2: Semantic splitting (by sections)
    sections = text.split('\n## ')
    semantic_chunks = [section.strip() for section in sections if section.strip()]
    
    print("2. Semantic Splitting (by sections):")
    print(f"   Number of sections: {len(semantic_chunks)}")
    print(f"   Section titles: {[chunk.split('\\n')[0] for chunk in semantic_chunks[:3]]}")
    print()
    
    return char_chunks

def build_qa_pipeline(chat, chunks):
    """Build question-answering pipeline"""
    
    print("=== Q&A Pipeline Construction ===\n")
    
    if not chat or not chunks:
        print("❌ Missing components for Q&A pipeline")
        return None
    
    # Create Q&A prompt template
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that answers questions based on provided context. 
        Use only the information from the context to answer questions. 
        If the answer is not in the context, say "I don't have enough information to answer that question."
        
        Context:
        {context}"""),
        ("human", "{question}")
    ])
    
    def answer_question(question: str, max_chunks: int = 3):
        """Answer question using relevant document chunks"""
        
        # Simple relevance scoring (in production, use embeddings)
        question_words = set(question.lower().split())
        
        chunk_scores = []
        for i, chunk in enumerate(chunks):
            chunk_words = set(chunk.lower().split())
            overlap = len(question_words.intersection(chunk_words))
            chunk_scores.append((i, overlap, chunk))
        
        # Sort by relevance and take top chunks
        chunk_scores.sort(key=lambda x: x[1], reverse=True)
        relevant_chunks = [chunk for _, _, chunk in chunk_scores[:max_chunks]]
        
        # Combine relevant chunks as context
        context = "\n\n".join(relevant_chunks)
        
        # Generate answer
        messages = qa_prompt.format_messages(
            context=context,
            question=question
        )
        
        try:
            response = chat.invoke(messages)
            return {
                "answer": response.content,
                "context_used": len(relevant_chunks),
                "context_length": len(context)
            }
        except Exception as e:
            return {"error": f"Failed to generate answer: {e}"}
    
    print("✅ Q&A pipeline constructed")
    return answer_question

def test_qa_system(qa_function):
    """Test the Q&A system with sample questions"""
    
    print("=== Q&A System Testing ===\n")
    
    if not qa_function:
        print("❌ Q&A function not available")
        return
    
    test_questions = [
        "What is LangChain?",
        "What models are available in AWS Bedrock?",
        "What are the best practices mentioned?",
        "How do you implement streaming?",  # Not in context
        "What are common use cases for LangChain?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"Question {i}: {question}")
        
        result = qa_function(question)
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"Answer: {result['answer'][:150]}...")
            print(f"Context: {result['context_used']} chunks, {result['context_length']} chars")
        
        print()

def implement_advanced_qa_features():
    """Implement advanced Q&A features"""
    
    print("=== Advanced Q&A Features ===\n")
    
    class AdvancedDocumentQA:
        """Advanced document Q&A system with enhanced features"""
        
        def __init__(self, chat_model):
            self.chat = chat_model
            self.documents = {}
            self.chunks = {}
            
        def add_document(self, doc_id: str, content: str):
            """Add document to the system"""
            
            # Split document into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=400,
                chunk_overlap=50
            )
            
            chunks = splitter.split_text(content)
            
            self.documents[doc_id] = content
            self.chunks[doc_id] = chunks
            
            return len(chunks)
        
        def answer_with_sources(self, question: str, doc_ids: List[str] = None):
            """Answer question with source attribution"""
            
            if doc_ids is None:
                doc_ids = list(self.documents.keys())
            
            # Collect relevant chunks from specified documents
            all_chunks = []
            for doc_id in doc_ids:
                if doc_id in self.chunks:
                    for i, chunk in enumerate(self.chunks[doc_id]):
                        all_chunks.append({
                            "content": chunk,
                            "source": doc_id,
                            "chunk_id": i
                        })
            
            # Simple relevance scoring
            question_words = set(question.lower().split())
            scored_chunks = []
            
            for chunk_info in all_chunks:
                chunk_words = set(chunk_info["content"].lower().split())
                overlap = len(question_words.intersection(chunk_words))
                if overlap > 0:
                    scored_chunks.append((overlap, chunk_info))
            
            # Sort and take top 3
            scored_chunks.sort(key=lambda x: x[0], reverse=True)
            top_chunks = [chunk_info for _, chunk_info in scored_chunks[:3]]
            
            if not top_chunks:
                return {
                    "answer": "I don't have relevant information to answer that question.",
                    "sources": []
                }
            
            # Build context with source information
            context_parts = []
            sources = []
            
            for chunk_info in top_chunks:
                context_parts.append(f"[Source: {chunk_info['source']}]\n{chunk_info['content']}")
                sources.append({
                    "document": chunk_info['source'],
                    "chunk": chunk_info['chunk_id']
                })
            
            context = "\n\n".join(context_parts)
            
            # Generate answer with source awareness
            prompt = f"""Based on the following context, answer the question. 
            Include source references in your answer when possible.
            
            Context:
            {context}
            
            Question: {question}
            
            Answer:"""
            
            try:
                response = self.chat.invoke([HumanMessage(content=prompt)])
                
                return {
                    "answer": response.content,
                    "sources": sources,
                    "context_chunks": len(top_chunks)
                }
                
            except Exception as e:
                return {"error": f"Failed to generate answer: {e}"}
    
    # Test advanced Q&A system
    chat = setup_document_qa_system()
    if chat:
        advanced_qa = AdvancedDocumentQA(chat)
        
        # Add sample document
        doc_path = create_sample_document()
        if doc_path:
            with open(doc_path, 'r') as f:
                content = f.read()
            
            chunks_added = advanced_qa.add_document("langchain_guide", content)
            print(f"Added document with {chunks_added} chunks")
            
            # Test with source attribution
            result = advanced_qa.answer_with_sources("What are the key features of LangChain?")
            
            if "error" not in result:
                print(f"Answer: {result['answer'][:200]}...")
                print(f"Sources: {result['sources']}")
            else:
                print(f"❌ {result['error']}")

if __name__ == "__main__":
    print("Module 5.1: Building a Document Q&A System\n")
    
    # Setup and demonstrations
    chat = setup_document_qa_system()
    chunks = demonstrate_text_splitting()
    
    # Build and test Q&A pipeline
    qa_function = build_qa_pipeline(chat, chunks)
    test_qa_system(qa_function)
    
    # Advanced features
    implement_advanced_qa_features()
    
    # Summary
    print("="*50)
    print("✅ Topic 5.1 Complete!")
    print("Key Takeaways:")
    print("• Document processing requires strategic text chunking")
    print("• Q&A systems need context-aware prompt engineering")
    print("• Source attribution enhances answer reliability")
    print("• Simple relevance scoring can be effective for basic use cases")
    print("🚀 Ready for Topic 5.2: Code Assistant!")
    print("="*50)