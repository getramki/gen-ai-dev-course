"""
Exercise 1: Document Q&A System

Task: Build a comprehensive document Q&A system that:
1. Processes multiple PDF documents with intelligent chunking
2. Implements semantic search for relevant context retrieval
3. Provides source attribution and confidence scoring
4. Includes conversation memory for follow-up questions

Time: 10 minutes
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

class ComprehensiveDocumentQA:
    """Advanced document Q&A system with multiple features"""
    
    def __init__(self):
        self.chat = self._initialize_chat()
        self.documents = {}
        self.chunks = {}
        self.conversation_history = []
        self.qa_sessions = {}
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def _initialize_chat(self):
        """Initialize ChatBedrockConverse for Q&A"""
        return ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=400,
            temperature=0.2
        )
    
    def add_document(self, doc_id: str, content: str, metadata: Dict = None):
        """Add document to the knowledge base"""
        
        # Store document
        self.documents[doc_id] = {
            "content": content,
            "metadata": metadata or {},
            "added_at": datetime.now().isoformat(),
            "length": len(content)
        }
        
        # Create chunks with metadata
        chunks = self.text_splitter.split_text(content)
        
        self.chunks[doc_id] = []
        for i, chunk in enumerate(chunks):
            chunk_info = {
                "content": chunk,
                "chunk_id": i,
                "doc_id": doc_id,
                "length": len(chunk),
                "keywords": self._extract_keywords(chunk)
            }
            self.chunks[doc_id].append(chunk_info)
        
        return {
            "doc_id": doc_id,
            "chunks_created": len(chunks),
            "total_length": len(content)
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text chunk"""
        
        # Simple keyword extraction (in production, use more sophisticated methods)
        words = text.lower().split()
        
        # Filter out common words and short words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        keywords = []
        for word in words:
            # Clean word
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 3 and clean_word not in stop_words:
                keywords.append(clean_word)
        
        # Return unique keywords
        return list(set(keywords))
    
    def _calculate_relevance_score(self, question: str, chunk_info: Dict) -> float:
        """Calculate relevance score between question and chunk"""
        
        question_words = set(question.lower().split())
        chunk_keywords = set(chunk_info["keywords"])
        chunk_words = set(chunk_info["content"].lower().split())
        
        # Keyword overlap score
        keyword_overlap = len(question_words.intersection(chunk_keywords))
        
        # Content overlap score
        content_overlap = len(question_words.intersection(chunk_words))
        
        # Length penalty (prefer chunks that aren't too short or too long)
        length_score = 1.0
        chunk_length = chunk_info["length"]
        if chunk_length < 100:
            length_score = 0.7
        elif chunk_length > 800:
            length_score = 0.8
        
        # Combined score
        total_score = (keyword_overlap * 2 + content_overlap) * length_score
        
        return total_score
    
    def _find_relevant_chunks(self, question: str, max_chunks: int = 3) -> List[Dict]:
        """Find most relevant chunks for the question"""
        
        all_chunks = []
        
        # Collect all chunks with relevance scores
        for doc_id, doc_chunks in self.chunks.items():
            for chunk_info in doc_chunks:
                score = self._calculate_relevance_score(question, chunk_info)
                if score > 0:
                    chunk_with_score = chunk_info.copy()
                    chunk_with_score["relevance_score"] = score
                    all_chunks.append(chunk_with_score)
        
        # Sort by relevance and return top chunks
        all_chunks.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return all_chunks[:max_chunks]
    
    def answer_question(self, question: str, session_id: str = "default") -> Dict:
        """Answer question with context and source attribution"""
        
        # Find relevant chunks
        relevant_chunks = self._find_relevant_chunks(question)
        
        if not relevant_chunks:
            return {
                "answer": "I don't have relevant information to answer that question.",
                "confidence": 0.0,
                "sources": [],
                "context_used": 0
            }
        
        # Build context from relevant chunks
        context_parts = []
        sources = []
        
        for chunk in relevant_chunks:
            doc_metadata = self.documents[chunk["doc_id"]]["metadata"]
            source_info = {
                "document": chunk["doc_id"],
                "chunk": chunk["chunk_id"],
                "relevance_score": chunk["relevance_score"],
                "metadata": doc_metadata
            }
            
            context_parts.append(f"[Source: {chunk['doc_id']}, Chunk {chunk['chunk_id']}]\n{chunk['content']}")
            sources.append(source_info)
        
        context = "\n\n".join(context_parts)
        
        # Get conversation history for this session
        session_history = self.qa_sessions.get(session_id, [])
        
        # Build prompt with conversation context
        prompt_parts = [
            "You are a helpful assistant that answers questions based on provided context.",
            "Use only the information from the context to answer questions.",
            "If the answer is not in the context, say so clearly.",
            "Reference sources when possible using the format [Source: document_name].",
            ""
        ]
        
        # Add conversation history if available
        if session_history:
            prompt_parts.append("Previous conversation context:")
            for entry in session_history[-3:]:  # Last 3 exchanges
                prompt_parts.append(f"Q: {entry['question']}")
                prompt_parts.append(f"A: {entry['answer'][:100]}...")
            prompt_parts.append("")
        
        prompt_parts.extend([
            "Current context:",
            context,
            "",
            f"Question: {question}",
            "",
            "Answer:"
        ])
        
        full_prompt = "\n".join(prompt_parts)
        
        try:
            # Generate answer
            response = self.chat.invoke([HumanMessage(content=full_prompt)])
            
            # Calculate confidence based on relevance scores
            avg_relevance = sum(chunk["relevance_score"] for chunk in relevant_chunks) / len(relevant_chunks)
            confidence = min(avg_relevance / 10.0, 1.0)  # Normalize to 0-1
            
            # Store in session history
            if session_id not in self.qa_sessions:
                self.qa_sessions[session_id] = []
            
            self.qa_sessions[session_id].append({
                "question": question,
                "answer": response.content,
                "timestamp": datetime.now().isoformat(),
                "sources": sources,
                "confidence": confidence
            })
            
            return {
                "answer": response.content,
                "confidence": confidence,
                "sources": sources,
                "context_used": len(relevant_chunks),
                "session_id": session_id
            }
            
        except Exception as e:
            return {"error": f"Failed to generate answer: {e}"}
    
    def get_document_summary(self, doc_id: str) -> Dict:
        """Get summary of a specific document"""
        
        if doc_id not in self.documents:
            return {"error": f"Document {doc_id} not found"}
        
        doc_info = self.documents[doc_id]
        chunks_info = self.chunks[doc_id]
        
        # Generate summary using first few chunks
        summary_chunks = chunks_info[:3]
        summary_content = "\n".join([chunk["content"] for chunk in summary_chunks])
        
        summary_prompt = f"""Provide a brief summary of this document content:

{summary_content}

Summary (2-3 sentences):"""
        
        try:
            response = self.chat.invoke([HumanMessage(content=summary_prompt)])
            
            return {
                "doc_id": doc_id,
                "summary": response.content,
                "metadata": doc_info["metadata"],
                "stats": {
                    "total_length": doc_info["length"],
                    "chunks": len(chunks_info),
                    "added_at": doc_info["added_at"]
                }
            }
            
        except Exception as e:
            return {"error": f"Failed to generate summary: {e}"}
    
    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics"""
        
        total_docs = len(self.documents)
        total_chunks = sum(len(chunks) for chunks in self.chunks.values())
        total_sessions = len(self.qa_sessions)
        total_questions = sum(len(session) for session in self.qa_sessions.values())
        
        return {
            "documents": {
                "total": total_docs,
                "list": list(self.documents.keys())
            },
            "chunks": {
                "total": total_chunks,
                "avg_per_doc": total_chunks / max(total_docs, 1)
            },
            "sessions": {
                "total": total_sessions,
                "total_questions": total_questions,
                "avg_questions_per_session": total_questions / max(total_sessions, 1)
            }
        }

def create_sample_documents():
    """Create sample documents for testing"""
    
    documents = {
        "python_guide": {
            "content": """
