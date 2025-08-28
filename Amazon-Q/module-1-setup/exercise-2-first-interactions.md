# Exercise 2: First Interactions with Amazon Q

## Objective
Learn basic Amazon Q interaction patterns and generate your first code.

---

## Part A: Basic Chat Interactions (5 minutes)

### Exercise A1: Introduction Chat
**Task:** Have a basic conversation with Amazon Q

**Steps:**
1. Open Amazon Q chat panel
2. Type each message below and observe responses:

```
Hi Amazon Q! I'm new to using AI coding assistants.
```

```
What programming languages do you work best with?
```

```
Can you help me learn Python?
```

**Expected Learning:**
- Amazon Q responds conversationally
- Understands context and follow-up questions
- Provides helpful information about capabilities

---

## Part B: Simple Code Generation (10 minutes)

### Exercise B1: Hello World Programs
**Task:** Generate hello world programs in different languages

**Steps:**
1. Request Python hello world:
```
Create a hello world program in Python
```

2. Request JavaScript hello world:
```
Now create the same in JavaScript
```

3. Request Java hello world:
```
And one more in Java
```

**Save each result** in separate files:
- `hello.py`
- `hello.js` 
- `Hello.java`

### Exercise B2: Simple Functions
**Task:** Generate basic utility functions

**Request 1 - Calculator Function:**
```
Write a Python function that takes two numbers and returns their sum, difference, product, and quotient
```

**Request 2 - String Utilities:**
```
Create a JavaScript function that reverses a string and counts vowels in it
```

**Request 3 - Array Processing:**
```
Write a Java method that finds the maximum number in an array
```

---

## Part C: Understanding Context (5 minutes)

### Exercise C1: Follow-up Questions
**Task:** Test Amazon Q's ability to maintain conversation context

**Conversation Flow:**
1. Start with:
```
I need to create a simple calculator class in Python
```

2. Follow up with:
```
Add a method for square root calculation
```

3. Then ask:
```
Can you add error handling for division by zero?
```

**Observe:** How Amazon Q builds upon previous responses

### Exercise C2: Code Explanation
**Task:** Ask Amazon Q to explain generated code

**Steps:**
1. Generate this code:
```
Write a Python function that checks if a number is prime
```

2. Then ask:
```
Explain how this prime number function works step by step
```

**Learning Goal:** Understand Amazon Q's explanation capabilities

---

## Part D: File Context Basics

### Exercise D1: Create Sample File
**Task:** Create a file and use it with Amazon Q

**Steps:**
1. Create a new file `sample.py` with this content:
```python
def greet(name):
    return f"Hello, {name}!"

def calculate_area(length, width):
    return length * width
```

2. In Amazon Q chat, type:
```
@sample.py explain what this code does
```

3. Then ask:
```
@sample.py add a function to calculate circle area
```

**Learning Goal:** Understand file context usage with @filename syntax

---

## Verification Checklist

After completing all exercises, verify:

### Basic Interaction
- [ ] Amazon Q responds to conversational messages
- [ ] Can generate code in multiple languages
- [ ] Maintains context in conversations
- [ ] Provides code explanations

### Code Generation Quality
- [ ] Generated code is syntactically correct
- [ ] Code follows language conventions
- [ ] Functions work as expected
- [ ] Error handling suggestions are appropriate

### File Context
- [ ] @filename syntax works correctly
- [ ] Amazon Q can read and understand existing files
- [ ] Can add to existing code appropriately

---

## Sample Solutions

### Hello World Programs

**Python (hello.py):**
```python
print("Hello, World!")
```

**JavaScript (hello.js):**
```javascript
console.log("Hello, World!");
```

**Java (Hello.java):**
```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

### Calculator Function
```python
def calculator(a, b):
    return {
        'sum': a + b,
        'difference': a - b,
        'product': a * b,
        'quotient': a / b if b != 0 else 'Cannot divide by zero'
    }
```

---

## Common Issues and Solutions

### Issue: No Response from Amazon Q
**Solution:** Check connection status, try refreshing or restarting IDE

### Issue: Code Doesn't Work
**Solution:** Copy code exactly as provided, check for syntax errors

### Issue: @filename Not Working
**Solution:** Ensure file is saved and filename is typed correctly

---

## Key Takeaways

After this exercise, you should understand:
- How to communicate effectively with Amazon Q
- Basic code generation capabilities
- Context maintenance in conversations
- File reference using @filename syntax
- Amazon Q's explanation abilities

**Time Required:** 15-20 minutes  
**Difficulty:** Beginner  
**Next:** Ready for Module 2 - Advanced Code Generation