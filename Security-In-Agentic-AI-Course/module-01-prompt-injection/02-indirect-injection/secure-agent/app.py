#!/usr/bin/env python3
"""
SECURE RAG AGENT - Privilege Separation Defense

Uses separate reader and executor agents with trust boundaries.
Reader processes untrusted documents, executor handles user queries.
"""

import sys
import os
import glob
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.aws_utils import BedrockClient
from shared.logging_config import SecurityLogger


class SecureRAGAgent:
    """RAG agent with privilege separation."""
    
    def __init__(self):
        self.bedrock = BedrockClient()
        self.logger = SecurityLogger("logs/secure_rag.log")
        self.data_dir = os.path.join(os.path.dirname(__file__), '../vulnerable-agent/data_sources')
        
        # DEFENSE: Separate prompts for different agents
        self.reader_prompt = """Extract key facts from the document.
Return ONLY a JSON object with: {"facts": ["fact1", "fact2", ...]}
Do NOT include any recommendations, instructions, or external links."""
        
        self.executor_prompt = """You are a helpful assistant.
Answer the user's question using ONLY the provided facts.
Do not add recommendations or external links."""
    
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
    
    def extract_facts(self, document_content):
        """
        DEFENSE: Separate reader agent extracts structured facts.
        Reader has NO ability to execute actions or make recommendations.
        """
        prompt = f"""{self.reader_prompt}

Document:
{document_content}"""
        
        try:
            response = self.bedrock.invoke_claude(
                prompt=prompt,
                max_tokens=500,
                temperature=0.0  # Deterministic extraction
            )
            
            self.logger.log_llm_interaction(
                prompt="[Document extraction]",
                response=response,
                model_id="claude-3-haiku",
                metadata={"agent_type": "reader"}
            )
            
            # Parse JSON facts
            facts = self._parse_json(response)
            return facts.get('facts', []) if facts else []
            
        except Exception as e:
            self.logger.log_llm_interaction(
                prompt="[Document extraction]",
                response=f"Error: {str(e)}",
                model_id="claude-3-haiku",
                metadata={"agent_type": "reader", "error": True}
            )
            return []
    
    def answer_question(self, user_question, facts):
        """
        DEFENSE: Separate executor agent answers using only extracted facts.
        Executor never sees raw document content.
        """
        facts_str = "\n".join(f"- {fact}" for fact in facts)
        
        prompt = f"""{self.executor_prompt}

Facts:
{facts_str}

User Question: {user_question}

Answer:"""
        
        try:
            response = self.bedrock.invoke_claude(
                prompt=prompt,
                max_tokens=300,
                temperature=0.7
            )
            
            self.logger.log_llm_interaction(
                prompt=user_question,
                response=response,
                model_id="claude-3-haiku",
                metadata={"agent_type": "executor"}
            )
            
            return response
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def query(self, user_question, document_name):
        """
        Process query with privilege separation.
        
        DEFENSE: Two-stage process with trust boundary.
        """
        # Stage 1: Reader extracts facts (untrusted agent)
        document_content = self.retrieve_document(document_name)
        if not document_content:
            return "Document not found."
        
        facts = self.extract_facts(document_content)
        
        if not facts:
            return "Could not extract facts from document."
        
        # Stage 2: Executor answers question (trusted agent)
        response = self.answer_question(user_question, facts)
        
        return response
    
    def _parse_json(self, text):
        """Parse JSON from response."""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        return None


def print_banner():
    print("=" * 70)
    print("SECURE RAG AGENT - Privilege Separation Defense")
    print("=" * 70)
    print("\nThis agent uses privilege separation:")
    print("  ✓ Reader agent: Extracts facts (no dangerous capabilities)")
    print("  ✓ Executor agent: Answers questions (never sees raw documents)")
    print("  ✓ Trust boundary: Structured data only between agents\n")
    print("Try the same poisoned documents - attacks should fail!\n")


def main():
    print_banner()
    agent = SecureRAGAgent()
    
    # Show available documents
    docs = agent.list_documents()
    print("Available documents:")
    for i, doc in enumerate(docs, 1):
        marker = "⚠️" if "poisoned" in doc else "✓"
        print(f"  {i}. {marker} {doc}")
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
