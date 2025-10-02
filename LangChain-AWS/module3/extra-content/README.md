# Module 3: ChatBedrock Fundamentals (25 minutes)

## Learning Objectives
- Master ChatBedrock initialization and configuration
- Implement effective chat completion patterns
- Optimize streaming responses and token management
- Fine-tune model parameters for different use cases

## Prerequisites
- Module 1 (LangChain Fundamentals) completed
- Module 2 (Setup and Environment) completed
- AWS Bedrock access configured and tested
- Claude models accessible

## Module Structure
1. **Topic 3.1**: Introduction to ChatBedrock (6 min)
2. **Topic 3.2**: Basic Chat Completion with Claude (6 min)
3. **Topic 3.3**: Streaming Responses and Token Management (6 min)
4. **Topic 3.4**: Model Parameters and Configuration (7 min)

## Setup Instructions
```bash
# Navigate to module3
cd module3

# Install dependencies
pip install -r requirements.txt

# Verify AWS configuration
python -c "import boto3; print(boto3.client('bedrock', region_name='us-east-1').list_foundation_models())"
```

## Files in this Module
- `topic_3_1_introduction.py` - ChatBedrock basics and initialization
- `topic_3_2_chat_completion.py` - Message handling and response processing
- `topic_3_3_streaming.py` - Real-time responses and token management
- `topic_3_4_parameters.py` - Model parameter tuning and optimization
- `exercises/` - Hands-on practice files

## Quick Start
Run each topic file to explore ChatBedrock features:
```bash
python topic_3_1_introduction.py
python topic_3_2_chat_completion.py
python topic_3_3_streaming.py
python topic_3_4_parameters.py
```

## Key Concepts Covered
- ChatBedrock vs direct Bedrock API
- Message types and formatting
- Streaming implementation patterns
- Parameter optimization strategies
- Error handling and best practices

## Expected Outcomes
After completing this module, you will:
- Build production-ready chatbots with Claude
- Implement efficient streaming interfaces
- Optimize model parameters for specific use cases
- Handle errors and edge cases effectively