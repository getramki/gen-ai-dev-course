"""
Exercise 2: AI Coding Assistant

Task: Build an intelligent coding assistant that:
1. Generates code with multiple programming languages support
2. Provides real-time code analysis and suggestions
3. Implements safe code execution with comprehensive testing
4. Includes debugging assistance and code optimization

Time: 10 minutes
"""

from langchain_aws.chat_models import ChatBedrockConverse
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import subprocess
import tempfile
import os
import json
import ast
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

class IntelligentCodingAssistant:
    """Advanced AI coding assistant with multi-language support"""
    
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
        
        # Code generation templates
        self.generation_templates = {
            "function": """Generate a {language} function that {description}.

Requirements:
- Include proper error handling
- Add comprehensive docstrings/comments
- Follow {language} best practices and conventions
- Include type hints where applicable
- Provide a simple usage example

Format your response as:
```{language}
# Your code here
```""",
            
            "class": """Create a {language} class that {description}.

Requirements:
- Include constructor and essential methods
- Add proper documentation
- Implement error handling
- Follow OOP best practices
- Include usage examples

Format your response as:
```{language}
# Your code here
```""",
            
            "script": """Write a complete {language} script that {description}.

Requirements:
- Include main execution logic
- Add command-line argument handling if needed
- Implement proper error handling and logging
- Follow best practices for script structure
- Include usage instructions

Format your response as:
```{language}
# Your code here
```"""
        }
        
        # Analysis criteria
        self.analysis_criteria = {
            "bugs": "Potential runtime errors, logic issues, edge cases",
            "performance": "Efficiency improvements, algorithmic optimizations",
            "security": "Security vulnerabilities, input validation issues",
            "maintainability": "Code readability, modularity, documentation",
            "best_practices": "Language-specific conventions and patterns"
        }
    
    def _initialize_chat(self):
        """Initialize ChatBedrockConverse for coding assistance"""
        return ChatBedrockConverse(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # Use Sonnet for better code generation
            region_name="us-east-1",
            max_tokens=800,
            temperature=0.2  # Lower temperature for more consistent code
        )
    
    def _validate_python_code(self, code: str) -> Dict[str, Any]:
        """Validate Python code syntax and safety"""
        issues = []
        
        try:
            # Parse AST to check syntax
            ast.parse(code)
        except SyntaxError as e:
            issues.append(f"Syntax error: {e}")
        
        # Check for dangerous operations
        dangerous_patterns = [
            r'import\s+subprocess',
            r'import\s+os',
            r'eval\s*\(',
            r'exec\s*\(',
            r'__import__',
            r'open\s*\(',
            r'file\s*\('
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                issues.append(f"Potentially unsafe operation: {pattern}")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "language": "python"
        }
    
    def _validate_javascript_code(self, code: str) -> Dict[str, Any]:
        """Validate JavaScript code"""
        issues = []
        
        # Basic JavaScript validation (simplified)
        dangerous_patterns = [
            r'eval\s*\(',
            r'Function\s*\(',
            r'require\s*\(\s*[\'"]fs[\'"]',
            r'require\s*\(\s*[\'"]child_process[\'"]'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                issues.append(f"Potentially unsafe operation: {pattern}")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "language": "javascript"
        }
    
    def _validate_bash_code(self, code: str) -> Dict[str, Any]:
        """Validate Bash code"""
        issues = []
        
        # Check for dangerous bash operations
        dangerous_patterns = [
            r'rm\s+-rf\s+/',
            r'dd\s+if=',
            r'mkfs\.',
            r'fdisk',
            r'>\s*/dev/sd'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                issues.append(f"Potentially dangerous operation: {pattern}")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "language": "bash"
        }
    
    def _analyze_python_code(self, code: str) -> Dict[str, List[str]]:
        """Analyze Python code for improvements"""
        analysis = {category: [] for category in self.analysis_criteria.keys()}
        
        # Simple static analysis
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Check for common issues
            if 'except:' in line_stripped:
                analysis['bugs'].append(f"Line {i}: Bare except clause - specify exception types")
            
            if 'print(' in line_stripped and 'def ' in code:
                analysis['maintainability'].append(f"Line {i}: Consider using logging instead of print")
            
            if len(line) > 100:
                analysis['maintainability'].append(f"Line {i}: Line too long (>100 characters)")
            
            if '==' in line_stripped and 'None' in line_stripped:
                analysis['best_practices'].append(f"Line {i}: Use 'is None' instead of '== None'")
        
        # Check for missing docstrings
        if 'def ' in code and '"""' not in code and "'''" not in code:
            analysis['maintainability'].append("Missing docstrings for functions")
        
        return analysis
    
    def _analyze_javascript_code(self, code: str) -> Dict[str, List[str]]:
        """Analyze JavaScript code for improvements"""
        analysis = {category: [] for category in self.analysis_criteria.keys()}
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            if 'var ' in line_stripped:
                analysis['best_practices'].append(f"Line {i}: Use 'let' or 'const' instead of 'var'")
            
            if '==' in line_stripped and '===' not in line_stripped:
                analysis['best_practices'].append(f"Line {i}: Use '===' for strict equality")
            
            if 'console.log(' in line_stripped:
                analysis['maintainability'].append(f"Line {i}: Remove console.log in production code")
        
        return analysis
    
    def _analyze_bash_code(self, code: str) -> Dict[str, List[str]]:
        """Analyze Bash code for improvements"""
        analysis = {category: [] for category in self.analysis_criteria.keys()}
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            if line_stripped.startswith('#!') and i > 1:
                analysis['best_practices'].append(f"Line {i}: Shebang should be on first line")
            
            if '$(' not in line_stripped and '`' in line_stripped:
                analysis['best_practices'].append(f"Line {i}: Use $() instead of backticks")
            
            if '[' in line_stripped and '[[' not in line_stripped:
                analysis['best_practices'].append(f"Line {i}: Consider using [[ ]] for better test syntax")
        
        return analysis
    
    def generate_code(self, description: str, language: str = "python", 
                     code_type: str = "function") -> Dict[str, Any]:
        """Generate code based on description and requirements"""
        
        if language not in self.supported_languages:
            return {"error": f"Unsupported language: {language}"}
        
        if code_type not in self.generation_templates:
            return {"error": f"Unsupported code type: {code_type}"}
        
        # Format prompt
        prompt = self.generation_templates[code_type].format(
            language=language,
            description=description
        )
        
        try:
            response = self.chat.invoke([HumanMessage(content=prompt)])
            
            # Extract code from response
            code_start = response.content.find(f"```{language}")
            if code_start == -1:
                code_start = response.content.find("```")
            
            if code_start != -1:
                code_end = response.content.find("```", code_start + 3)
                if code_end != -1:
                    # Extract code block
                    if f"```{language}" in response.content[code_start:code_start+10]:
                        code = response.content[code_start + len(f"```{language}"):code_end].strip()
                    else:
                        code = response.content[code_start + 3:code_end].strip()
                    
                    # Validate generated code
                    validation = self.supported_languages[language]["validator"](code)
                    
                    # Analyze code quality
                    analysis = self.supported_languages[language]["analyzer"](code)
                    
                    return {
                        "success": True,
                        "code": code,
                        "language": language,
                        "code_type": code_type,
                        "validation": validation,
                        "analysis": analysis,
                        "full_response": response.content
                    }
            
            return {
                "success": False,
                "error": "Could not extract code from response",
                "full_response": response.content
            }
            
        except Exception as e:
            return {"error": f"Code generation failed: {e}"}
    
    def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Safely execute code with timeout and validation"""
        
        if language not in self.supported_languages:
            return {"error": f"Execution not supported for language: {language}"}
        
        lang_config = self.supported_languages[language]
        
        # Validate code before execution
        validation = lang_config["validator"](code)
        if not validation["is_valid"]:
            return {
                "success": False,
                "error": f"Code validation failed: {validation['issues']}"
            }
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(
                mode='w', 
                suffix=lang_config["extension"], 
                delete=False
            ) as f:
                f.write(code)
                temp_file = f.name
            
            # Execute code with timeout
            result = subprocess.run(
                [lang_config["executor"], temp_file],
                capture_output=True,
                text=True,
                timeout=10  # 10 second timeout
            )
            
            # Clean up
            os.unlink(temp_file)
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "return_code": result.returncode,
                "language": language
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Code execution timed out (10 seconds)",
                "language": language
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error: {e}",
                "language": language
            }
    
    def debug_code(self, code: str, error_message: str = None, 
                   language: str = "python") -> Dict[str, Any]:
        """Provide debugging assistance for problematic code"""
        
        debug_prompt = f"""Help debug this {language} code:

