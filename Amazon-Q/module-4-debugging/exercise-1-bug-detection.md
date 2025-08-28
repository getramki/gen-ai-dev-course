# Exercise 1: Bug Detection and Fixing

## Objective
Master Amazon Q's bug detection capabilities by identifying and fixing various types of errors.

**Time:** 15 minutes  
**Difficulty:** Intermediate

---

## Setup Instructions

### Create Debugging Workspace
```bash
mkdir debugging-practice
cd debugging-practice
```

---

## Part A: Logic Errors (5 minutes)

### Task A1: Mathematical Functions with Hidden Bugs

**Create file:** `math_functions.py`
```python
def calculate_average(numbers):
    """Calculate average of a list of numbers"""
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

def find_maximum(arr):
    """Find maximum value in array"""
    max_val = 0
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val

def factorial(n):
    """Calculate factorial of n"""
    if n == 0:
        return 1
    return n * factorial(n - 1)

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def binary_search(arr, target):
    """Binary search implementation"""
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def fibonacci(n):
    """Generate nth Fibonacci number"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def gcd(a, b):
    """Calculate Greatest Common Divisor"""
    while b:
        a, b = b, a % b
    return a

def power(base, exponent):
    """Calculate base raised to exponent"""
    result = 1
    for i in range(exponent):
        result *= base
    return result
```

**Amazon Q Debugging Tasks:**

1. **Test Edge Cases:**
```
@math_functions.py Find bugs by testing these functions with edge cases like empty lists, negative numbers, and zero values
```

2. **Specific Bug Analysis:**
```
What happens when calculate_average receives an empty list? Fix this issue.
```

3. **Performance and Logic Issues:**
```
Test find_maximum with the array [-5, -2, -10, -1]. What's wrong and how to fix it?
```

4. **Boundary Condition Bugs:**
```
Debug binary_search - test it with a sorted array [1, 3, 5, 7, 9] searching for 5. What's the issue?
```

5. **Efficiency Problems:**
```
Analyze is_prime function for large numbers. What's inefficient and how to optimize?
```

**Expected Bug Discoveries:**
- `calculate_average`: Division by zero with empty list
- `find_maximum`: Fails with all negative numbers (initializes max_val to 0)
- `factorial`: No handling for negative inputs, potential stack overflow
- `binary_search`: Off-by-one error in right boundary
- `is_prime`: Inefficient - should only check up to sqrt(n)
- `power`: No handling for negative exponents

### Task A2: String Processing Bugs

**Create file:** `string_processor.py`
```python
def reverse_words(sentence):
    """Reverse order of words in sentence"""
    words = sentence.split(' ')
    reversed_words = []
    for i in range(len(words) - 1, 0, -1):
        reversed_words.append(words[i])
    return ' '.join(reversed_words)

def count_vowels(text):
    """Count vowels in text"""
    vowels = 'aeiou'
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

def is_palindrome(s):
    """Check if string is palindrome"""
    cleaned = s.replace(' ', '').lower()
    return cleaned == cleaned[::-1]

def extract_numbers(text):
    """Extract all numbers from text"""
    numbers = []
    current_number = ""
    
    for char in text:
        if char.isdigit():
            current_number += char
        else:
            if current_number:
                numbers.append(int(current_number))
                current_number = ""
    
    return numbers

def capitalize_words(sentence):
    """Capitalize first letter of each word"""
    words = sentence.split(' ')
    capitalized = []
    for word in words:
        if len(word) > 0:
            capitalized.append(word[0].upper() + word[1:])
    return ' '.join(capitalized)
```

**Amazon Q Tasks:**
```
@string_processor.py Identify bugs in these string processing functions and suggest fixes
```

```
Test reverse_words with "hello world" - what's missing?
```

```
Check extract_numbers with "price is 123 dollars" - what happens to the last number?
```

---

## Part B: Runtime Errors (5 minutes)

### Task B1: Exception-Prone Code

**Create file:** `error_prone.py`
```python
import json
import requests
from datetime import datetime

def process_user_data(users):
    """Process list of user dictionaries"""
    results = []
    for user in users:
        full_name = user['first_name'] + ' ' + user['last_name']
        age_next_year = user['age'] + 1
        email_domain = user['email'].split('@')[1]
        
        results.append({
            'name': full_name,
            'age_next_year': age_next_year,
            'domain': email_domain
        })
    return results

def fetch_api_data(url):
    """Fetch data from API endpoint"""
    response = requests.get(url)
    data = json.loads(response.text)
    return data['results'][0]['value']

def divide_and_calculate(numbers):
    """Perform division calculations"""
    results = []
    for i in range(len(numbers) - 1):
        result = numbers[i] / numbers[i + 1]
        results.append(result)
    return results

def access_nested_data(data):
    """Access deeply nested data structure"""
    user_theme = data['user']['profile']['settings']['theme']
    last_login = data['user']['activity']['last_login']
    preferences = data['user']['profile']['preferences']['notifications']
    
    return {
        'theme': user_theme,
        'last_login': last_login,
        'notifications': preferences
    }

def process_file_data(filename):
    """Process data from file"""
    with open(filename, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    first_line = lines[0]
    header_data = first_line.split(',')
    
    return {
        'columns': len(header_data),
        'first_column': header_data[0],
        'last_column': header_data[-1]
    }

def parse_date_string(date_str):
    """Parse date string to datetime object"""
    return datetime.strptime(date_str, '%Y-%m-%d')

def calculate_statistics(data_list):
    """Calculate basic statistics"""
    total = sum(data_list)
    average = total / len(data_list)
    maximum = max(data_list)
    minimum = min(data_list)
    
    return {
        'total': total,
        'average': average,
        'max': maximum,
        'min': minimum
    }
```

