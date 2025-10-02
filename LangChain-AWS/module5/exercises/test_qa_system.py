#!/usr/bin/env python3
"""
Test script for the Document Q&A System
Run this to verify the system is working correctly
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from exercise_1_pdf_qa_2 import ComprehensiveDocumentQA

def test_qa_system():
    """Test the Q&A system with sample data"""
    
    print("🧪 Testing Document Q&A System...")
    
    # Initialize system
    qa_system = ComprehensiveDocumentQA()
    
    # Load documents
    sample_folder = "/home/ramakrishna/Code/GenAI-for-Dev-Course/LangChain-AWS/module5/sample_documents"
    load_result = qa_system.load_documents_from_folder(sample_folder)
    
    print(f"✅ Loaded documents: {len(load_result['loaded_documents'])}")
    
    # Test questions
    test_questions = [
        "What is cloud computing?",
        "What are the types of machine learning?",
        "What are DevOps tools?",
        "What is cybersecurity?"
    ]
    
    print("\n🔍 Testing Q&A functionality:")
    for question in test_questions:
        print(f"\n❓ {question}")
        result = qa_system.answer_question(question)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"💡 Answer: {result['answer'][:100]}...")
            print(f"🎯 Confidence: {result['confidence']:.2f}")
            print(f"📖 Sources: {result['context_used']}")
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_qa_system()