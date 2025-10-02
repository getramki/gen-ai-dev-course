"""
Topic 5.4: RAG Implementation with Vector Stores (7 minutes)

Learning Goals:
- Implement Retrieval-Augmented Generation (RAG) systems
- Master vector embeddings and similarity search
- Build production-ready vector stores with FAISS and ChromaDB
- Create intelligent document retrieval and generation pipelines
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import numpy as np
import os
import tempfile
from typing import List, Dict, Optional

def setup_rag_components():
    """Initialize components for RAG system"""
    
    print("=== RAG System Setup ===\n")
    
    components = {}
    
    # Initialize ChatBedrockConverse
    try:
        components['chat'] = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=400,
            temperature=0.3
        )
        print("✅ ChatBedrockConverse initialized")
    except Exception as e:
        print(f"❌ Chat initialization failed: {e}")
        components['chat'] = None
    
    # Initialize Bedrock Embeddings
    try:
        components['embeddings'] = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1",
            region_name="us-east-1"
        )
        print("✅ Bedrock Embeddings initialized")
    except Exception as e:
        print(f"❌ Embeddings initialization failed: {e}")
        components['embeddings'] = None
    
    # Initialize text splitter
    components['text_splitter'] = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    print("✅ Text splitter configured")
    
    print()
    return components

def create_sample_knowledge_base():
    """Create sample documents for RAG system"""
    
    print("=== Creating Knowledge Base ===\n")
    
    documents = {
        "aws_bedrock_overview": """
AWS Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) 
from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Stability AI, and Amazon via a single API, 
along with a broad set of capabilities you need to build generative AI applications with security, privacy, and responsible AI.

Key Features:
- Choice of foundation models from multiple providers
- Serverless experience with no infrastructure to manage
- Fine-tuning capabilities for customization
- Built-in responsible AI features and guardrails
- Integration with AWS services for enterprise applications

Supported Models:
- Anthropic Claude for conversational AI and text generation
- Amazon Titan for embeddings and text generation
- Stability AI for image generation
- Cohere for text analysis and generation
- AI21 Labs Jurassic for text completion
""",
        
        "langchain_integration": """
LangChain provides seamless integration with AWS Bedrock through dedicated components and abstractions.
The integration allows developers to easily switch between different foundation models and build complex AI applications.

Key Components:
- ChatBedrock: Direct integration with Bedrock chat models
- ChatBedrockConverse: Enhanced conversation-focused interface
- BedrockEmbeddings: Vector embeddings using Titan models
- BedrockLLM: General-purpose LLM interface

Benefits:
- Unified API across different model providers
- Easy model switching and comparison
- Built-in streaming and async support
- Integration with LangChain's ecosystem of tools
- Production-ready error handling and retry logic
""",
        
        "rag_best_practices": """
Retrieval-Augmented Generation (RAG) combines the power of large language models with external knowledge retrieval.
This approach enables AI systems to access up-to-date information and domain-specific knowledge.

RAG Architecture:
1. Document Ingestion: Load and process documents into chunks
2. Embedding Generation: Convert text chunks into vector representations
3. Vector Storage: Store embeddings in a searchable vector database
4. Query Processing: Convert user queries into embeddings
5. Similarity Search: Find most relevant document chunks
6. Context Augmentation: Combine retrieved context with user query
7. Generation: Use LLM to generate response based on context

Best Practices:
- Optimize chunk size for your domain (typically 200-800 tokens)
- Use appropriate overlap between chunks (10-20% of chunk size)
- Implement hybrid search combining semantic and keyword matching
- Monitor and evaluate retrieval quality regularly
- Consider re-ranking retrieved results for better relevance
""",
        
        "vector_databases": """
Vector databases are specialized systems designed to store, index, and search high-dimensional vector embeddings efficiently.
They are essential components of modern AI applications, especially for similarity search and retrieval tasks.

Popular Vector Databases:
- FAISS: Facebook's library for efficient similarity search
- ChromaDB: Open-source embedding database
- Pinecone: Managed vector database service
- Weaviate: Open-source vector search engine
- Qdrant: Vector similarity search engine

Key Features:
- High-dimensional vector storage and indexing
- Fast approximate nearest neighbor search
- Scalability for millions or billions of vectors
- Support for metadata filtering and hybrid search
- Integration with machine learning workflows

