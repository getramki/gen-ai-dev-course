# Exercise 2: AI Coding Assistant

## 🎯 **Objective**
Build an intelligent coding assistant with multi-language support, real-time analysis, safe execution, and comprehensive debugging capabilities.

**Time**: 10 minutes  
**Difficulty**: Advanced  
**File**: `exercise_2_code_helper.py`

## 📋 **Step-by-Step Instructions**

### Step 1: Core Assistant Architecture (2 minutes)
Create `IntelligentCodingAssistant` class:
```python
class IntelligentCodingAssistant:
    def __init__(self):
        self.chat = self._initialize_chat()
        self.supported_languages = {
            "python": {
                "extension": ".py",
                "executor": "python", 
                "validator": self._validate_python_code,
                "analyzer": self._analyze_python_code
            },
            "javascript": {
                "extension": ".js",
                "executor": "node",
                "validator": self._validate_javascript_code,
                "analyzer": self._analyze_javascript_code
            },
            "bash": {
                "extension": ".sh",
                "executor": "bash", 
                "validator": self._validate_bash_code,
                "analyzer": self._analyze_bash_code
            }
        }
```

**Use Claude-3 Sonnet** for better code generation capabilities.

### Step 2: Code Validation System (2 minutes)
Implement language-specific validators:

**Python Validator** (`_validate_python_code`):
- Use `ast.parse()` to check syntax
- Detect dangerous operations: `eval`, `exec`, `subprocess`, `os`, `open`
- Return validation status with specific issues

**JavaScript Validator** (`_validate_javascript_code`):
- Check for dangerous patterns: `eval`, `Function`, `require('fs')`
- Validate basic syntax patterns
- Return safety assessment

**Bash Validator** (`_validate_bash_code`):
- Detect dangerous operations: `rm -rf /`, `dd if=`, `mkfs`
- Check for system-level commands
- Ensure script safety

### Step 3: Code Analysis Engine (2 minutes)
Implement `_analyze_[language]_code()` methods for each language:

**Analysis Categories**:
- **Bugs**: Runtime errors, logic issues, edge cases
- **Performance**: Efficiency improvements, algorithmic optimizations  
- **Security**: Vulnerabilities, input validation issues
- **Maintainability**: Readability, modularity, documentation
- **Best Practices**: Language-specific conventions

**Python Analysis Examples**:
```python
if 'except:' in line_stripped:
    analysis['bugs'].append(f"Line {i}: Bare except clause - specify exception types")

if '==' in line_stripped and 'None' in line_stripped:
    analysis['best_practices'].append(f"Line {i}: Use 'is None' instead of '== None'")
```

### Step 4: Code Generation System (2 minutes)
Implement `generate_code()` method:
- Support multiple code types: function, class, script
- Use structured prompt templates for consistency
- Extract code from response using regex patterns
- Validate and analyze generated code automatically

**Generation Template Example**:
```python
template = """Generate a {language} {code_type} that {description}.

Requirements:
- Include proper error handling
- Add comprehensive docstrings/comments
- Follow {language} best practices
- Include usage examples

Format as:
```{language}
# Your code here
```"""
```

### Step 5: Safe Code Execution (2 minutes)
Implement `execute_code()` method:
1. Validate code before execution using language validator
2. Create temporary file with appropriate extension
3. Execute using subprocess with timeout (10 seconds)
4. Capture stdout, stderr, and return code
5. Clean up temporary files
6. Return structured execution results

**Safety Features**:
- Pre-execution validation
- Timeout protection
- Sandboxed execution environment
- Comprehensive error handling

### Step 6: Advanced Features (2 minutes)
Implement additional capabilities:

**`debug_code()`**: 
- Analyze problematic code with error messages
- Generate corrected code with explanations
- Test corrected code automatically

**`optimize_code()`**:
- Optimize for performance, readability, security, or memory
- Provide before/after comparison
- Explain optimization strategies

**`get_coding_suggestions()`**:
- Analyze partial code
- Provide completion suggestions
- Recommend best practices

## ✅ **Expected Output**
```
=== Intelligent Coding Assistant Demo ===

1. Code Generation Test:
✅ Code generated successfully
Code preview: def factorial(n):
    """Calculate factorial of a number with error handling."""
    if not isinstance(n, int):...
✅ Valid

2. Code Execution Test:
✅ Code executed successfully
Output: factorial(5) = 120

3. Debugging Test:
✅ Debugging assistance provided
✅ Corrected code generated
✅ Corrected code executes successfully

4. Code Optimization Test:
✅ Code optimization completed
✅ Optimized version generated

5. Multi-language Support Test:
✅ JavaScript code generated
✅ Valid
```

## 🔧 **Common Issues**

**Issue**: Code extraction from LLM response fails
**Solution**: Use robust regex patterns and handle multiple code block formats

**Issue**: Code execution security concerns
**Solution**: Implement comprehensive validation and use subprocess isolation

**Issue**: Language-specific analysis inaccurate
**Solution**: Refine analysis patterns and add more language-specific rules

**Issue**: Timeout issues with complex code
**Solution**: Adjust timeout values and implement proper cleanup

## 🚀 **Challenge Extensions**
1. **Advanced Static Analysis**: Integrate with tools like pylint, eslint
2. **Code Formatting**: Add automatic code formatting capabilities
3. **Test Generation**: Generate unit tests for created functions
4. **Documentation Generation**: Create comprehensive API documentation
5. **Code Refactoring**: Implement intelligent code refactoring suggestions

### Advanced Static Analysis Extension:
```python
def run_static_analysis(self, code: str, language: str) -> Dict[str, Any]:
    if language == "python":
        # Run pylint or flake8
        result = subprocess.run(['pylint', '--output-format=json', temp_file], 
                              capture_output=True, text=True)
        return json.loads(result.stdout)
    elif language == "javascript":
        # Run eslint
        result = subprocess.run(['eslint', '--format=json', temp_file],
                              capture_output=True, text=True)
        return json.loads(result.stdout)
```

### Test Generation Extension:
```python
def generate_tests(self, code: str, language: str = "python") -> Dict[str, Any]:
    prompt = f"""Generate comprehensive unit tests for this {language} code:

{code}

Include:
- Test cases for normal operation
- Edge cases and error conditions
- Mock objects where needed
- Assertions for expected behavior"""
    
    # Generate and return test code
```

## 📋 **Completion Checklist**
- [ ] IntelligentCodingAssistant class with multi-language support
- [ ] Code validation system for Python, JavaScript, and Bash
- [ ] Comprehensive code analysis engine with 5 categories
- [ ] Code generation with structured templates
- [ ] Safe code execution with timeout and validation
- [ ] Debugging assistance with corrected code generation
- [ ] Code optimization for multiple criteria
- [ ] Multi-language demo runs successfully
- [ ] All safety checks prevent dangerous code execution
- [ ] Error handling prevents system crashes

## 🎓 **Learning Outcomes**
After completing this exercise, you will understand:
- Multi-language AI code generation techniques
- Safe code execution and validation strategies
- Comprehensive code analysis and quality assessment
- Intelligent debugging and optimization approaches
- Production-ready coding assistant architecture
- Security considerations for AI-powered code tools