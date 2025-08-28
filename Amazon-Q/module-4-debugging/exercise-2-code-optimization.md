# Exercise 2: Code Optimization

## Objective
Master Amazon Q's code optimization capabilities by improving algorithm efficiency and performance.

**Time:** 10 minutes  
**Difficulty:** Intermediate to Advanced

---

## Setup Instructions

### Create Optimization Workspace
```bash
mkdir optimization-practice
cd optimization-practice
```

---

## Part A: Algorithm Optimization (4 minutes)

### Task A1: Inefficient Algorithms

**Create file:** `slow_algorithms.py`
```python
import time
import random

def bubble_sort(arr):
    """Bubble sort - O(n²) time complexity"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def linear_search_all(arr, target):
    """Find all occurrences using linear search"""
    positions = []
    for i in range(len(arr)):
        if arr[i] == target:
            positions.append(i)
    return positions

def count_duplicates(arr):
    """Count duplicates - O(n²) approach"""
    duplicates = {}
    for item in arr:
        count = 0
        for other_item in arr:
            if item == other_item:
                count += 1
        if count > 1:
            duplicates[item] = count
    return duplicates

def find_common_elements(list1, list2):
    """Find common elements between two lists"""
    common = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2 and item1 not in common:
                common.append(item1)
    return common

def fibonacci_recursive(n):
    """Recursive Fibonacci - exponential time complexity"""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def matrix_multiply_naive(A, B):
    """Naive matrix multiplication"""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Cannot multiply matrices")
    
    result = []
    for i in range(rows_A):
        row = []
        for j in range(cols_B):
            sum_val = 0
            for k in range(cols_A):
                sum_val += A[i][k] * B[k][j]
            row.append(sum_val)
        result.append(row)
    
    return result

def is_subset(small_list, large_list):
    """Check if small_list is subset of large_list"""
    for item in small_list:
        found = False
        for large_item in large_list:
            if item == large_item:
                found = True
                break
        if not found:
            return False
    return True
```

**Amazon Q Optimization Tasks:**

1. **Time Complexity Analysis:**
```
@slow_algorithms.py Analyze the time complexity of each algorithm and suggest more efficient alternatives
```

2. **Specific Algorithm Improvements:**
```
Replace bubble_sort with a more efficient sorting algorithm. What's the best choice and why?
```

3. **Data Structure Optimization:**
```
Optimize count_duplicates using appropriate data structures to reduce time complexity from O(n²) to O(n)
```

4. **Fibonacci Optimization:**
```
Fix fibonacci_recursive to avoid exponential time complexity. Show both iterative and memoized solutions.
```

**Expected Optimizations:**
- `bubble_sort` → `quicksort` or `mergesort` (O(n log n))
- `count_duplicates` → Use dictionary/hash map (O(n))
- `find_common_elements` → Use sets for intersection (O(n + m))
- `fibonacci_recursive` → Iterative or memoized approach (O(n))
- `is_subset` → Convert to sets and use subset operation (O(n + m))

### Task A2: Search and Sort Optimization

**Create file:** `search_sort_slow.py`
```python
def find_kth_largest(arr, k):
    """Find kth largest element by sorting entire array"""
    sorted_arr = sorted(arr, reverse=True)
    return sorted_arr[k-1]

def binary_search_inefficient(arr, target):
    """Binary search with unnecessary operations"""
    arr = sorted(arr)  # Sorts every time
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def merge_sorted_arrays_slow(arr1, arr2):
    """Merge two sorted arrays inefficiently"""
    merged = arr1 + arr2
    return sorted(merged)

def find_median(arr):
    """Find median by sorting entire array"""
    sorted_arr = sorted(arr)
    n = len(sorted_arr)
    if n % 2 == 0:
        return (sorted_arr[n//2 - 1] + sorted_arr[n//2]) / 2
    else:
        return sorted_arr[n//2]

def remove_duplicates_slow(arr):
    """Remove duplicates while preserving order"""
    result = []
    for item in arr:
        if item not in result:
            result.append(item)
    return result
```

**Amazon Q Tasks:**
```
@search_sort_slow.py Optimize these search and sort operations for better performance
```

```
Improve find_kth_largest to avoid sorting the entire array. What algorithm should be used?
```

```
Fix binary_search_inefficient to avoid unnecessary sorting on each call
```

---

## Part B: Memory Optimization (3 minutes)

### Task B1: Memory-Intensive Operations

