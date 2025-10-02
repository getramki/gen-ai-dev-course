# Module 5: Practical Applications (30 minutes)

## Learning Objectives
- Build production-ready document Q&A systems with PDF processing
- Create intelligent code assistants with function calling capabilities
- Implement multi-modal interactions combining text and images
- Develop RAG (Retrieval-Augmented Generation) systems with vector stores

## Prerequisites
- Module 1-4 completed successfully
- Understanding of ChatBedrock and ChatBedrockConverse
- Familiarity with conversation management and system messages
- Basic knowledge of document processing and vector databases

## Module Structure
1. **Topic 5.1**: Building a Document Q&A System (8 min)
2. **Topic 5.2**: Creating a Code Assistant with Function Calling (8 min)
3. **Topic 5.3**: Multi-modal Interactions (Text + Images) (7 min)
4. **Topic 5.4**: RAG Implementation with Vector Stores (7 min)

## Setup Instructions
```bash
# Navigate to module5
cd module5

# Install dependencies (includes document processing and vector stores)
pip install -r requirements.txt

# Verify additional dependencies
python -c "import pypdf; import faiss; print('✅ Document processing ready')"
```

## Files in this Module
- `topic_5_1_document_qa.py` - PDF processing and Q&A pipeline implementation
- `topic_5_2_code_assistant.py` - Function calling and code generation systems
- `topic_5_3_multimodal.py` - Text and image processing with Claude-3
- `topic_5_4_rag_system.py` - Vector stores, embeddings, and retrieval systems
- `exercises/` - Hands-on practice files
- `sample_documents/` - Sample PDFs and images for testing

## Quick Start
Run each topic file to explore practical applications:
```bash
python topic_5_1_document_qa.py
python topic_5_2_code_assistant.py
python topic_5_3_multimodal.py
python topic_5_4_rag_system.py
```

## Key Concepts Covered
- Document loading, chunking, and processing strategies
- Function calling and tool integration patterns
- Multi-modal prompt engineering and image analysis
- Vector embeddings, similarity search, and retrieval
- Production deployment patterns for AI applications

## Expected Outcomes
After completing this module, you will:
- Build document Q&A systems for enterprise knowledge bases
- Create code assistants that generate and execute code
- Implement multi-modal AI applications with image understanding
- Deploy RAG systems with vector databases for enhanced AI responses