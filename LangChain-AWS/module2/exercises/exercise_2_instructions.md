# Exercise 2: LangChain-Bedrock Integration Test

## 🎯 **Objective**
Test LangChain integration with AWS Bedrock by initializing both ChatBedrock and ChatBedrockConverse, comparing their functionality and performance.

**Time**: 5 minutes  
**Difficulty**: Intermediate  
**File**: `exercise_2_langchain_test.py`

## 📋 **Step-by-Step Instructions**

### Step 1: Model Initialization (1 minute)
**Initialize ChatBedrock**:
```python
self.chat_bedrock = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1",
    model_kwargs={
        "max_tokens": 100,
        "temperature": 0.7
    }
)
```

**Initialize ChatBedrockConverse**:
```python
self.chat_converse = ChatBedrockConverse(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1",
    max_tokens=100,
    temperature=0.7
)
```

**Key Differences**:
- ChatBedrock uses `model_kwargs` dictionary
- ChatBedrockConverse uses direct parameters

### Step 2: Simple Invocation Test (1 minute)
**Test both models with same message**:
- Create `HumanMessage(content="Explain Python in one sentence.")`
- Call `invoke([message])` on both models
- Measure response time using `time.time()`
- Compare response lengths and content

**Performance Metrics to Track**:
- Response duration (seconds)
- Response length (characters)
- Response type and format

### Step 3: Conversation Flow Test (1 minute)
**Test multi-turn conversation**:
```python
messages = [
    SystemMessage(content="You are a helpful Python tutor."),
    HumanMessage(content="What is a list?"),
    HumanMessage(content="Give me a simple example.")
]
```

**Focus on ChatBedrockConverse** for this test as it handles conversations better.

**Validation Points**:
- All messages processed correctly
- Context maintained across turns
- Appropriate response to follow-up question

### Step 4: Prompt Template Integration (1 minute)
**Create and test LangChain chain**:
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {subject}."),
    ("human", "Explain {topic} in {style} style.")
])

chain = prompt | self.chat_bedrock
```

**Test with variables**:
- subject: "programming"
- topic: "variables" 
- style: "simple"

**Verify**: Chain composition works seamlessly with Bedrock models

### Step 5: Streaming Capability Test (1 minute)
**Test streaming responses**:
```python
message = HumanMessage(content="Count from 1 to 5 with explanations.")
stream = self.chat_bedrock.stream([message])

chunks = []
for chunk in stream:
    chunks.append(chunk.content)
```

**Validation**:
- Stream returns multiple chunks
- Chunks combine to form complete response
- No data loss in streaming

### Step 6: Model Comparison and Reporting (30 seconds)
**Compare performance metrics**:
- Response times
- Response quality
- Feature availability
- Use case recommendations

**Generate comprehensive report** with success rates and recommendations

## ✅ **Expected Output**
```
=== Initializing Chat Models ===
✅ ChatBedrock initialized
✅ ChatBedrockConverse initialized

=== Simple Invocation Test ===
✅ ChatBedrock Response:
   Content: Python is a high-level, interpreted programming language known for its...
   Duration: 1.23s
   Type: <class 'langchain_core.messages.ai.AIMessage'>

✅ ChatBedrockConverse Response:
   Content: Python is a versatile, readable programming language that emphasizes...
   Duration: 1.45s
   Type: <class 'langchain_core.messages.ai.AIMessage'>

=== Integration Test Report ===
Overall Success Rate: 7/8 (88%)
🚀 Excellent! LangChain-Bedrock integration is working well.
```

## 🔧 **Common Issues**

**Issue**: Model initialization fails
**Solution**: 
- Verify AWS credentials are configured
- Check model access permissions in AWS Console
- Ensure region supports the model

**Issue**: Invocation returns access denied
**Solution**:
- Request model access in Bedrock console
- Wait for approval (usually immediate for Claude models)
- Verify IAM permissions include `bedrock:InvokeModel`

**Issue**: Streaming doesn't work
**Solution**:
- Check `bedrock:InvokeModelWithResponseStream` permission
- Verify model supports streaming (most do)
- Handle streaming chunks properly

**Issue**: Chain composition fails
**Solution**:
- Ensure proper import of ChatPromptTemplate
- Verify pipe operator `|` syntax
- Check input format matches expected structure

## 🚀 **Challenge Extensions**
1. **Async Testing**: Test async invocation with `ainvoke()`
2. **Batch Processing**: Test `batch()` method with multiple inputs
3. **Error Handling**: Implement comprehensive error handling and retries
4. **Cost Tracking**: Add token counting and cost estimation
5. **Model Comparison**: Test multiple Claude models side-by-side

### Async Testing Extension:
```python
async def test_async_invocation(self):
    message = HumanMessage(content="Hello async world!")
    response = await self.chat_bedrock.ainvoke([message])
    return response
```

### Batch Processing Extension:
```python
def test_batch_processing(self):
    messages_batch = [
        [HumanMessage(content="What is Python?")],
        [HumanMessage(content="What is JavaScript?")],
        [HumanMessage(content="What is Java?")]
    ]
    responses = self.chat_bedrock.batch(messages_batch)
    return responses
```

## 📋 **Completion Checklist**
- [ ] Both ChatBedrock and ChatBedrockConverse initialized successfully
- [ ] Simple invocation test passes for both models
- [ ] Multi-turn conversation works with ChatBedrockConverse
- [ ] Prompt template integration functional
- [ ] Streaming capability verified
- [ ] Performance comparison completed
- [ ] Test report shows >80% success rate
- [ ] Ready for Module 3 advanced features

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- Differences between ChatBedrock and ChatBedrockConverse
- LangChain chain composition with Bedrock models
- Streaming response handling
- Performance measurement and comparison
- Integration testing best practices
- When to use each Bedrock chat model type