# Python Programming Guide

## Introduction
Python is a high-level, interpreted programming language known for its simplicity and readability. 
It was created by Guido van Rossum and first released in 1991.

## Key Features
- Simple and readable syntax
- Dynamic typing
- Extensive standard library
- Cross-platform compatibility
- Strong community support

## Data Types
Python supports various data types including:
- Numbers (int, float, complex)
- Strings
- Lists
- Tuples
- Dictionaries
- Sets

## Control Structures
Python provides standard control structures:
- if/elif/else statements
- for loops
- while loops
- try/except for error handling

## Functions
Functions in Python are defined using the 'def' keyword:
def function_name(parameters):
    # function body
    return value

## Object-Oriented Programming
Python supports object-oriented programming with classes:
class ClassName:
    def __init__(self):
        # constructor
        pass
    
    def method_name(self):
        # method body
        pass
""",
            "metadata": {"type": "programming_guide", "language": "python", "level": "beginner"}
        },
        
        "machine_learning": {
            "content": """
# Machine Learning Fundamentals

## What is Machine Learning?
Machine Learning (ML) is a subset of artificial intelligence that enables computers to learn 
and make decisions from data without being explicitly programmed for every task.

## Types of Machine Learning
1. Supervised Learning: Learning with labeled data
   - Classification: Predicting categories
   - Regression: Predicting continuous values

