# Module 4: Debugging and Troubleshooting

**Duration:** 25 minutes  
**Objective:** Master Amazon Q's debugging capabilities and code optimization techniques

---

## Topic 4.1: Error Analysis and Resolution (15 minutes)

### Understanding Error Analysis

Amazon Q can help with:
- **Syntax Errors:** Missing brackets, semicolons, indentation issues
- **Runtime Errors:** Null pointer exceptions, index out of bounds, type errors
- **Logic Errors:** Incorrect algorithms, wrong conditions, data flow issues
- **Performance Issues:** Memory leaks, inefficient algorithms, resource bottlenecks
- **Integration Errors:** API failures, database connection issues, dependency conflicts

### Types of Debugging Assistance

#### Error Message Interpretation
```
"Explain this error message and suggest fixes"
"What causes this exception and how to prevent it?"
"Analyze this stack trace and identify the root cause"
```

#### Code Review for Bugs
```
"Find potential bugs in this code"
"What could go wrong with this implementation?"
"Review this code for edge cases and error conditions"
```

#### Step-by-Step Debugging
```
"Walk through this code execution and identify where it fails"
"Trace the data flow and find the issue"
"Debug this function with sample input"
```

### Common Error Patterns

#### Null/Undefined Reference Errors
```python
# Common issue
def process_user(user):
    return user.name.upper()  # Fails if user is None or name is None

# Amazon Q suggests
def process_user(user):
    if user is None:
        raise ValueError("User cannot be None")
    if user.name is None:
        return "UNKNOWN"
    return user.name.upper()
```

#### Index Out of Bounds
```python
# Problematic code
def get_first_three(items):
    return [items[0], items[1], items[2]]

# Amazon Q suggests
def get_first_three(items):
    if len(items) < 3:
        raise ValueError("List must have at least 3 items")
    return items[:3]
```

#### Type Errors
```python
# Issue with mixed types
def calculate_total(prices):
    total = 0
    for price in prices:
        total += price  # Fails if price is string
    return total

# Amazon Q suggests
def calculate_total(prices):
    total = 0
    for price in prices:
        try:
            total += float(price)
        except (ValueError, TypeError):
            raise TypeError(f"Invalid price format: {price}")
    return total
```

### Debugging Strategies

#### Systematic Approach
1. **Reproduce the Error:** Create minimal test case
2. **Analyze Error Message:** Understand what went wrong
3. **Trace Execution:** Follow code path to error
4. **Identify Root Cause:** Find underlying issue
5. **Implement Fix:** Address root cause, not symptoms
6. **Test Solution:** Verify fix works for all cases

#### Using Amazon Q for Debugging
```
"Debug this function with input [specific_input]"
"What happens when this code receives [edge_case]?"
"Trace through this algorithm step by step"
"Find the bug in this implementation"
```

---

## Topic 4.2: Code Optimization (10 minutes)

### Performance Optimization Areas

#### Algorithm Efficiency
- Time complexity improvements
- Space complexity optimization
- Data structure selection
- Algorithm choice optimization

#### Memory Management
- Memory leak detection
- Garbage collection optimization
- Resource cleanup
- Memory usage patterns

#### I/O Operations
- Database query optimization
- File handling efficiency
- Network request optimization
- Caching strategies

### Optimization Techniques

#### Time Complexity Improvements
```python
# O(n²) - Inefficient
def find_duplicates_slow(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates

# O(n) - Optimized
def find_duplicates_fast(arr):
    seen = set()
    duplicates = set()
    for item in arr:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)
```

#### Memory Optimization
```python
# Memory inefficient
def process_large_file_bad(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()  # Loads entire file into memory
    
    processed = []
    for line in lines:
        processed.append(line.strip().upper())
    return processed

# Memory efficient
def process_large_file_good(filename):
    def line_generator():
        with open(filename, 'r') as f:
            for line in f:
                yield line.strip().upper()
    
    return line_generator()
```

#### Database Query Optimization
```python
# Inefficient - N+1 query problem
def get_users_with_orders_bad():
    users = User.query.all()
    result = []
    for user in users:
        orders = Order.query.filter_by(user_id=user.id).all()  # N queries
        result.append({'user': user, 'orders': orders})
    return result

# Efficient - Single query with join
def get_users_with_orders_good():
    return db.session.query(User).options(
        joinedload(User.orders)
    ).all()
```

### Performance Analysis

