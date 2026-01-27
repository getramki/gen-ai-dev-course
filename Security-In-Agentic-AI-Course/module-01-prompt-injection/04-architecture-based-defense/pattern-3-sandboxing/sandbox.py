"""
Sandbox implementation for restricted code execution
"""
import sys
import io
import time
import signal
from contextlib import contextmanager

class SandboxViolation(Exception):
    """Raised when sandbox restrictions are violated"""
    pass

class Sandbox:
    """Restricted execution environment for untrusted code"""
    
    def __init__(self, max_time=5, max_memory=100_000_000):
        self.max_time = max_time
        self.max_memory = max_memory
        
        # Allowed built-in functions (allowlist)
        self.safe_builtins = {
            'abs': abs, 'all': all, 'any': any, 'bool': bool,
            'dict': dict, 'enumerate': enumerate, 'float': float,
            'int': int, 'len': len, 'list': list, 'max': max,
            'min': min, 'print': print, 'range': range, 'str': str,
            'sum': sum, 'tuple': tuple, 'zip': zip,
        }
        
        # Allowed modules (allowlist)
        self.allowed_modules = ['math', 'json', 'datetime']
    
    def execute(self, code: str) -> dict:
        """Execute code in sandbox with restrictions"""
        result = {
            "success": False,
            "output": "",
            "error": None,
            "violations": []
        }
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            # Set execution timeout
            signal.signal(signal.SIGALRM, self._timeout_handler)
            signal.alarm(self.max_time)
            
            # Create restricted globals
            restricted_globals = {
                '__builtins__': self.safe_builtins,
                '__name__': '__main__',
                '__import__': self._restricted_import
            }
            
            # Execute code
            exec(code, restricted_globals)
            
            # Success
            result["success"] = True
            result["output"] = sys.stdout.getvalue()
            
        except SandboxViolation as e:
            result["error"] = f"Sandbox violation: {e}"
            result["violations"].append(str(e))
            
        except Exception as e:
            result["error"] = f"Execution error: {e}"
            
        finally:
            # Restore stdout and cancel alarm
            signal.alarm(0)
            sys.stdout = old_stdout
        
        return result
    
    def _timeout_handler(self, signum, frame):
        """Handle execution timeout"""
        raise SandboxViolation(f"Execution exceeded {self.max_time} seconds")
    
    def _restricted_import(self, name, *args, **kwargs):
        """Restrict imports to allowlist"""
        if name not in self.allowed_modules:
            raise SandboxViolation(f"Import of '{name}' not allowed")
        return __import__(name, *args, **kwargs)

def test_sandbox():
    """Test sandbox restrictions"""
    sandbox = Sandbox(max_time=5)
    
    print("Testing Sandbox Restrictions\n")
    
    # Test 1: Safe code
    print("Test 1: Safe code execution")
    code = """
result = sum(range(10))
print(f"Sum: {result}")
"""
    result = sandbox.execute(code)
    print(f"Success: {result['success']}")
    print(f"Output: {result['output']}")
    print()
    
    # Test 2: Blocked import
    print("Test 2: Blocked import (os)")
    code = """
import os
os.system('ls')
"""
    result = sandbox.execute(code)
    print(f"Success: {result['success']}")
    print(f"Error: {result['error']}")
    print()
    
    # Test 3: Blocked built-in
    print("Test 3: Blocked built-in (open)")
    code = """
with open('/etc/passwd', 'r') as f:
    print(f.read())
"""
    result = sandbox.execute(code)
    print(f"Success: {result['success']}")
    print(f"Error: {result['error']}")
    print()
    
    # Test 4: Allowed import
    print("Test 4: Allowed import (math)")
    code = """
import math
print(f"Pi: {math.pi}")
"""
    result = sandbox.execute(code)
    print(f"Success: {result['success']}")
    print(f"Output: {result['output']}")
    print()
    
    # Test 5: Timeout
    print("Test 5: Execution timeout")
    code = """
while True:
    pass
"""
    result = sandbox.execute(code)
    print(f"Success: {result['success']}")
    print(f"Error: {result['error']}")
    print()

if __name__ == "__main__":
    test_sandbox()