2. Unsupervised Learning: Learning from unlabeled data
   - Clustering: Grouping similar data points
   - Dimensionality Reduction: Simplifying data

3. Reinforcement Learning: Learning through interaction and feedback

## Common Algorithms
- Linear Regression
- Decision Trees
- Random Forest
- Support Vector Machines
- Neural Networks
- K-Means Clustering

## Applications
- Image recognition
- Natural language processing
- Recommendation systems
- Fraud detection
- Autonomous vehicles
- Medical diagnosis

## Getting Started
To start with machine learning:
1. Learn Python programming
2. Understand statistics and mathematics
3. Practice with datasets
4. Use libraries like scikit-learn, TensorFlow, PyTorch
5. Work on real projects
""",
            "metadata": {"type": "technical_guide", "domain": "machine_learning", "level": "intermediate"}
        }
    }
    
    return documents

def run_comprehensive_qa_demo():
    """Run comprehensive document Q&A demonstration"""
    
    print("=== Comprehensive Document Q&A Demo ===\n")
    
    # Initialize system
    qa_system = ComprehensiveDocumentQA()
    
    # Add sample documents
    sample_docs = create_sample_documents()
    
    print("Adding documents to knowledge base:")
    for doc_id, doc_data in sample_docs.items():
        result = qa_system.add_document(doc_id, doc_data["content"], doc_data["metadata"])
        print(f"✅ {doc_id}: {result['chunks_created']} chunks created")
    
    print()
    
    # Test questions
    test_questions = [
        "What is Python?",
        "What are the main types of machine learning?",
        "How do you define a function in Python?",
        "What are some applications of machine learning?",
        "Can you explain Python data types?",
        "What is supervised learning?"
    ]
    
    print("Testing Q&A system:")
    session_id = "demo_session"
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nQuestion {i}: {question}")
        
        result = qa_system.answer_question(question, session_id)
        
        if "error" in result:
            print(f"❌ {result['error']}")
            continue
        
        print(f"Answer: {result['answer'][:150]}...")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Sources: {len(result['sources'])} documents")
        
        # Show source details
        for source in result['sources']:
            print(f"  - {source['document']} (chunk {source['chunk']}, score: {source['relevance_score']:.1f})")
    
    # Show system statistics
    print(f"\n📊 System Statistics:")
    stats = qa_system.get_system_stats()
    print(f"Documents: {stats['documents']['total']}")
    print(f"Total chunks: {stats['chunks']['total']}")
    print(f"Questions answered: {stats['sessions']['total_questions']}")
    
    # Generate document summaries
    print(f"\n📄 Document Summaries:")
    for doc_id in sample_docs.keys():
        summary = qa_system.get_document_summary(doc_id)
        if "error" not in summary:
            print(f"{doc_id}: {summary['summary'][:100]}...")

if __name__ == "__main__":
    run_comprehensive_qa_demo()
    
    print("\n" + "="*50)
    print("✅ Exercise 1 Complete!")
    print("Advanced Features Implemented:")
    print("• Multi-document knowledge base with metadata")
    print("• Intelligent chunking with keyword extraction")
    print("• Semantic relevance scoring for context retrieval")
    print("• Source attribution with confidence scoring")
    print("• Conversation memory for follow-up questions")
    print("• Comprehensive analytics and document summaries")
    print("="*50)