#### Profiling and Benchmarking
```
"Analyze the performance bottlenecks in this code"
"Compare the efficiency of these two implementations"
"Suggest optimizations for this slow function"
"Profile this code and identify improvement areas"
```

#### Scalability Considerations
```
"How will this code perform with 1 million records?"
"What are the scalability limitations of this approach?"
"Suggest improvements for handling large datasets"
```

---

## Hands-On Exercise 4.1: Bug Detection and Fixing

### Objective
Practice identifying and fixing various types of bugs using Amazon Q.

### Setup
Create debugging workspace with intentionally buggy code.

### Task 1: Logic Errors (5 minutes)

**Create file:** `buggy_calculator.py`
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

def find_maximum(arr):
    max_val = 0
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def binary_search(arr, target):
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
```

**Amazon Q Tasks:**
1. "Find all bugs in this calculator code"
2. "What happens if calculate_average receives an empty list?"
3. "Test find_maximum with negative numbers"
4. "Check factorial function for edge cases"
5. "Debug binary_search with sample data"

### Task 2: Runtime Errors (5 minutes)

**Create file:** `error_prone_code.py`
```python
import json
import requests

def process_user_data(users):
    results = []
    for user in users:
        full_name = user['first_name'] + ' ' + user['last_name']
        age_next_year = user['age'] + 1
        results.append({
            'name': full_name,
            'age_next_year': age_next_year
        })
    return results

def fetch_api_data(url):
    response = requests.get(url)
    data = json.loads(response.text)
    return data['results'][0]['value']

def divide_numbers(a, b):
    return a / b

def access_nested_data(data):
    return data['user']['profile']['settings']['theme']

def process_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    first_line = lines[0]
    return first_line.strip().upper()
```

**Amazon Q Tasks:**
1. "Identify potential runtime errors in this code"
2. "What error handling is missing?"
3. "Test these functions with problematic inputs"
4. "Add proper exception handling"

### Task 3: Performance Issues (5 minutes)

**Create file:** `slow_algorithms.py`
```python
def slow_fibonacci(n):
    if n <= 1:
        return n
    return slow_fibonacci(n-1) + slow_fibonacci(n-2)

def inefficient_search(data, target):
    found_items = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == target:
                found_items.append((i, j))
    return found_items

def memory_waster(n):
    big_list = []
    for i in range(n):
        big_list.append([0] * 1000000)
    return len(big_list)

def string_concatenation_slow(words):
    result = ""
    for word in words:
        result = result + word + " "
    return result.strip()
```

**Amazon Q Tasks:**
1. "Analyze performance issues in these algorithms"
2. "Suggest optimizations for slow_fibonacci"
3. "Improve the efficiency of inefficient_search"
4. "Fix memory usage in memory_waster"
5. "Optimize string concatenation"

---

## Hands-On Exercise 4.2: Code Optimization

### Objective
Learn to optimize code performance using Amazon Q suggestions.

### Task 1: Algorithm Optimization (3 minutes)

**Create file:** `optimization_targets.py`
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def linear_search_all(arr, target):
    positions = []
    for i in range(len(arr)):
        if arr[i] == target:
            positions.append(i)
    return positions

def count_duplicates(arr):
    duplicates = {}
    for item in arr:
        count = 0
        for other_item in arr:
            if item == other_item:
                count += 1
        if count > 1:
            duplicates[item] = count
    return duplicates
```

**Amazon Q Tasks:**
1. "Optimize bubble_sort for better performance"
2. "Improve linear_search_all efficiency"
3. "Reduce time complexity of count_duplicates"

### Task 2: Memory Optimization (4 minutes)

**Create file:** `memory_intensive.py`
```python
def process_large_dataset(data):
    # Creates multiple copies of data
    filtered_data = []
    for item in data:
        if item['active']:
            filtered_data.append(item)
    
    processed_data = []
    for item in filtered_data:
        processed_item = {
            'id': item['id'],
            'name': item['name'].upper(),
            'score': item['score'] * 2
        }
        processed_data.append(processed_item)
    
    return processed_data

def generate_report(users):
    # Inefficient string building
    report = ""
    report += "User Report\n"
    report += "=" * 50 + "\n"
    
    for user in users:
        report += f"Name: {user['name']}\n"
        report += f"Email: {user['email']}\n"
        report += f"Status: {user['status']}\n"
        report += "-" * 30 + "\n"
    
    return report
```

**Amazon Q Tasks:**
1. "Optimize memory usage in process_large_dataset"
2. "Improve string building in generate_report"
3. "Suggest generator-based alternatives"

