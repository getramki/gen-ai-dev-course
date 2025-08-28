# Exercise 1: Document Q&A System

## 🎯 **Objective**
Build a comprehensive document Q&A system with intelligent chunking, semantic search, source attribution, and conversation memory.

**Time**: 10 minutes  
**Difficulty**: Advanced  
**File**: `exercise_1_pdf_qa.py`

## 📋 **Step-by-Step Instructions**

### Step 1: Core System Architecture (2 minutes)
Create `ComprehensiveDocumentQA` class:
```python
class ComprehensiveDocumentQA:
    def __init__(self):
        self.chat = self._initialize_chat()
        self.documents = {}  # Store full documents with metadata
        self.chunks = {}     # Store processed chunks with keywords
        self.conversation_history = []
        self.qa_sessions = {}  # Track conversation sessions
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
```

### Step 2: Document Processing System (2 minutes)
Implement `add_document()` method:
- Store document with metadata (type, domain, level, etc.)
- Split text into chunks using RecursiveCharacterTextSplitter
- Extract keywords from each chunk for better retrieval
- Create chunk metadata with IDs, length, and keywords

**Keyword Extraction**:
```python
def _extract_keywords(self, text: str) -> List[str]:
    words = text.lower().split()
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    keywords = []
    for word in words:
        clean_word = ''.join(c for c in word if c.isalnum())
        if len(clean_word) > 3 and clean_word not in stop_words:
            keywords.append(clean_word)
    
    return list(set(keywords))
```

### Step 3: Intelligent Relevance Scoring (2 minutes)
Implement `_calculate_relevance_score()` method:
- **Keyword Overlap**: Match question words with chunk keywords (weight: 2x)
- **Content Overlap**: Match question words with all chunk words (weight: 1x)
- **Length Penalty**: Prefer chunks that aren't too short (<100 chars) or too long (>800 chars)

**Scoring Formula**:
```python
total_score = (keyword_overlap * 2 + content_overlap) * length_penalty
```

### Step 4: Context Retrieval System (2 minutes)
Implement `_find_relevant_chunks()` method:
- Calculate relevance scores for all chunks across all documents
- Sort chunks by relevance score (highest first)
- Return top N chunks (default: 3) with scores above threshold
- Include source attribution (document ID, chunk ID, relevance score)

### Step 5: Advanced Q&A with Memory (2 minutes)
Implement `answer_question()` method:
1. Find relevant chunks using scoring system
2. Build context from top chunks with source attribution
3. Include conversation history from session (last 3 exchanges)
4. Generate answer using ChatBedrockConverse
5. Calculate confidence score based on average relevance
6. Store Q&A in session history for follow-up questions

**Confidence Calculation**:
```python
avg_relevance = sum(chunk["relevance_score"] for chunk in relevant_chunks) / len(relevant_chunks)
confidence = min(avg_relevance / 10.0, 1.0)  # Normalize to 0-1
```

## ✅ **Expected Output**
```
=== Comprehensive Document Q&A Demo ===

Adding documents to knowledge base:
✅ python_guide: 12 chunks created
✅ machine_learning: 15 chunks created

Testing Q&A system:

Question 1: What is Python?
Answer: Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991...
Confidence: 0.85
Sources: 2 documents
  - python_guide (chunk 0, score: 8.5)
  - python_guide (chunk 1, score: 6.2)

Question 4: What are some applications of machine learning?
Answer: Machine learning has numerous applications including image recognition, natural language processing, recommendation systems, fraud detection...
Confidence: 0.92
Sources: 1 documents
  - machine_learning (chunk 8, score: 9.2)

📊 System Statistics:
Documents: 2
Total chunks: 27
Questions answered: 6

📄 Document Summaries:
python_guide: This document is a comprehensive Python programming guide covering the basics of the language...
machine_learning: This document explains machine learning fundamentals, including types of ML and common algorithms...
```

## 🔧 **Common Issues**

**Issue**: Poor relevance scoring accuracy
**Solution**: Refine keyword extraction and adjust scoring weights based on testing

**Issue**: Chunks too large or too small
**Solution**: Adjust RecursiveCharacterTextSplitter parameters (chunk_size, chunk_overlap)

**Issue**: Missing conversation context
**Solution**: Ensure session management properly stores and retrieves conversation history

**Issue**: Low confidence scores
**Solution**: Calibrate confidence calculation based on actual relevance score distributions

## 🚀 **Challenge Extensions**
1. **Vector Embeddings**: Replace keyword matching with semantic embeddings
2. **Multi-format Support**: Add support for DOCX, HTML, and other document formats
3. **Advanced Summarization**: Use LLM-based summarization for document overviews
4. **Query Expansion**: Expand user queries with synonyms and related terms
5. **Feedback Learning**: Incorporate user feedback to improve relevance scoring

### Vector Embeddings Extension:
```python
from langchain_community.embeddings import BedrockEmbeddings

def _initialize_embeddings(self):
    return BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v1",
        region_name="us-east-1"
    )

def _calculate_semantic_similarity(self, question_embedding, chunk_embedding):
    # Calculate cosine similarity between embeddings
    return cosine_similarity(question_embedding, chunk_embedding)
```

### Multi-format Support Extension:
```python
def add_document_from_file(self, file_path: str, doc_id: str = None):
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    
    documents = loader.load()
    content = "\n".join([doc.page_content for doc in documents])
    
    return self.add_document(doc_id or file_path, content)
```

## 📋 **Completion Checklist**
- [ ] ComprehensiveDocumentQA class with all core methods
- [ ] Document processing with intelligent chunking
- [ ] Keyword extraction working for all chunks
- [ ] Relevance scoring system implemented and calibrated
- [ ] Context retrieval finding appropriate chunks
- [ ] Q&A system with conversation memory
- [ ] Source attribution with confidence scoring
- [ ] Session management for follow-up questions
- [ ] System statistics and document summaries
- [ ] Demo runs successfully with multiple documents and questions

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- Advanced document processing and chunking strategies
- Intelligent relevance scoring for information retrieval
- Source attribution and confidence measurement
- Conversation memory management for Q&A systems
- Production-ready document Q&A system architecture
- Performance monitoring and system analytics for AI applications