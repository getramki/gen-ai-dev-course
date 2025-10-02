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
        return {
            "doc_id": doc_id,
            "length": doc_info["length"],
            "chunks": len(self.chunks.get(doc_id, [])),
            "metadata": doc_info["metadata"],
            "added_at": doc_info["added_at"]
        }
    
    def load_documents_from_folder(self, folder_path: str) -> Dict:
        """Load all PDF and text files from a folder"""
        results = {}
        
        # Get all supported files
        all_files = os.listdir(folder_path)
        pdf_files = [f for f in all_files if f.endswith('.pdf')]
        txt_files = [f for f in all_files if f.endswith(('.txt', '.md'))]
        
        # Load PDF files
        if pdf_files:
            try:
                import PyPDF2
                for pdf_file in pdf_files:
                    pdf_path = os.path.join(folder_path, pdf_file)
                    try:
                        with open(pdf_path, 'rb') as file:
                            pdf_reader = PyPDF2.PdfReader(file)
                            text_content = ""
                            
                            for page in pdf_reader.pages:
                                text_content += page.extract_text() + "\n"
                            
                            doc_id = pdf_file.replace('.pdf', '')
                            result = self.add_document(
                                doc_id=doc_id,
                                content=text_content,
                                metadata={"source": pdf_file, "type": "pdf", "pages": len(pdf_reader.pages)}
                            )
                            results[doc_id] = result
                            
                    except Exception as e:
                        results[pdf_file] = {"error": str(e)}
            except ImportError:
                results["pdf_error"] = "PyPDF2 not installed. Run: pip install PyPDF2"
        
        # Load text files
        for txt_file in txt_files:
            txt_path = os.path.join(folder_path, txt_file)
            try:
                with open(txt_path, 'r', encoding='utf-8') as file:
                    text_content = file.read()
                    
                    doc_id = txt_file.replace('.txt', '').replace('.md', '')
                    result = self.add_document(
                        doc_id=doc_id,
                        content=text_content,
                        metadata={"source": txt_file, "type": "text"}
                    )
                    results[doc_id] = result
                    
            except Exception as e:
                results[txt_file] = {"error": str(e)}
        
        # If no files found, create sample content
        if not results:
            sample_content = """Artificial Intelligence and Machine Learning

Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines that can perform tasks that typically require human intelligence. These tasks include learning, reasoning, problem-solving, perception, and language understanding.

Machine Learning (ML) is a subset of AI that focuses on the development of algorithms and statistical models that enable computers to improve their performance on a specific task through experience, without being explicitly programmed.

Key concepts in Machine Learning:
1. Supervised Learning: Learning with labeled training data
2. Unsupervised Learning: Finding patterns in data without labels
3. Reinforcement Learning: Learning through interaction with an environment
4. Deep Learning: Using neural networks with multiple layers

Applications of AI and ML:
- Natural Language Processing
- Computer Vision
- Recommendation Systems
- Autonomous Vehicles
- Medical Diagnosis
- Financial Trading

The future of AI holds great promise for solving complex problems and improving human life across various domains."""
            
            doc_id = "sample_ai_ml_document"
            result = self.add_document(
                doc_id=doc_id,
                content=sample_content,
                metadata={"source": "sample", "topic": "AI/ML", "type": "educational"}
            )
            results[doc_id] = result
            return {"loaded_documents": results, "note": "No documents found, loaded sample document"}
        
        return {"loaded_documents": results}

def main():
    """Demonstrate the comprehensive document Q&A system"""
    
    print("🚀 Initializing Comprehensive Document Q&A System...")
    qa_system = ComprehensiveDocumentQA()
    
    # Load documents from the sample folder
    print("\n📁 Loading documents from sample_documents folder...")
    sample_folder = "/home/ramakrishna/Code/GenAI-for-Dev-Course/LangChain-AWS/module5/sample_documents"
    
    load_result = qa_system.load_documents_from_folder(sample_folder)
    print(f"✅ Load result: {json.dumps(load_result, indent=2)}")
    
    # Display loaded documents
    print(f"\n📚 Loaded {len(qa_system.documents)} documents:")
    for doc_id in qa_system.documents:
        summary = qa_system.get_document_summary(doc_id)
        print(f"  - {doc_id}: {summary['chunks']} chunks, {summary['length']} chars")
    
    # Sample questions for demonstration
    sample_questions = [
        "What is artificial intelligence?",
        "What are the key concepts in machine learning?",
        "What are some applications of AI?",
        "Tell me about deep learning"
    ]
    
    print("\n🤖 Demonstrating with sample questions:")
    session_id = "demo_session"
    
    for question in sample_questions:
        print(f"\n❓ Question: {question}")
        
        result = qa_system.answer_question(question, session_id)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"💡 Answer: {result['answer']}")
            print(f"🎯 Confidence: {result['confidence']:.2f}")
            print(f"📖 Sources used: {result['context_used']}")
    
    print("\n👋 Demo completed!")

if __name__ == "__main__":
    main()