Code:
```{language}
{code}
```

{f"Error message: {error_message}" if error_message else ""}

Please provide:
1. Explanation of the issue(s)
2. Corrected code with fixes
3. Explanation of what was changed and why
4. Additional recommendations for improvement

Format corrected code as:
```{language}
# Corrected code here
```"""
        
        try:
            response = self.chat.invoke([HumanMessage(content=debug_prompt)])
            
            # Extract corrected code if available
            corrected_code = None
            code_start = response.content.find(f"```{language}")
            if code_start != -1:
                code_end = response.content.find("```", code_start + len(f"```{language}"))
                if code_end != -1:
                    corrected_code = response.content[code_start + len(f"```{language}"):code_end].strip()
            
            result = {
                "success": True,
                "explanation": response.content,
                "corrected_code": corrected_code,
                "language": language
            }
            
            # Test corrected code if available
            if corrected_code and language in self.supported_languages:
                test_result = self.execute_code(corrected_code, language)
                result["test_result"] = test_result
            
            return result
            
        except Exception as e:
            return {"error": f"Debugging assistance failed: {e}"}
    
    def optimize_code(self, code: str, language: str = "python", 
                     optimization_focus: str = "performance") -> Dict[str, Any]:
        """Optimize code for performance, readability, or other criteria"""
        
        optimization_prompts = {
            "performance": f"Optimize this {language} code for better performance and efficiency",
            "readability": f"Improve the readability and maintainability of this {language} code",
            "security": f"Enhance the security of this {language} code",
            "memory": f"Optimize this {language} code for better memory usage"
        }
        
        if optimization_focus not in optimization_prompts:
            return {"error": f"Unsupported optimization focus: {optimization_focus}"}
        
        prompt = f"""{optimization_prompts[optimization_focus]}:

