# Pattern 3: Sandboxing

## Concept

**Principle**: Isolate agent execution in a restricted environment with limited capabilities.

## The Problem

Agents with unrestricted access can:
- Access sensitive files
- Make network requests to arbitrary endpoints
- Execute system commands
- Consume unlimited resources
- Persist malicious changes

## The Solution

Run agent in a sandbox with strict limits:

```
┌─────────────────────────────────────────────────────────┐
│                    SANDBOX ENVIRONMENT                  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              LLM Agent Process                   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  Restrictions:                                          │
│  ✓ File System: Read-only or restricted directories    │
│  ✓ Network: Allowlist of endpoints only                │
│  ✓ System Calls: Blocked or limited                    │
│  ✓ Resources: CPU, memory, time limits                 │
│  ✓ Processes: Cannot spawn new processes               │
│                                                         │
│  Violations → Immediate termination                     │
└─────────────────────────────────────────────────────────┘
```

## Why It Works

1. **Least privilege**: Agent gets minimal necessary capabilities
2. **Containment**: Compromised agent can't escape sandbox
3. **Resource limits**: Prevents DoS attacks
4. **Fail-safe**: Violations terminate execution
5. **Defense-in-depth**: Works even if other defenses fail

## Sandbox Dimensions

### File System Isolation
- **Read-only root**: System files cannot be modified
- **Restricted writes**: Only specific directories writable
- **No path traversal**: Cannot access parent directories
- **Temporary storage**: Cleared after execution

### Network Isolation
- **Endpoint allowlist**: Only approved URLs/IPs accessible
- **Protocol restrictions**: Only HTTPS allowed
- **No localhost**: Cannot access local services
- **Rate limiting**: Prevent network flooding

### Process Isolation
- **No shell access**: Cannot execute system commands
- **No subprocess**: Cannot spawn new processes
- **No privilege escalation**: Cannot change permissions
- **Single-threaded**: Limited concurrency

### Resource Limits
- **CPU time**: Maximum execution time (e.g., 30 seconds)
- **Memory**: Maximum RAM usage (e.g., 512MB)
- **Disk I/O**: Limited read/write operations
- **Network bandwidth**: Rate-limited requests

## Implementation Approaches

### Approach 1: Docker Container
```bash
docker run --rm \
  --read-only \
  --network=none \
  --memory=512m \
  --cpus=0.5 \
  --pids-limit=10 \
  agent:latest
```

### Approach 2: Python Sandbox (RestrictedPython)
```python
from RestrictedPython import compile_restricted

# Compile code with restrictions
code = compile_restricted(user_code, '<string>', 'exec')

# Execute with limited globals
safe_globals = {'__builtins__': safe_builtins}
exec(code, safe_globals)
```

### Approach 3: AWS Lambda
- Automatic sandboxing
- Resource limits enforced
- Network isolation via VPC
- Temporary file system

## Real-World Example: Code Execution Agent

**Vulnerable (No Sandbox)**:
```python
# Agent can execute arbitrary code
user_code = "import os; os.system('rm -rf /')"
exec(user_code)  # ✗ DANGEROUS
```

**Secure (Sandboxed)**:
```python
# Agent runs in restricted environment
sandbox = Sandbox(
    allowed_imports=['math', 'json'],
    max_time=5,
    max_memory=100_000_000
)
result = sandbox.execute(user_code)  # ✓ SAFE
```

## Attack Resistance

| Attack Type | No Sandbox | With Sandbox |
|-------------|------------|--------------|
| File System Access | ✗ Succeeds | ✓ Blocked |
| Network Exfiltration | ✗ Succeeds | ✓ Blocked |
| System Commands | ✗ Succeeds | ✓ Blocked |
| Resource Exhaustion | ✗ Succeeds | ✓ Blocked |
| Privilege Escalation | ✗ Succeeds | ✓ Blocked |

## Sandbox Configuration Example

```python
SANDBOX_CONFIG = {
    # File system
    "allowed_read_dirs": ["/app/data"],
    "allowed_write_dirs": ["/app/temp"],
    "max_file_size": 10_000_000,  # 10MB
    
    # Network
    "allowed_domains": ["api.company.com"],
    "allowed_protocols": ["https"],
    "max_requests_per_minute": 10,
    
    # Resources
    "max_execution_time": 30,  # seconds
    "max_memory": 512_000_000,  # 512MB
    "max_cpu_percent": 50,
    
    # Capabilities
    "allow_subprocess": False,
    "allow_network": True,
    "allow_file_write": True
}
```

## Code Example

See `app.py` for full implementation demonstrating:
- Python code execution in sandbox
- File system restrictions
- Network restrictions
- Resource limits
- Attack attempts failing due to sandbox

## Monitoring and Logging

```python
# Log all sandbox violations
@sandbox.on_violation
def handle_violation(violation):
    log.security_alert(
        event="sandbox_violation",
        type=violation.type,
        details=violation.details,
        timestamp=time.time()
    )
    # Terminate execution
    sandbox.terminate()
```

## Key Takeaways

1. **Isolation**: Run untrusted code in restricted environment
2. **Least privilege**: Grant minimal necessary capabilities
3. **Resource limits**: Prevent DoS and resource exhaustion
4. **Fail-safe**: Violations terminate execution immediately
5. **Defense-in-depth**: Last line of defense when others fail
6. **Monitoring**: Log all violations for security analysis