Selection Criteria:
- Performance requirements and latency needs
- Scalability and data volume expectations
- Integration capabilities with existing systems
- Cost considerations for managed vs self-hosted solutions
- Support for specific distance metrics and search algorithms
"""
    }
    
    print(f"Created knowledge base with {len(documents)} documents")
    for doc_id in documents.keys():
        print(f"  • {doc_id}")
    
    print()
    return documents

def demonstrate_vector_embeddings(components):
    """Demonstrate vector embedding generation and similarity"""
    
    print("=== Vector Embeddings Demo ===\n")
    
    embeddings = components.get('embeddings')
    if not embeddings:
        print("❌ Embeddings not available")
        return
    
    # Sample texts for embedding
    sample_texts = [
        "AWS Bedrock provides access to foundation models",
        "LangChain integrates with multiple AI providers",
        "Vector databases store high-dimensional embeddings",
        "RAG systems combine retrieval with generation"
    ]
    
    try:
        print("Generating embeddings for sample texts:")
        
        # Generate embeddings
        text_embeddings = []
        for i, text in enumerate(sample_texts):
            embedding = embeddings.embed_query(text)
            text_embeddings.append(embedding)
            print(f"  Text {i+1}: {len(embedding)} dimensions")
        
        # Calculate similarity between first two texts
        if len(text_embeddings) >= 2:
            similarity = np.dot(text_embeddings[0], text_embeddings[1])
            print(f"\nSimilarity between text 1 and 2: {similarity:.4f}")
        
        print("✅ Embedding generation successful")
        
    except Exception as e:
        print(f"❌ Embedding generation failed: {e}")
    
    print()

def build_faiss_vector_store(components, documents):
    """Build FAISS vector store from documents"""
    
    print("=== FAISS Vector Store ===\n")
    
    embeddings = components.get('embeddings')
    text_splitter = components.get('text_splitter')
    
    if not embeddings or not text_splitter:
        print("❌ Required components not available")
        return None
    
    try:
        # Prepare documents for vector store
        texts = []
        metadatas = []
        
        for doc_id, content in documents.items():
            # Split document into chunks
            chunks = text_splitter.split_text(content)
            
            for i, chunk in enumerate(chunks):
                texts.append(chunk)
                metadatas.append({
                    "source": doc_id,
                    "chunk_id": i,
                    "chunk_length": len(chunk)
                })
        
        print(f"Preparing {len(texts)} text chunks for vector store")
        
        # Create FAISS vector store
        vector_store = FAISS.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas
        )
        
        print(f"✅ FAISS vector store created with {len(texts)} vectors")
        
        # Test similarity search
        query = "What is AWS Bedrock?"
        results = vector_store.similarity_search(query, k=3)
        
        print(f"\nSimilarity search for: '{query}'")
        for i, result in enumerate(results):
            print(f"  Result {i+1}: {result.page_content[:80]}...")
            print(f"    Source: {result.metadata['source']}")
        
        return vector_store
        
    except Exception as e:
        print(f"❌ FAISS vector store creation failed: {e}")
        return None

def build_chroma_vector_store(components, documents):
    """Build ChromaDB vector store from documents"""
    
    print("=== ChromaDB Vector Store ===\n")
    
    embeddings = components.get('embeddings')
    text_splitter = components.get('text_splitter')
    
    if not embeddings or not text_splitter:
        print("❌ Required components not available")
        return None
    
    try:
        # Prepare documents
        texts = []
        metadatas = []
        ids = []
        
        for doc_id, content in documents.items():
            chunks = text_splitter.split_text(content)
            
            for i, chunk in enumerate(chunks):
                texts.append(chunk)
                metadatas.append({
                    "source": doc_id,
                    "chunk_id": i
                })
                ids.append(f"{doc_id}_{i}")
        
        print(f"Preparing {len(texts)} text chunks for ChromaDB")
        
        # Create temporary directory for ChromaDB
        temp_dir = tempfile.mkdtemp()
        
        # Create ChromaDB vector store
        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas,
            ids=ids,
            persist_directory=temp_dir
        )
        
        print(f"✅ ChromaDB vector store created with {len(texts)} vectors")
        
        # Test similarity search with metadata filtering
        query = "How does LangChain integrate with Bedrock?"
        results = vector_store.similarity_search(
            query, 
            k=2,
            filter={"source": "langchain_integration"}
        )
        
        print(f"\nFiltered search for: '{query}'")
        for i, result in enumerate(results):
            print(f"  Result {i+1}: {result.page_content[:80]}...")
            print(f"    Source: {result.metadata['source']}")
        
        return vector_store
        
    except Exception as e:
        print(f"❌ ChromaDB vector store creation failed: {e}")
        return None

def implement_rag_pipeline(components, vector_store):
    """Implement complete RAG pipeline"""
    
    print("=== RAG Pipeline Implementation ===\n")
    
    chat = components.get('chat')
    if not chat or not vector_store:
        print("❌ Required components not available")
        return None
    
    class RAGSystem:
        """Complete RAG system implementation"""
        
        def __init__(self, chat_model, vector_store):
            self.chat = chat_model
            self.vector_store = vector_store
            
            # RAG prompt template
            self.rag_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a helpful assistant that answers questions based on provided context.
                Use the context information to provide accurate and detailed answers.
                If the context doesn't contain enough information, say so clearly.
                Always cite the sources when possible."""),
                ("human", """Context:
{context}

Question: {question}

Answer:""")
            ])
        
        def retrieve_context(self, query: str, k: int = 3) -> List[Dict]:
            """Retrieve relevant context for query"""
            
            try:
                # Perform similarity search
                results = self.vector_store.similarity_search_with_score(query, k=k)
                
                context_items = []
                for doc, score in results:
                    context_items.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "similarity_score": float(score)
                    })
                
                return context_items
                
            except Exception as e:
                print(f"❌ Context retrieval failed: {e}")
                return []
        
        def generate_answer(self, query: str, max_context_items: int = 3) -> Dict:
            """Generate answer using RAG pipeline"""
            
            # Retrieve relevant context
            context_items = self.retrieve_context(query, k=max_context_items)
            
            if not context_items:
                return {
                    "answer": "I don't have relevant information to answer that question.",
                    "sources": [],
                    "context_used": 0
                }
            
            # Build context string
            context_parts = []
            sources = []
            
            for item in context_items:
                context_parts.append(f"[Source: {item['metadata']['source']}]\n{item['content']}")
                sources.append({
                    "source": item['metadata']['source'],
                    "chunk_id": item['metadata'].get('chunk_id', 0),
                    "similarity_score": item['similarity_score']
                })
            
            context = "\n\n".join(context_parts)
            
            try:
                # Generate answer using RAG prompt
                messages = self.rag_prompt.format_messages(
                    context=context,
                    question=query
                )
                
                response = self.chat.invoke(messages)
                
                return {
                    "answer": response.content,
                    "sources": sources,
                    "context_used": len(context_items),
                    "query": query
                }
                
            except Exception as e:
                return {"error": f"Answer generation failed: {e}"}
    
    # Test RAG system
    rag_system = RAGSystem(chat, vector_store)
    
    test_queries = [
        "What is AWS Bedrock and what models does it support?",
        "How does LangChain integrate with Bedrock?",
        "What are the best practices for RAG systems?",
        "Which vector databases are recommended for AI applications?"
    ]
    
    print("Testing RAG pipeline:")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: {query}")
        
        result = rag_system.generate_answer(query)
        
        if "error" in result:
            print(f"❌ {result['error']}")
            continue
        
        print(f"Answer: {result['answer'][:150]}...")
        print(f"Sources: {len(result['sources'])} documents")
        
        # Show source details
        for source in result['sources']:
            print(f"  • {source['source']} (similarity: {source['similarity_score']:.3f})")
    
    return rag_system

