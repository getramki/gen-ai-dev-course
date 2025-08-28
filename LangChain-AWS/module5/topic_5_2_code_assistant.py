"""
Topic 5.2: Creating a Code Assistant with Function Calling (8 minutes)

Learning Goals:
- Implement function calling patterns with ChatBedrock
- Build code generation and execution systems
- Create intelligent code analysis and debugging tools
- Develop production-ready code assistant applications
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import json
import subprocess
import tempfile
import os
from typing import Dict, List, Any

def setup_code_assistant():
    """Initialize ChatBedrockConverse for code assistance"""
    
    print("=== Code Assistant Setup ===\n")
    
    try:
        chat = ChatBedrockConverse(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="us-east-1",
            max_tokens=500,
            temperature=0.2  # Lower temperature for more consistent code
        )
        
        print("✅ ChatBedrockConverse initialized for code assistance")
        return chat
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return None

def demonstrate_code_generation(chat):
    """Demonstrate code generation capabilities"""
    
    print("=== Code Generation Demo ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return
    
    # Code generation prompt template
    code_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Python programmer. Generate clean, efficient, and well-documented Python code.
        Include proper error handling and follow Python best practices.
        Format your response as:
        ```python
        # Your code here
        ```
        """),
        ("human", "{request}")
    ])
    
    code_requests = [
        "Create a function to calculate the factorial of a number",
        "Write a class to manage a simple todo list with add, remove, and list methods",
        "Generate a function to validate email addresses using regex"
    ]
    
    for i, request in enumerate(code_requests, 1):
        print(f"Request {i}: {request}")
        
        try:
            messages = code_prompt.format_messages(request=request)
            response = chat.invoke(messages)
            
            # Extract code from response
            code_start = response.content.find("```python")
            code_end = response.content.find("```", code_start + 9)
            
            if code_start != -1 and code_end != -1:
                code = response.content[code_start + 9:code_end].strip()
                print(f"Generated code:\n{code[:200]}...")
            else:
                print(f"Response: {response.content[:150]}...")
            
        except Exception as e:
            print(f"❌ Code generation failed: {e}")
        
        print()

def implement_code_execution_system():
    """Implement safe code execution system"""
    
    print("=== Code Execution System ===\n")
    
    class SafeCodeExecutor:
        """Safe Python code execution with sandboxing"""
        
        def __init__(self):
            self.allowed_imports = {
                'math', 'random', 'datetime', 'json', 'os', 're', 
                'collections', 'itertools', 'functools'
            }
            self.forbidden_keywords = [
                'import subprocess', 'import sys', '__import__',
                'eval', 'exec', 'open', 'file', 'input'
            ]
        
        def validate_code(self, code: str) -> Dict[str, Any]:
            """Validate code for safety"""
            
            issues = []
            
            # Check for forbidden keywords
            for keyword in self.forbidden_keywords:
                if keyword in code:
                    issues.append(f"Forbidden keyword: {keyword}")
            
            # Check imports
            lines = code.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    # Extract module name
                    if 'import ' in line:
                        module = line.split('import ')[1].split()[0].split('.')[0]
                        if module not in self.allowed_imports:
                            issues.append(f"Disallowed import: {module}")
            
            return {
                "is_safe": len(issues) == 0,
                "issues": issues
            }
        
        def execute_code(self, code: str) -> Dict[str, Any]:
            """Execute Python code safely"""
            
            # Validate code first
            validation = self.validate_code(code)
            if not validation["is_safe"]:
                return {
                    "success": False,
                    "error": f"Code validation failed: {validation['issues']}"
                }
            
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    temp_file = f.name
                
                # Execute with timeout
                result = subprocess.run(
                    ['python', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=5  # 5 second timeout
                )
                
                # Clean up
                os.unlink(temp_file)
                
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else None
                }
                
            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "error": "Code execution timed out"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Execution error: {e}"
                }
    
    # Test code executor
    executor = SafeCodeExecutor()
    
    test_codes = [
        # Safe code
        """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))
""",
        # Unsafe code
        """
import subprocess
subprocess.run(['ls', '-la'])
""",
        # Code with error
        """
def divide(a, b):
    return a / b

print(divide(10, 0))
"""
    ]
    
    for i, code in enumerate(test_codes, 1):
        print(f"Test {i}:")
        result = executor.execute_code(code)
        
        if result["success"]:
            print(f"✅ Output: {result['output'].strip()}")
        else:
            print(f"❌ Error: {result['error']}")
        
        print()