### Task 3: Database Query Optimization (3 minutes)

**Create file:** `database_queries.py`
```python
# Simulated ORM-style code
class User:
    @classmethod
    def get_by_id(cls, user_id):
        # Simulates database query
        pass
    
    @classmethod
    def get_all(cls):
        # Simulates getting all users
        pass

class Order:
    @classmethod
    def get_by_user_id(cls, user_id):
        # Simulates getting orders for user
        pass

def get_user_order_summary():
    # N+1 query problem
    users = User.get_all()
    summary = []
    
    for user in users:
        orders = Order.get_by_user_id(user.id)
        total_orders = len(orders)
        total_amount = sum(order.amount for order in orders)
        
        summary.append({
            'user_id': user.id,
            'name': user.name,
            'total_orders': total_orders,
            'total_amount': total_amount
        })
    
    return summary

def search_users_by_criteria(name=None, email=None, status=None):
    # Inefficient filtering
    all_users = User.get_all()
    results = []
    
    for user in all_users:
        match = True
        if name and name.lower() not in user.name.lower():
            match = False
        if email and email.lower() not in user.email.lower():
            match = False
        if status and user.status != status:
            match = False
        
        if match:
            results.append(user)
    
    return results
```

**Amazon Q Tasks:**
1. "Identify the N+1 query problem"
2. "Optimize get_user_order_summary"
3. "Improve search_users_by_criteria efficiency"

---

## Advanced Debugging Techniques

### Error Pattern Recognition

#### Common Patterns Amazon Q Can Identify
- **Race Conditions:** Concurrent access issues
- **Memory Leaks:** Unreleased resources
- **Infinite Loops:** Non-terminating conditions
- **Stack Overflow:** Excessive recursion
- **Deadlocks:** Circular waiting conditions

### Debugging Prompts

#### Effective Debugging Questions
```
"What could cause this function to fail?"
"Trace through this code with input X"
"Find edge cases that break this logic"
"Analyze this error message: [error_text]"
"Why might this code be slow?"
```

#### Context-Specific Debugging
```
"Debug this web API endpoint that returns 500 errors"
"Find the issue in this database transaction"
"Analyze this concurrent code for race conditions"
"Check this recursive function for stack overflow"
```

---

## Performance Profiling

### Identifying Bottlenecks

#### CPU-Bound Issues
- Inefficient algorithms
- Excessive computations
- Poor loop optimization
- Redundant calculations

#### I/O-Bound Issues
- Slow database queries
- Inefficient file operations
- Network latency problems
- Blocking operations

#### Memory-Bound Issues
- Memory leaks
- Excessive object creation
- Large data structures
- Poor garbage collection

### Optimization Strategies

#### Algorithm Improvements
```
"Replace this O(n²) algorithm with O(n log n) alternative"
"Use hash tables instead of linear search"
"Implement caching for expensive operations"
"Apply memoization to recursive functions"
```

#### Resource Management
```
"Add connection pooling for database access"
"Implement lazy loading for large datasets"
"Use generators instead of lists for memory efficiency"
"Add proper resource cleanup in finally blocks"
```

---

## Quality Assessment

### Bug Detection Quality
- ✅ Identifies actual bugs vs false positives
- ✅ Explains root cause clearly
- ✅ Suggests appropriate fixes
- ✅ Considers edge cases and error conditions
- ✅ Provides prevention strategies

### Optimization Effectiveness
- ✅ Significant performance improvements
- ✅ Maintains code correctness
- ✅ Considers trade-offs (time vs space)
- ✅ Scalability improvements
- ✅ Real-world applicability

---

## Troubleshooting Common Issues

### When Amazon Q Misses Bugs
- Provide more context about expected behavior
- Include sample inputs and expected outputs
- Describe the specific problem symptoms
- Add information about the runtime environment

### When Optimizations Don't Help
- Profile the code to identify actual bottlenecks
- Consider the specific use case and constraints
- Test with realistic data sizes
- Measure before and after performance

---

## Key Takeaways

After Module 4, you should be able to:
- Effectively use Amazon Q to identify and fix bugs
- Optimize code performance with AI assistance
- Understand common error patterns and solutions
- Apply systematic debugging approaches
- Recognize performance bottlenecks and optimization opportunities

**Time Required:** 25 minutes  
**Difficulty:** Intermediate to Advanced  
**Next:** Module 5 - Security and Best Practices