**Create file:** `memory_wasters.py`
```python
def process_large_dataset(data):
    """Creates multiple copies of large dataset"""
    # Step 1: Filter active users
    active_users = []
    for user in data:
        if user.get('active', False):
            active_users.append(user)
    
    # Step 2: Transform data
    transformed_users = []
    for user in active_users:
        transformed_user = {
            'id': user['id'],
            'name': user['name'].upper(),
            'email': user['email'].lower(),
            'score': user.get('score', 0) * 2,
            'category': 'premium' if user.get('score', 0) > 100 else 'standard'
        }
        transformed_users.append(transformed_user)
    
    # Step 3: Sort by score
    sorted_users = sorted(transformed_users, key=lambda x: x['score'], reverse=True)
    
    return sorted_users

def generate_report(users):
    """Inefficient string concatenation"""
    report = ""
    report += "User Report\n"
    report += "=" * 50 + "\n"
    report += f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Total users: {len(users)}\n"
    report += "-" * 50 + "\n"
    
    for user in users:
        report += f"ID: {user['id']}\n"
        report += f"Name: {user['name']}\n"
        report += f"Email: {user['email']}\n"
        report += f"Score: {user['score']}\n"
        report += f"Category: {user['category']}\n"
        report += "-" * 30 + "\n"
    
    return report

def load_and_process_file(filename):
    """Loads entire file into memory"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    processed_lines = []
    for line in lines:
        cleaned_line = line.strip().upper()
        if len(cleaned_line) > 0:
            processed_lines.append(cleaned_line)
    
    return processed_lines

def create_lookup_table(items):
    """Creates inefficient lookup structure"""
    lookup = []
    for item in items:
        lookup.append({
            'key': item['id'],
            'value': item,
            'searchable': f"{item['name']} {item['email']} {item.get('department', '')}"
        })
    return lookup

def calculate_statistics(numbers):
    """Stores intermediate results unnecessarily"""
    squared_numbers = [x**2 for x in numbers]
    cubed_numbers = [x**3 for x in numbers]
    sqrt_numbers = [x**0.5 for x in numbers if x >= 0]
    
    stats = {
        'sum_squares': sum(squared_numbers),
        'sum_cubes': sum(cubed_numbers),
        'sum_sqrt': sum(sqrt_numbers),
        'mean_squares': sum(squared_numbers) / len(squared_numbers),
        'mean_cubes': sum(cubed_numbers) / len(cubed_numbers)
    }
    
    return stats
```

**Amazon Q Memory Optimization Tasks:**

1. **Memory Usage Analysis:**
```
@memory_wasters.py Analyze memory usage patterns and suggest optimizations to reduce memory footprint
```

2. **Generator-Based Solutions:**
```
Convert process_large_dataset to use generators instead of creating intermediate lists
```

3. **String Building Optimization:**
```
Optimize generate_report to use more efficient string building techniques
```

4. **Streaming File Processing:**
```
Modify load_and_process_file to process files in chunks instead of loading everything into memory
```

**Expected Optimizations:**
- Use generators for data processing pipelines
- Replace string concatenation with `join()` or `StringIO`
- Process files line by line instead of loading all
- Use dictionary for O(1) lookups instead of lists
- Calculate statistics in single pass without storing intermediates

### Task B2: Resource Management

**Create file:** `resource_leaks.py`
```python
import sqlite3
import requests
import json
from contextlib import contextmanager

def database_operations_leaky():
    """Database operations without proper cleanup"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)')
    cursor.execute('INSERT INTO users VALUES (1, "John")')
    
    results = cursor.execute('SELECT * FROM users').fetchall()
    return results

def file_operations_risky(filenames):
    """File operations without proper resource management"""
    file_contents = {}
    
    for filename in filenames:
        try:
            f = open(filename, 'r')
            content = f.read()
            file_contents[filename] = content
        except FileNotFoundError:
            file_contents[filename] = None
    
    return file_contents

def network_requests_inefficient(urls):
    """Network requests without session reuse"""
    results = []
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results.append(data)
        except Exception as e:
            results.append({'error': str(e)})
    
    return results

class DataProcessor:
    """Class with resource management issues"""
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.temp_files = []
    
    def process_data(self, data):
        cursor = self.connection.cursor()
        
        # Create temporary file
        temp_filename = f"temp_{id(data)}.json"
        temp_file = open(temp_filename, 'w')
        json.dump(data, temp_file)
        self.temp_files.append(temp_filename)
        
        # Process data
        for item in data:
            cursor.execute('INSERT INTO processed_data VALUES (?, ?)', 
                         (item['id'], item['value']))
        
        return len(data)
```

**Amazon Q Resource Management Tasks:**
```
@resource_leaks.py Identify resource management issues and add proper cleanup using context managers
```

```
Fix database_operations_leaky to ensure connections are properly closed
```

```
Improve network_requests_inefficient to reuse connections and handle resources properly
```

---

## Part C: Database and I/O Optimization (3 minutes)

### Task C1: Database Query Optimization

