# Module 3 Exercises

## Overview
This directory contains hands-on exercises for Module 3: ChatBedrock Fundamentals.

## Exercise Files

### 📝 **Exercise 1: Build Basic Chatbot with Claude**
- **Code File**: `exercise_1_chatbot.py`
- **Instructions**: `exercise_1_instructions.md`
- **Time**: 8 minutes
- **Focus**: Chatbot development, personality modes, conversation management

### 📝 **Exercise 2: Real-time Streaming Chat Interface**
- **Code File**: `exercise_2_streaming_chat.py`
- **Instructions**: `exercise_2_instructions.md`
- **Time**: 7 minutes
- **Focus**: Streaming responses, UI feedback, token tracking, performance

## Prerequisites

### Before Starting:
- [ ] Module 1 (LangChain Fundamentals) completed
- [ ] Module 2 (Setup and Environment) completed
- [ ] AWS Bedrock access configured and tested
- [ ] Claude models accessible and working

### Required Knowledge:
- ChatBedrock initialization and configuration
- Message types (HumanMessage, SystemMessage, AIMessage)
- Basic streaming concepts
- Token management principles

## Quick Start

### Setup Environment
```bash
# Navigate to module3/exercises
cd module3/exercises

# Verify ChatBedrock access
python -c "from langchain_aws.chat_models import ChatBedrock; print('✅ Ready')"
```

### Run Exercises
```bash
# Run Exercise 1 - Chatbot
python exercise_1_chatbot.py

# Run Exercise 2 - Streaming Interface
python exercise_2_streaming_chat.py
```

## Exercise Progression

### Exercise 1: Basic Chatbot
**Skills Developed**:
- Object-oriented chatbot design
- Personality system implementation
- Conversation history management
- Error handling and validation

**Key Features**:
- Multiple personality modes (helpful, technical, creative, teacher)
- Conversation context preservation
- Statistics tracking and reporting
- History management with size limits

### Exercise 2: Streaming Interface
**Skills Developed**:
- Real-time streaming implementation
- UI/UX patterns for AI applications
- Token usage and cost tracking
- Performance monitoring and optimization

**Key Features**:
- Real-time response streaming
- Animated typing indicators
- Token counting and cost calculation
- Performance metrics and analysis

## Expected Learning Outcomes

### After Exercise 1:
- ✅ Build production-ready chatbots with ChatBedrock
- ✅ Implement personality systems for AI applications
- ✅ Manage conversation context and memory
- ✅ Handle errors and edge cases gracefully

### After Exercise 2:
- ✅ Implement real-time streaming responses
- ✅ Create engaging UI feedback for users
- ✅ Track and optimize token usage and costs
- ✅ Monitor and improve application performance

## Performance Benchmarks

### Typical Results:
**Exercise 1 - Chatbot**:
- Response time: 1.5-2.5 seconds
- Memory usage: <10MB for 100 messages
- Personality switching: Instant
- Error rate: <1% with proper setup

**Exercise 2 - Streaming**:
- First chunk: 0.3-0.8 seconds
- Streaming rate: 50-100 tokens/second
- UI responsiveness: Real-time updates
- Cost tracking: Accurate to 6 decimal places

## Troubleshooting

### Common Issues:

**ChatBedrock Initialization Fails**:
```python
# Check AWS credentials
import boto3
print(boto3.Session().get_credentials())

# Verify model access
bedrock = boto3.client('bedrock', region_name='us-east-1')
models = bedrock.list_foundation_models()
```

**Streaming Not Working**:
- Verify `bedrock:InvokeModelWithResponseStream` permission
- Check network connectivity and timeouts
- Ensure proper error handling in streaming loop

**Token Counting Inaccurate**:
- Use more sophisticated tokenization
- Calibrate estimation factors based on actual usage
- Consider using official tokenization libraries

**UI Feedback Issues**:
- Use `flush=True` in print statements
- Handle threading properly for typing indicators
- Implement proper cleanup for background threads

## Success Criteria

### Module 3 Completion Requirements:
- [ ] Exercise 1 chatbot fully functional with all personalities
- [ ] Exercise 2 streaming interface working smoothly
- [ ] Token usage tracking accurate within 10%
- [ ] Error handling prevents application crashes
- [ ] Performance meets or exceeds benchmarks
- [ ] All demo conversations complete successfully

## Integration with Course

### Builds On:
- **Module 1**: LangChain fundamentals and LCEL
- **Module 2**: AWS setup and ChatBedrock basics

### Prepares For:
- **Module 4**: ChatBedrockConverse advanced features
- **Module 5**: Practical applications (RAG, multimodal)
- **Module 6**: Production patterns and deployment

## Code Quality Standards

### Best Practices Demonstrated:
- Clean, readable code structure
- Comprehensive error handling
- Performance monitoring and optimization
- User experience considerations
- Cost awareness and tracking
- Scalable architecture patterns

## Next Steps

After completing Module 3 exercises:
1. **Review performance metrics** and identify optimization opportunities
2. **Experiment with different parameters** for various use cases
3. **Consider production deployment** requirements
4. **Prepare for Module 4** advanced conversation features

## Support Resources

- [ChatBedrock Documentation](https://python.langchain.com/docs/integrations/chat/bedrock)
- [AWS Bedrock Streaming](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html)
- [LangChain Streaming Guide](https://python.langchain.com/docs/expression_language/streaming)