# Document Q&A System

A comprehensive document Q&A system that processes PDF and text documents with intelligent chunking, semantic search, source attribution, and conversation memory.

## Features

- **Multi-format Support**: Processes PDF and text files
- **Intelligent Chunking**: Splits documents into meaningful chunks with overlap
- **Semantic Search**: Finds relevant context using keyword and content matching
- **Source Attribution**: Tracks which documents and chunks were used for answers
- **Confidence Scoring**: Provides confidence scores for answers
- **Conversation Memory**: Maintains context across multiple questions
- **Session Management**: Supports multiple conversation sessions

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure AWS credentials are configured for Bedrock access:
```bash
aws configure
```

## Usage

### Basic Usage

```python
from exercise_1_pdf_qa_2 import ComprehensiveDocumentQA

# Initialize the system
qa_system = ComprehensiveDocumentQA()

# Load documents from a folder
folder_path = "/path/to/your/documents"
load_result = qa_system.load_documents_from_folder(folder_path)

# Ask questions
result = qa_system.answer_question("What is artificial intelligence?")
print(result['answer'])
```

### Running the Demo

```bash
python exercise_1_pdf_qa_2.py
```

This will:
1. Load documents from the sample_documents folder
2. Run sample questions
3. Start an interactive Q&A session

### Running Tests

```bash
python test_qa_system.py
```

## System Architecture

### Components

1. **Document Processor**: Loads and processes PDF/text files
2. **Text Splitter**: Intelligently chunks documents with overlap
3. **Keyword Extractor**: Extracts keywords from chunks for better matching
4. **Relevance Scorer**: Calculates relevance between questions and chunks
5. **Context Builder**: Assembles relevant chunks for answering
6. **Answer Generator**: Uses AWS Bedrock to generate answers
7. **Session Manager**: Maintains conversation history

### Workflow

1. **Document Loading**: 
   - Load PDF/text files from specified folder
   - Extract text content
   - Store with metadata

2. **Document Chunking**:
   - Split documents into overlapping chunks
   - Extract keywords from each chunk
   - Store chunk metadata

3. **Question Processing**:
   - Calculate relevance scores for all chunks
   - Select top relevant chunks
   - Build context with source attribution

4. **Answer Generation**:
   - Send context and question to AWS Bedrock
   - Generate answer with source references
   - Calculate confidence score
   - Store in conversation history

## Configuration

### Model Settings

The system uses AWS Bedrock with Claude-3-Haiku by default. You can modify the model in the `_initialize_chat()` method:

```python
return ChatBedrockConverse(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1",
    max_tokens=400,
    temperature=0.2
)
```

### Chunking Parameters

Adjust chunking behavior in the constructor:

```python
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # Size of each chunk
    chunk_overlap=100,     # Overlap between chunks
    separators=["\n\n", "\n", ". ", " ", ""]
)
```

## API Reference

### ComprehensiveDocumentQA

#### Methods

- `add_document(doc_id, content, metadata)`: Add a document to the knowledge base
- `load_documents_from_folder(folder_path)`: Load all documents from a folder
- `answer_question(question, session_id)`: Answer a question with context
- `get_document_summary(doc_id)`: Get summary of a specific document

#### Response Format

```python
{
    "answer": "Generated answer text",
    "confidence": 0.85,
    "sources": [
        {
            "document": "doc_id",
            "chunk": 2,
            "relevance_score": 8.5,
            "metadata": {...}
        }
    ],
    "context_used": 3,
    "session_id": "session_name"
}
```

## Sample Documents

The system includes a sample technology overview document covering:
- Cloud Computing
- Artificial Intelligence & Machine Learning
- DevOps & Containerization
- Cybersecurity
- Data Science & Analytics

## Troubleshooting

### Common Issues

1. **AWS Credentials**: Ensure AWS credentials are properly configured
2. **PyPDF2 Installation**: Install PyPDF2 for PDF processing: `pip install PyPDF2`
3. **Empty Folder**: If no documents are found, the system will load sample content
4. **Low Confidence**: Try rephrasing questions or adding more relevant documents

### Error Messages

- `"PyPDF2 not installed"`: Install PyPDF2 package
- `"Document not found"`: Check document ID exists
- `"Failed to generate answer"`: Check AWS Bedrock access and credentials

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is part of the GenAI for Developers course materials.