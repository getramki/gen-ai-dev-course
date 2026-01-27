#!/usr/bin/env python3
"""
Classic Code Injection Examples (SQL and Command Injection)
Demonstrates how traditional injection attacks work and how they're prevented.
"""

import sqlite3
import subprocess
import shlex
from typing import List, Dict


def setup_database():
    """Create a simple in-memory database for demonstration."""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT,
            role TEXT
        )
    ''')
    
    cursor.executemany(
        'INSERT INTO users (username, email, role) VALUES (?, ?, ?)',
        [
            ('alice', 'alice@example.com', 'user'),
            ('bob', 'bob@example.com', 'user'),
            ('admin', 'admin@example.com', 'admin'),
        ]
    )
    
    conn.commit()
    return conn


# ============================================================================
# SQL INJECTION EXAMPLES
# ============================================================================

def sql_injection_vulnerable(conn, username: str) -> List[Dict]:
    """VULNERABLE: String concatenation allows SQL injection."""
    cursor = conn.cursor()
    
    # VULNERABLE CODE - DO NOT USE IN PRODUCTION
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"[VULNERABLE] Executing: {query}")
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return [{'id': r[0], 'username': r[1], 'email': r[2], 'role': r[3]} for r in results]
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
        return []


def sql_injection_secure(conn, username: str) -> List[Dict]:
    """SECURE: Parameterized query prevents SQL injection."""
    cursor = conn.cursor()
    
    # SECURE CODE - Uses parameterized query
    query = "SELECT * FROM users WHERE username = ?"
    print(f"[SECURE] Executing: {query} with params: [{username}]")
    
    cursor.execute(query, (username,))
    results = cursor.fetchall()
    return [{'id': r[0], 'username': r[1], 'email': r[2], 'role': r[3]} for r in results]


def demonstrate_sql_injection():
    """Demonstrate SQL injection attack and defense."""
    print("=" * 70)
    print("SQL INJECTION DEMONSTRATION")
    print("=" * 70)
    
    conn = setup_database()
    
    # Normal usage
    print("\n1. NORMAL USAGE")
    print("-" * 70)
    results = sql_injection_vulnerable(conn, "alice")
    print(f"Results: {results}\n")
    
    # Attack: SQL injection to bypass authentication
    print("2. ATTACK: SQL Injection (OR 1=1)")
    print("-" * 70)
    malicious_input = "' OR '1'='1"
    print(f"Attacker input: {malicious_input}")
    results = sql_injection_vulnerable(conn, malicious_input)
    print(f"Results: {results}")
    print("⚠️  ATTACK SUCCESSFUL: Retrieved all users!\n")
    
    # Attack: SQL injection with UNION
    print("3. ATTACK: SQL Injection (UNION)")
    print("-" * 70)
    malicious_input = "' UNION SELECT 1, 'hacker', 'hacker@evil.com', 'admin' --"
    print(f"Attacker input: {malicious_input}")
    results = sql_injection_vulnerable(conn, malicious_input)
    print(f"Results: {results}")
    print("⚠️  ATTACK SUCCESSFUL: Injected fake admin user!\n")
    
    # Defense: Parameterized query
    print("4. DEFENSE: Parameterized Query")
    print("-" * 70)
    malicious_input = "' OR '1'='1"
    print(f"Attacker input: {malicious_input}")
    results = sql_injection_secure(conn, malicious_input)
    print(f"Results: {results}")
    print("✅ DEFENSE SUCCESSFUL: Attack treated as literal string!\n")
    
    conn.close()


# ============================================================================
# COMMAND INJECTION EXAMPLES
# ============================================================================

def command_injection_vulnerable(filename: str) -> str:
    """VULNERABLE: Shell=True allows command injection."""
    # VULNERABLE CODE - DO NOT USE IN PRODUCTION
    command = f"cat {filename}"
    print(f"[VULNERABLE] Executing: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,  # DANGEROUS: Allows shell interpretation
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout
    except Exception as e:
        return f"Error: {e}"


def command_injection_secure(filename: str) -> str:
    """SECURE: No shell and argument list prevents command injection."""
    # SECURE CODE - Uses argument list without shell
    print(f"[SECURE] Executing: cat with args: [{filename}]")
    
    try:
        result = subprocess.run(
            ['cat', filename],  # Argument list
            shell=False,  # No shell interpretation
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout
    except Exception as e:
        return f"Error: {e}"


def demonstrate_command_injection():
    """Demonstrate command injection attack and defense."""
    print("=" * 70)
    print("COMMAND INJECTION DEMONSTRATION")
    print("=" * 70)
    
    # Create test file
    test_file = "/tmp/test_file.txt"
    with open(test_file, 'w') as f:
        f.write("This is a test file.\n")
    
    # Normal usage
    print("\n1. NORMAL USAGE")
    print("-" * 70)
    result = command_injection_vulnerable(test_file)
    print(f"Output: {result}")
    
    # Attack: Command injection
    print("2. ATTACK: Command Injection (Command Chaining)")
    print("-" * 70)
    malicious_input = "/tmp/test_file.txt; echo 'HACKED' > /tmp/hacked.txt; cat /tmp/hacked.txt"
    print(f"Attacker input: {malicious_input}")
    result = command_injection_vulnerable(malicious_input)
    print(f"Output: {result}")
    print("⚠️  ATTACK SUCCESSFUL: Executed arbitrary commands!\n")
    
    # Defense: No shell, argument list
    print("3. DEFENSE: No Shell + Argument List")
    print("-" * 70)
    malicious_input = "/tmp/test_file.txt; echo 'HACKED'"
    print(f"Attacker input: {malicious_input}")
    result = command_injection_secure(malicious_input)
    print(f"Output: {result}")
    print("✅ DEFENSE SUCCESSFUL: Special characters treated as filename!\n")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

def print_key_takeaways():
    """Print key lessons from code injection examples."""
    print("=" * 70)
    print("KEY TAKEAWAYS: CODE INJECTION")
    print("=" * 70)
    print("""
1. CODE INJECTION HAS CLEAR SOLUTIONS:
   - SQL: Use parameterized queries
   - Commands: Use argument lists without shell
   
2. WHY THESE SOLUTIONS WORK:
   - Clear boundary between code and data
   - Special characters have well-defined meanings
   - Escaping mechanisms are standardized
   
3. DEFENSE IS INPUT-BASED:
   - Prevent malicious input from becoming code
   - Validation and sanitization are effective
   
4. DETECTION IS RELIABLE:
   - Limited set of attack patterns
   - Syntax-based detection works
   
5. PROBLEM IS SOLVED:
   - Best practices are well-established
   - Tools enforce secure patterns
   - Frameworks provide safe defaults

Now compare this to prompt injection (see prompt_injection_example.py)
where NONE of these solutions work!
""")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    demonstrate_sql_injection()
    print("\n")
    demonstrate_command_injection()
    print("\n")
    print_key_takeaways()
