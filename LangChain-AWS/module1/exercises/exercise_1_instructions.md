# Exercise 1: Build Your First LangChain Pipeline

## 🎯 **Objective**
Create a text processing pipeline using LCEL that analyzes text input and returns structured insights.

**Time**: 5 minutes  
**Difficulty**: Beginner  
**File**: `exercise_1_basic_chain.py`

## 📋 **Step-by-Step Instructions**

### Step 1: Setup and Imports (30 seconds)
```python
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
```

### Step 2: Create Prompt Template (30 seconds)
Create a `PromptTemplate` that:
- Uses template variable `{text}` for input
- Asks for text analysis with specific instructions
- Formats the request clearly

**Hint**: Use `PromptTemplate.from_template()` method

### Step 3: Build Analysis Functions (2 minutes)
Create three analysis functions:

**Length Analyzer**:
- Function name: `analyze_length(text)`
- Return: Character count as integer

**Word Analyzer**:
- Function name: `analyze_words(text)`
- Return: Word count using `text.split()`

**Sentiment Analyzer**:
- Function name: `analyze_sentiment(text)`
- Use simple word lists for detection:
  - Positive: ['good', 'great', 'excellent', 'amazing', 'wonderful']
  - Negative: ['bad', 'terrible', 'awful', 'horrible', 'poor']
- Return: "positive", "negative", or "neutral"

### Step 4: Create Parallel Processing (1 minute)
- Use `RunnableParallel` to run all analyzers simultaneously
- Map each function using `RunnableLambda`
- Use descriptive keys: `length`, `words`, `sentiment`

```python
analyzer = RunnableParallel(
    length=RunnableLambda(analyze_length),
    words=RunnableLambda(analyze_words),
    sentiment=RunnableLambda(analyze_sentiment)
)
```

### Step 5: Build Complete Chain (1 minute)
Create the full pipeline:
- Input processing: Convert string to dict with 'text' key
- Chain: `input → prompt → text_extraction → analyzer → formatter`
- Use LCEL pipe operator `|` for composition

**Formatter function**: Create summary string from analysis results

### Step 6: Test Your Pipeline (30 seconds)
Test with these sample texts:
```python
test_texts = [
    "This is a great example of LangChain!",
    "I think this is a terrible implementation.", 
    "LangChain provides powerful tools for developers."
]
```

## ✅ **Expected Output**
```
Test 1: 'This is a great example of LangChain!'
Result: Text has 7 words, 37 characters, sentiment: positive
Details: {'length': 37, 'words': 7, 'sentiment': 'positive'}

Test 2: 'I think this is a terrible implementation.'
Result: Text has 7 words, 39 characters, sentiment: negative
Details: {'length': 39, 'words': 7, 'sentiment': 'negative'}
```

## 🔧 **Common Issues**

**Issue**: Chain doesn't work with pipe operator
**Solution**: Wrap functions with `RunnableLambda`

**Issue**: Text extraction from prompt fails
**Solution**: Create simple extraction function to get original text

**Issue**: Parallel execution returns wrong format
**Solution**: Ensure RunnableParallel keys match expected output

## 🚀 **Challenge Extensions**
1. Add uppercase letter count analysis
2. Include punctuation analysis function
3. Implement error handling for empty inputs
4. Support batch processing of multiple texts
5. Add execution time measurement

## 📋 **Completion Checklist**
- [ ] Prompt template created with `{text}` variable
- [ ] Three analysis functions implemented correctly
- [ ] RunnableParallel configured with proper keys
- [ ] Complete chain works with pipe operator
- [ ] All test cases produce expected output format
- [ ] Results include both summary and detailed analysis

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- LCEL chain composition with pipe operator
- RunnableParallel for concurrent processing
- Prompt template usage and formatting
- Text processing pipeline architecture