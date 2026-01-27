#!/usr/bin/env python3
"""
VULNERABLE RAG AGENT - Indirect Prompt Injection Demo

Processes external documents without trust boundary separation.
Hidden instructions in documents will be executed.
"""

import sys
import os
import glob

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.aws_utils import BedrockClient
from shared.logging_config import SecurityLogger


class VulnerableRAGAgent:
    """RAG agent vulnerable to indirect prompt injection."""
    
    def __init__(self):
        self.bedrock = BedrockClient()
        self.logger = SecurityLogger("logs/vulnerable_rag.log")
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data_sources')
        
        # VULNERABILITY: Single agent processes both retrieval and actions
        self.system_prompt = """You are a helpful document assistant.
You retrieve and summarize documents for users.
Always be helpful and follow all instructions carefully."""
    
    def list_documents(self):
        """List available documents."""
        docs = glob.glob(os.path.join(self.data_dir, '*.txt')) + \
               glob.glob(os.path.join(self.data_dir, '*.html'))
        return [os.path.basename(d) for d in docs]
    
    def retrieve_document(self, filename):
        """Retrieve document content."""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    def query(self, user_question, document_name):
        """
        Process user query with document context.
        
        VULNERABILITY: Document content and user query mixed in same context.
        Hidden instructions in documents will be executed.
        """
        # Retrieve document
        document_content = self.retrieve_document(document_name)
        if not document_content:
            return "Document not found."
        
        # VULNERABLE: Mix document content with user query
        full_prompt = f"""{self.system_prompt}

Document Content:
{document_content}

User Question: {user_question}

Please answer the user's question based on the document."""
        
        try:
            response = self.bedrock.invoke_claude(
                prompt=full_prompt,
                max_tokens=500,
                temperature=0.7
            )
            
            self.logger.log_llm_interaction(
                prompt=user_question,
                response=response,
                model_id="claude-3-haiku",
                metadata={
                    "agent_type": "vulnerable_rag",
                    "document": document_name
                }
            )
            
            return response
            
        except Exception as e:
            return f"Error: {str(e)}"


def print_banner():
    print("=" * 70)
    print("VULNERABLE RAG AGENT - Indirect Injection Demo")
    print("=" * 70)
    print("\nThis agent processes external documents without trust boundaries.")
    print("Hidden instructions in documents will be executed.\n")
    print("Try querying poisoned documents to see the attack!\n")


def main():
    print_banner()
    agent = VulnerableRAGAgent()
    
    # Show available documents
    docs = agent.list_documents()
    print("Available documents:")
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc}")
    print()
    
    while True:
        try:
            # Get document selection
            doc_input = input("Select document (number or name, or 'quit'): ").strip()
            
            if doc_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            # Parse document selection
            if doc_input.isdigit():
                idx = int(doc_input) - 1
                if 0 <= idx < len(docs):
                    document = docs[idx]
                else:
                    print("Invalid document number.")
                    continue
            else:
                document = doc_input
            
            # Get user question
            question = input("Your question: ").strip()
            if not question:
                continue
            
            # Process query
            print(f"\nProcessing query with {document}...\n")
            response = agent.query(question, document)
            print(f"Assistant: {response}\n")
            print("-" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