**Create file:** `database_inefficient.py`
```python
# Simulated database operations
class Database:
    def execute_query(self, query, params=None):
        # Simulates database query execution
        pass
    
    def fetch_all(self, query, params=None):
        # Simulates fetching all results
        pass

def get_user_orders_slow(db, user_ids):
    """N+1 query problem"""
    users_with_orders = []
    
    for user_id in user_ids:
        # Query 1: Get user info
        user = db.fetch_all("SELECT * FROM users WHERE id = ?", (user_id,))[0]
        
        # Query 2: Get user orders (N queries)
        orders = db.fetch_all("SELECT * FROM orders WHERE user_id = ?", (user_id,))
        
        # Query 3: Get order details for each order
        detailed_orders = []
        for order in orders:
            order_details = db.fetch_all(
                "SELECT * FROM order_items WHERE order_id = ?", 
                (order['id'],)
            )
            detailed_orders.append({
                'order': order,
                'items': order_details
            })
        
        users_with_orders.append({
            'user': user,
            'orders': detailed_orders
        })
    
    return users_with_orders

def search_products_inefficient(db, filters):
    """Inefficient filtering and searching"""
    # Get all products first
    all_products = db.fetch_all("SELECT * FROM products")
    
    # Filter in Python instead of database
    filtered_products = []
    for product in all_products:
        match = True
        
        if filters.get('category') and product['category'] != filters['category']:
            match = False
        
        if filters.get('min_price') and product['price'] < filters['min_price']:
            match = False
        
        if filters.get('max_price') and product['price'] > filters['max_price']:
            match = False
        
        if filters.get('name') and filters['name'].lower() not in product['name'].lower():
            match = False
        
        if match:
            filtered_products.append(product)
    
    # Sort in Python
    if filters.get('sort_by'):
        filtered_products.sort(key=lambda x: x[filters['sort_by']])
    
    return filtered_products

def update_user_scores(db, score_updates):
    """Individual updates instead of batch"""
    updated_count = 0
    
    for user_id, new_score in score_updates.items():
        db.execute_query(
            "UPDATE users SET score = ? WHERE id = ?",
            (new_score, user_id)
        )
        updated_count += 1
    
    return updated_count
```

**Amazon Q Database Optimization Tasks:**

1. **Query Optimization:**
```
@database_inefficient.py Identify and fix the N+1 query problem in get_user_orders_slow
```

2. **Filtering Optimization:**
```
Optimize search_products_inefficient to use database-level filtering instead of Python filtering
```

3. **Batch Operations:**
```
Improve update_user_scores to use batch updates instead of individual queries
```

**Expected Optimizations:**
- Use JOINs to eliminate N+1 queries
- Move filtering logic to SQL WHERE clauses
- Use batch operations for multiple updates
- Add proper indexing suggestions
- Implement connection pooling

---

## Performance Measurement

### Task: Benchmark Your Optimizations

**Create file:** `benchmark_improvements.py`
```python
import time
import random
from memory_profiler import profile

def benchmark_sorting():
    """Compare sorting algorithm performance"""
    # Generate test data
    small_data = [random.randint(1, 1000) for _ in range(100)]
    large_data = [random.randint(1, 10000) for _ in range(5000)]
    
    # Test bubble sort vs optimized sort
    print("Sorting Algorithm Comparison:")
    
    # Small dataset
    start_time = time.time()
    bubble_sort(small_data.copy())
    bubble_time = time.time() - start_time
    
    start_time = time.time()
    sorted(small_data.copy())
    optimized_time = time.time() - start_time
    
    print(f"Small dataset (100 items):")
    print(f"  Bubble sort: {bubble_time:.4f}s")
    print(f"  Optimized sort: {optimized_time:.4f}s")
    print(f"  Improvement: {bubble_time/optimized_time:.1f}x faster")

@profile
def memory_usage_comparison():
    """Compare memory usage of different approaches"""
    # Test memory-efficient vs memory-wasteful approaches
    data = [{'id': i, 'value': random.randint(1, 100)} for i in range(10000)]
    
    # Memory wasteful approach
    result1 = process_large_dataset(data)
    
    # Memory efficient approach (after optimization)
    result2 = process_large_dataset_optimized(data)
    
    return len(result1), len(result2)

def performance_test_suite():
    """Run comprehensive performance tests"""
    print("Performance Test Results:")
    print("=" * 50)
    
    benchmark_sorting()
    memory_usage_comparison()
    
    # Add more benchmarks for other optimizations
```

**Amazon Q Benchmarking Task:**
```
Create comprehensive benchmarks to measure the performance improvements from our optimizations
```

---

## Success Criteria

You've mastered code optimization when you can:
- [ ] Identify algorithm complexity issues and suggest better alternatives
- [ ] Optimize memory usage through generators and efficient data structures
- [ ] Fix resource management problems with proper cleanup
- [ ] Eliminate database N+1 query problems
- [ ] Measure and verify performance improvements
- [ ] Balance time vs space complexity trade-offs

**Optimization Categories Covered:**
- ✅ Algorithm time complexity improvements
- ✅ Memory usage optimization
- ✅ Resource management and cleanup
- ✅ Database query optimization
- ✅ I/O operation efficiency

**Performance Improvements Expected:**
- 10x-100x faster algorithms (O(n²) → O(n log n))
- 50-90% memory usage reduction
- Elimination of resource leaks
- 5-10x faster database operations

**Completion Time:** 10 minutes  
**Next:** Module 5 - Security and Best Practices