Original Code:
```{language}
{code}
```

Please provide:
1. Analysis of current code issues related to {optimization_focus}
2. Optimized version of the code
3. Explanation of optimizations made
4. Performance/improvement expectations

Format optimized code as:
```{language}
# Optimized code here
```"""
        
        try:
            response = self.chat.invoke([HumanMessage(content=prompt)])
            
            # Extract optimized code
            optimized_code = None
            code_start = response.content.find(f"```{language}")
            if code_start != -1:
                code_end = response.content.find("```", code_start + len(f"```{language}"))
                if code_end != -1:
                    optimized_code = response.content[code_start + len(f"```{language}"):code_end].strip()
            
            return {
                "success": True,
                "original_code": code,
                "optimized_code": optimized_code,
                "optimization_focus": optimization_focus,
                "explanation": response.content,
                "language": language
            }
            
        except Exception as e:
            return {"error": f"Code optimization failed: {e}"}
    
    def get_coding_suggestions(self, partial_code: str, language: str = "python") -> Dict[str, Any]:
        """Provide coding suggestions and completions"""
        
        suggestion_prompt = f"""Analyze this partial {language} code and provide suggestions:

Partial Code:
```{language}
{partial_code}
```

Please provide:
1. Possible completions for the code
2. Suggestions for improvement
3. Best practices recommendations
4. Potential issues to avoid