**Amazon Q Error Analysis Tasks:**

1. **Identify Potential Exceptions:**
```
@error_prone.py Analyze this code and identify all potential runtime exceptions that could occur
```

2. **Specific Error Scenarios:**
```
What exceptions could process_user_data raise? Provide examples of problematic input data.
```

3. **Network and I/O Errors:**
```
What could go wrong in fetch_api_data and process_file_data? Add proper error handling.
```

4. **Data Structure Errors:**
```
Test access_nested_data with incomplete data structures. What errors occur?
```

**Expected Error Types:**
- `KeyError`: Missing dictionary keys
- `IndexError`: List index out of bounds
- `ZeroDivisionError`: Division by zero
- `FileNotFoundError`: Missing files
- `ValueError`: Invalid data formats
- `TypeError`: Wrong data types
- `AttributeError`: Missing object attributes

### Task B2: Add Error Handling

**Amazon Q Task:**
```
@error_prone.py Add comprehensive error handling to all functions with appropriate exception types and user-friendly error messages
```

**Expected Improvements:**
- Try-catch blocks around risky operations
- Input validation
- Graceful error recovery
- Informative error messages
- Proper resource cleanup

---

## Part C: Concurrency and Race Condition Bugs (5 minutes)

### Task C1: Threading Issues

**Create file:** `concurrent_bugs.py`
```python
import threading
import time
from queue import Queue

class BankAccount:
    """Bank account with potential race conditions"""
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
    
    def deposit(self, amount):
        """Deposit money to account"""
        current_balance = self.balance
        time.sleep(0.001)  # Simulate processing time
        self.balance = current_balance + amount
    
    def withdraw(self, amount):
        """Withdraw money from account"""
        if self.balance >= amount:
            current_balance = self.balance
            time.sleep(0.001)  # Simulate processing time
            self.balance = current_balance - amount
            return True
        return False

class Counter:
    """Thread-unsafe counter"""
    def __init__(self):
        self.count = 0
    
    def increment(self):
        """Increment counter"""
        temp = self.count
        temp += 1
        time.sleep(0.0001)  # Simulate work
        self.count = temp

def worker_function(shared_list, worker_id):
    """Worker that modifies shared data"""
    for i in range(100):
        shared_list.append(f"worker_{worker_id}_item_{i}")
        if len(shared_list) > 50:
            shared_list.pop(0)  # Remove first item

def producer_consumer_bug():
    """Producer-consumer with synchronization issues"""
    buffer = []
    
    def producer():
        for i in range(10):
            item = f"item_{i}"
            buffer.append(item)
            print(f"Produced: {item}")
            time.sleep(0.1)
    
    def consumer():
        while True:
            if buffer:
                item = buffer.pop(0)
                print(f"Consumed: {item}")
            time.sleep(0.15)
    
    # Start threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()
```

**Amazon Q Concurrency Analysis:**

1. **Race Condition Detection:**
```
@concurrent_bugs.py Identify race conditions and thread safety issues in this code
```

2. **Specific Threading Problems:**
```
Analyze the BankAccount class for race conditions. What happens with concurrent deposits and withdrawals?
```

3. **Synchronization Solutions:**
```
Fix the Counter class to be thread-safe using appropriate synchronization mechanisms
```

4. **Producer-Consumer Issues:**
```
What's wrong with the producer_consumer_bug function? How to fix it properly?
```

**Expected Issues:**
- Race conditions in balance updates
- Non-atomic operations on shared data
- Missing synchronization primitives
- Potential deadlocks
- Data corruption from concurrent access

---

## Bug Fix Verification

### Testing Your Fixes

**Create file:** `test_fixes.py`
```python
# Test cases to verify bug fixes

def test_math_functions():
    """Test mathematical function fixes"""
    # Test empty list handling
    try:
        result = calculate_average([])
        print("Empty list test failed - should raise exception")
    except ValueError as e:
        print(f"✓ Empty list handled correctly: {e}")
    
    # Test negative numbers
    result = find_maximum([-5, -2, -10, -1])
    assert result == -1, f"Expected -1, got {result}"
    print("✓ Negative numbers handled correctly")

def test_error_handling():
    """Test error handling improvements"""
    # Test missing keys
    incomplete_user = {'first_name': 'John'}  # Missing last_name
    try:
        result = process_user_data([incomplete_user])
        print("Missing key test failed")
    except (KeyError, ValueError) as e:
        print(f"✓ Missing key handled: {e}")

def test_thread_safety():
    """Test thread safety fixes"""
    account = BankAccount(1000)
    
    def make_transactions():
        for _ in range(100):
            account.deposit(10)
            account.withdraw(5)
    
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=make_transactions)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    expected_balance = 1000 + (5 * 100 * 5)  # Initial + (net_gain * transactions * threads)
    print(f"Final balance: {account.balance}, Expected: {expected_balance}")
```

---

## Success Criteria

You've mastered bug detection when you can:
- [ ] Identify logic errors through systematic testing
- [ ] Recognize potential runtime exceptions
- [ ] Spot race conditions and threading issues
- [ ] Add appropriate error handling
- [ ] Verify fixes with comprehensive tests
- [ ] Use Amazon Q effectively for debugging guidance

**Common Bug Categories Covered:**
- ✅ Logic errors and edge cases
- ✅ Runtime exceptions and error handling
- ✅ Concurrency and race conditions
- ✅ Input validation issues
- ✅ Resource management problems

**Completion Time:** 15 minutes  
**Next:** Exercise 2 - Code Optimization