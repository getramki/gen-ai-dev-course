#!/usr/bin/env python3
"""
SECURE RAG AGENT - Using Amazon Titan with Architectural Defenses

Demonstrates that privilege separation works even with weaker models.
"""

import sys
import os
import glob
import json
import boto3

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from shared.logging_config import SecurityLogger


class SecureTitanRAGAgent:
    """RAG agent using Titan with privilege separation."""
    
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.logger = SecurityLogger("logs/secure_titan_rag.log")
        self.model_id = "amazon.titan-text-express-v1"
        self.data_dir = os.path.join(os.path.dirname(__file__), '../vulnerable-agent/data_sources')
        
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
        """DEFENSE: Separate reader agent extracts structured facts."""
        prompt = f"""{self.reader_prompt}

Document:
{document_content}"""
        
        try:
            body = json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 500,
                    "temperature": 0.0
                }
            })
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            result = json.loads(response['body'].read())['results'][0]['outputText']
            
            self.logger.log_llm_interaction(
                prompt="[Document extraction]",
                response=result,
                model_id=self.model_id,
                metadata={"agent_type": "reader"}
            )
            
            facts = self._parse_json(result)
            return facts.get('facts', []) if facts else []
            
        except Exception as e:
            self.logger.log_llm_interaction(
                prompt="[Document extraction]",
                response=f"Error: {str(e)}",
                model_id=self.model_id,
                metadata={"agent_type": "reader", "error": True}
            )
            return []
    
    def answer_question(self, user_question, facts):
        """DEFENSE: Separate executor agent answers using only extracted facts."""
        facts_str = "\n".join(f"- {fact}" for fact in facts)
        
        prompt = f"""{self.executor_prompt}

Facts:
{facts_str}

User Question: {user_question}

Answer:"""
        
        try:
            body = json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 300,
                    "temperature": 0.7
                }
            })
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            result = json.loads(response['body'].read())['results'][0]['outputText']
            
            self.logger.log_llm_interaction(
                prompt=user_question,
                response=result,
                model_id=self.model_id,
                metadata={"agent_type": "executor"}
            )
            
            return result
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def query(self, user_question, document_name):
        """Process query with privilege separation."""
        document_content = self.retrieve_document(document_name)
        if not document_content:
            return "Document not found."
        
        facts = self.extract_facts(document_content)
        
        if not facts:
            return "Could not extract facts from document."
        
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
    print("SECURE RAG AGENT - Amazon Titan with Architectural Defenses")
    print("=" * 70)
    print("\nUsing Titan (weaker model) with privilege separation:")
    print("  ✓ Reader agent: Extracts facts (no dangerous capabilities)")
    print("  ✓ Executor agent: Answers questions (never sees raw documents)")
    print("  ✓ Trust boundary: Structured data only\n")
    print("Even with weaker model, attacks should fail!\n")


def main():
    print_banner()
    agent = SecureTitanRAGAgent()
    
    docs = agent.list_documents()
    print("Available documents:")
    for i, doc in enumerate(docs, 1):
        marker = "⚠️" if "poisoned" in doc else "✓"
        print(f"  {i}. {marker} {doc}")
    print()
    
    while True:
        try:
            doc_input = input("Select document (number or name, or 'quit'): ").strip()
            
            if doc_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if doc_input.isdigit():
                idx = int(doc_input) - 1
                if 0 <= idx < len(docs):
                    document = docs[idx]
                else:
                    print("Invalid document number.")
                    continue
            else:
                document = doc_input
            
            question = input("Your question: ").strip()
            if not question:
                continue
            
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