Format any code suggestions as:
```{language}
# Suggested code here
```"""
        
        try:
            response = self.chat.invoke([HumanMessage(content=suggestion_prompt)])
            
            return {
                "success": True,
                "suggestions": response.content,
                "language": language,
                "partial_code": partial_code
            }
            
        except Exception as e:
            return {"error": f"Suggestion generation failed: {e}"}

def run_coding_assistant_demo():
    """Run comprehensive coding assistant demonstration"""
    
    print("=== Intelligent Coding Assistant Demo ===\n")
    
    assistant = IntelligentCodingAssistant()
    
    # Test code generation
    print("1. Code Generation Test:")
    generation_result = assistant.generate_code(
        "calculate the factorial of a number with error handling",
        language="python",
        code_type="function"
    )
    
    if generation_result.get("success"):
        print("✅ Code generated successfully")
        print(f"Code preview: {generation_result['code'][:100]}...")
        print(f"Validation: {'✅ Valid' if generation_result['validation']['is_valid'] else '❌ Issues found'}")
        
        # Test execution
        print("\n2. Code Execution Test:")
        exec_result = assistant.execute_code(generation_result['code'], "python")
        
        if exec_result.get("success"):
            print("✅ Code executed successfully")
            if exec_result.get("output"):
                print(f"Output: {exec_result['output'][:100]}...")
        else:
            print(f"❌ Execution failed: {exec_result.get('error')}")
    else:
        print(f"❌ Code generation failed: {generation_result.get('error')}")
    
    # Test debugging
    print("\n3. Debugging Test:")
    buggy_code = """
def divide_numbers(a, b):
    return a / b

result = divide_numbers(10, 0)
print(result)
"""
    
    debug_result = assistant.debug_code(
        buggy_code, 
        "ZeroDivisionError: division by zero",
        "python"
    )
    
    if debug_result.get("success"):
        print("✅ Debugging assistance provided")
        if debug_result.get("corrected_code"):
            print("✅ Corrected code generated")
            
            # Test corrected code
            if debug_result.get("test_result", {}).get("success"):
                print("✅ Corrected code executes successfully")
    else:
        print(f"❌ Debugging failed: {debug_result.get('error')}")
    
    # Test optimization
    print("\n4. Code Optimization Test:")
    optimization_result = assistant.optimize_code(
        """
def find_max(numbers):
    max_num = numbers[0]
    for i in range(len(numbers)):
        if numbers[i] > max_num:
            max_num = numbers[i]
    return max_num
""",
        language="python",
        optimization_focus="performance"
    )
    
    if optimization_result.get("success"):
        print("✅ Code optimization completed")
        if optimization_result.get("optimized_code"):
            print("✅ Optimized version generated")
    else:
        print(f"❌ Optimization failed: {optimization_result.get('error')}")
    
    # Test multi-language support
    print("\n5. Multi-language Support Test:")
    js_result = assistant.generate_code(
        "create a function to validate email addresses",
        language="javascript",
        code_type="function"
    )
    
    if js_result.get("success"):
        print("✅ JavaScript code generated")
        print(f"Validation: {'✅ Valid' if js_result['validation']['is_valid'] else '❌ Issues found'}")
    else:
        print(f"❌ JavaScript generation failed: {js_result.get('error')}")

if __name__ == "__main__":
    run_coding_assistant_demo()
    
    print("\n" + "="*50)
    print("✅ Exercise 2 Complete!")
    print("Advanced Features Implemented:")
    print("• Multi-language code generation (Python, JavaScript, Bash)")
    print("• Comprehensive code validation and safety checks")
    print("• Real-time code analysis with quality metrics")
    print("• Intelligent debugging assistance with corrections")
    print("• Code optimization for performance and readability")
    print("• Safe code execution with timeout protection")
    print("="*50)