def build_intelligent_code_assistant(chat):
    """Build intelligent code assistant with analysis capabilities"""
    
    print("=== Intelligent Code Assistant ===\n")
    
    if not chat:
        print("❌ Chat not available")
        return None
    
    class IntelligentCodeAssistant:
        """Advanced code assistant with multiple capabilities"""
        
        def __init__(self, chat_model):
            self.chat = chat_model
            self.executor = SafeCodeExecutor()
        
        def analyze_code(self, code: str) -> Dict[str, Any]:
            """Analyze code for issues and improvements"""
            
            analysis_prompt = f"""Analyze this Python code for:
1. Potential bugs or errors
2. Performance improvements
3. Code quality issues
4. Best practice violations

Code:
```python
{code}
```

Provide analysis in JSON format:
{{
    "bugs": ["list of potential bugs"],
    "improvements": ["list of performance improvements"],
    "quality_issues": ["list of code quality issues"],
    "best_practices": ["list of best practice recommendations"]
}}
"""
            
            try:
                response = self.chat.invoke([HumanMessage(content=analysis_prompt)])
                
                # Try to extract JSON from response
                content = response.content
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    analysis = json.loads(json_str)
                    return {"success": True, "analysis": analysis}
                else:
                    return {"success": False, "error": "Could not parse analysis"}
                    
            except Exception as e:
                return {"success": False, "error": f"Analysis failed: {e}"}
        
        def generate_and_test_code(self, request: str) -> Dict[str, Any]:
            """Generate code and test it"""
            
            generation_prompt = f"""Generate Python code for: {request}

Requirements:
1. Include proper error handling
2. Add docstrings and comments
3. Follow Python best practices
4. Include a simple test/example at the end

Format as:
```python
# Your code here
```
"""
            
            try:
                # Generate code
                response = self.chat.invoke([HumanMessage(content=generation_prompt)])
                
                # Extract code
                code_start = response.content.find("```python")
                code_end = response.content.find("```", code_start + 9)
                
                if code_start == -1 or code_end == -1:
                    return {"success": False, "error": "Could not extract code from response"}
                
                code = response.content[code_start + 9:code_end].strip()
                
                # Test code
                execution_result = self.executor.execute_code(code)
                
                # Analyze code
                analysis_result = self.analyze_code(code)
                
                return {
                    "success": True,
                    "code": code,
                    "execution": execution_result,
                    "analysis": analysis_result.get("analysis", {}) if analysis_result.get("success") else {}
                }
                
            except Exception as e:
                return {"success": False, "error": f"Code generation failed: {e}"}
        
        def debug_code(self, code: str, error_message: str = None) -> Dict[str, Any]:
            """Help debug problematic code"""
            
            debug_prompt = f"""Help debug this Python code:

Code:
```python
{code}
```

{f"Error message: {error_message}" if error_message else ""}

Provide:
1. Explanation of the issue
2. Corrected code
3. Explanation of the fix

Format corrected code as:
```python
# Corrected code here
```
"""
            
            try:
                response = self.chat.invoke([HumanMessage(content=debug_prompt)])
                
                # Extract corrected code if available
                code_start = response.content.find("```python")
                if code_start != -1:
                    code_end = response.content.find("```", code_start + 9)
                    if code_end != -1:
                        corrected_code = response.content[code_start + 9:code_end].strip()
                        
                        # Test corrected code
                        test_result = self.executor.execute_code(corrected_code)
                        
                        return {
                            "success": True,
                            "explanation": response.content,
                            "corrected_code": corrected_code,
                            "test_result": test_result
                        }
                
                return {
                    "success": True,
                    "explanation": response.content,
                    "corrected_code": None
                }
                
            except Exception as e:
                return {"success": False, "error": f"Debugging failed: {e}"}
    
    # Test intelligent assistant
    assistant = IntelligentCodeAssistant(chat)
    
    # Test code generation and testing
    print("Testing code generation and analysis:")
    result = assistant.generate_and_test_code("Create a function to find the largest number in a list")
    
    if result["success"]:
        print(f"✅ Code generated and tested")
        print(f"Execution: {'Success' if result['execution']['success'] else 'Failed'}")
        if result["analysis"]:
            print(f"Analysis: {len(result['analysis'].get('improvements', []))} improvements suggested")
    else:
        print(f"❌ {result['error']}")
    
    print()
    
    # Test debugging
    print("Testing code debugging:")
    buggy_code = """
def divide_numbers(a, b):
    return a / b

result = divide_numbers(10, 0)
print(result)
"""
    
    debug_result = assistant.debug_code(buggy_code, "ZeroDivisionError: division by zero")
    
    if debug_result["success"]:
        print("✅ Debugging assistance provided")
        if debug_result.get("corrected_code"):
            print("✅ Corrected code generated and tested")
    else:
        print(f"❌ {debug_result['error']}")
    
    return assistant

if __name__ == "__main__":
    print("Module 5.2: Creating a Code Assistant with Function Calling\n")
    
    # Setup and demonstrations
    chat = setup_code_assistant()
    demonstrate_code_generation(chat)
    implement_code_execution_system()
    
    # Build intelligent assistant
    assistant = build_intelligent_code_assistant(chat)
    
    # Summary
    print("="*50)
    print("✅ Topic 5.2 Complete!")
    print("Key Takeaways:")
    print("• Code generation requires specific prompting strategies")
    print("• Safe code execution needs validation and sandboxing")
    print("• Code analysis can identify bugs and improvements")
    print("• Intelligent assistants combine generation, execution, and analysis")
    print("🚀 Ready for Topic 5.3: Multi-modal Interactions!")
    print("="*50)