def demonstrate_advanced_rag_features():
    """Demonstrate advanced RAG features and optimizations"""
    
    print("=== Advanced RAG Features ===\n")
    
    advanced_features = {
        "Hybrid Search": {
            "description": "Combine semantic and keyword-based search",
            "implementation": "Use both vector similarity and BM25 scoring",
            "benefits": ["Better recall", "Handles exact matches", "Robust to embedding limitations"]
        },
        "Re-ranking": {
            "description": "Re-order retrieved results for better relevance",
            "implementation": "Use cross-encoder models or LLM-based scoring",
            "benefits": ["Improved precision", "Context-aware ranking", "Better user experience"]
        },
        "Query Expansion": {
            "description": "Expand user queries with related terms",
            "implementation": "Use synonyms, related concepts, or LLM expansion",
            "benefits": ["Better coverage", "Handles vocabulary mismatch", "More comprehensive results"]
        },
        "Contextual Compression": {
            "description": "Compress retrieved context to most relevant parts",
            "implementation": "Use extractive summarization or LLM filtering",
            "benefits": ["Reduced token usage", "Focused context", "Better performance"]
        },
        "Multi-hop Reasoning": {
            "description": "Chain multiple retrieval steps for complex queries",
            "implementation": "Iterative retrieval based on intermediate results",
            "benefits": ["Complex question handling", "Better reasoning", "Comprehensive answers"]
        }
    }
    
    for feature, details in advanced_features.items():
        print(f"🚀 {feature}")
        print(f"   Description: {details['description']}")
        print(f"   Implementation: {details['implementation']}")
        print(f"   Benefits: {', '.join(details['benefits'][:2])}...")
        print()

if __name__ == "__main__":
    print("Module 5.4: RAG Implementation with Vector Stores\n")
    
    # Setup and demonstrations
    components = setup_rag_components()
    documents = create_sample_knowledge_base()
    
    # Demonstrate embeddings
    demonstrate_vector_embeddings(components)
    
    # Build vector stores
    faiss_store = build_faiss_vector_store(components, documents)
    chroma_store = build_chroma_vector_store(components, documents)
    
    # Implement RAG pipeline (use FAISS if available, otherwise ChromaDB)
    vector_store = faiss_store or chroma_store
    if vector_store:
        rag_system = implement_rag_pipeline(components, vector_store)
    
    # Advanced features
    demonstrate_advanced_rag_features()
    
    # Summary
    print("="*50)
    print("✅ Topic 5.4 Complete!")
    print("Key Takeaways:")
    print("• RAG combines retrieval with generation for enhanced AI")
    print("• Vector stores enable efficient similarity search")
    print("• Proper chunking and embedding strategies are crucial")
    print("• Advanced features like re-ranking improve performance")
    print("🚀 Module 5 Complete - Ready for exercises!")
    print("="*50)