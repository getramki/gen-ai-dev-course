# Buggy Code Examples for Module 4 Debugging Exercises

import threading
import time
import json
from datetime import datetime

# Logic Errors Collection
class LogicErrorExamples:
    """Collection of functions with logic errors for debugging practice"""
    
    @staticmethod
    def calculate_average(numbers):
        """Bug: Division by zero with empty list"""
        total = 0
        for num in numbers:
            total += num
        return total / len(numbers)  # Crashes with empty list
    
    @staticmethod
    def find_maximum(arr):
        """Bug: Fails with all negative numbers"""
        max_val = 0  # Should initialize with first element or negative infinity
        for num in arr:
            if num > max_val:
                max_val = num
        return max_val
    
    @staticmethod
    def binary_search(arr, target):
        """Bug: Off-by-one error in boundary"""
        left, right = 0, len(arr)  # Should be len(arr) - 1
        while left < right:  # Should be left <= right
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    @staticmethod
    def reverse_words(sentence):
        """Bug: Misses last word in reversal"""
        words = sentence.split(' ')
        reversed_words = []
        for i in range(len(words) - 1, 0, -1):  # Should be -1, not 0
            reversed_words.append(words[i])
        return ' '.join(reversed_words)
    
    @staticmethod
    def factorial(n):
        """Bug: No handling for negative numbers, potential stack overflow"""
        if n == 0:
            return 1
        return n * LogicErrorExamples.factorial(n - 1)  # No check for n < 0
    
    @staticmethod
    def is_palindrome(s):
        """Bug: Case sensitivity and space handling issues"""
        return s == s[::-1]  # Should handle case and spaces
    
    @staticmethod
    def count_vowels(text):
        """Bug: Only counts lowercase vowels"""
        vowels = 'aeiou'  # Missing uppercase vowels
        count = 0
        for char in text:
            if char in vowels:
                count += 1
        return count

# Runtime Error Examples
class RuntimeErrorExamples:
    """Collection of functions prone to runtime errors"""
    
    @staticmethod
    def process_user_data(users):
        """Multiple potential KeyError and TypeError issues"""
        results = []
        for user in users:
            # KeyError if keys missing
            full_name = user['first_name'] + ' ' + user['last_name']
            age_next_year = user['age'] + 1  # TypeError if age is string
            email_domain = user['email'].split('@')[1]  # IndexError if no @
            
            results.append({
                'name': full_name,
                'age_next_year': age_next_year,
                'domain': email_domain
            })
        return results
    
    @staticmethod
    def divide_numbers(numbers):
        """ZeroDivisionError potential"""
        results = []
        for i in range(len(numbers) - 1):
            result = numbers[i] / numbers[i + 1]  # Division by zero
            results.append(result)
        return results
    
    @staticmethod
    def access_nested_data(data):
        """Multiple potential KeyError and AttributeError"""
        # Will fail if any key in chain is missing
        user_theme = data['user']['profile']['settings']['theme']
        last_login = data['user']['activity']['last_login']
        preferences = data['user']['profile']['preferences']['notifications']
        
        return {
            'theme': user_theme,
            'last_login': last_login,
            'notifications': preferences
        }
    
    @staticmethod
    def process_file_lines(filename):
        """FileNotFoundError and IndexError potential"""
        with open(filename, 'r') as f:  # FileNotFoundError
            lines = f.readlines()
        
        first_line = lines[0]  # IndexError if file empty
        header_columns = first_line.split(',')
        first_column = header_columns[0]  # IndexError if no commas
        
        return {
            'total_lines': len(lines),
            'first_column': first_column
        }
    
    @staticmethod
    def parse_json_data(json_string):
        """JSON decode errors"""
        data = json.loads(json_string)  # JSONDecodeError
        
        # Assumes specific structure
        items = data['items']
        first_item = items[0]
        item_name = first_item['name']
        
        return item_name

# Performance Issues Examples
class PerformanceIssues:
    """Collection of performance-problematic code"""
    
    @staticmethod
    def slow_fibonacci(n):
        """Exponential time complexity - very slow for n > 35"""
        if n <= 1:
            return n
        return PerformanceIssues.slow_fibonacci(n-1) + PerformanceIssues.slow_fibonacci(n-2)
    
    @staticmethod
    def inefficient_duplicate_finder(arr):
        """O(n²) time complexity"""
        duplicates = []
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] == arr[j] and arr[i] not in duplicates:
                    duplicates.append(arr[i])
        return duplicates
    
    @staticmethod
    def memory_wasting_processor(data):
        """Creates unnecessary copies of large data"""
        # Step 1: Create copy
        filtered_data = []
        for item in data:
            if item.get('active', False):
                filtered_data.append(item)
        
        # Step 2: Create another copy
        processed_data = []
        for item in filtered_data:
            processed_item = {
                'id': item['id'],
                'name': item['name'].upper(),
                'score': item.get('score', 0) * 2
            }
            processed_data.append(processed_item)
        
        # Step 3: Create final copy
        sorted_data = sorted(processed_data, key=lambda x: x['score'])
        
        return sorted_data
    
    @staticmethod
    def string_concatenation_slow(words):
        """Inefficient string building"""
        result = ""
        for word in words:
            result = result + word + " "  # Creates new string each time
        return result.strip()
    
    @staticmethod
    def nested_loop_search(data, targets):
        """O(n*m) when could be O(n + m)"""
        found_items = []
        for target in targets:
            for item in data:
                if item['id'] == target:
                    found_items.append(item)
                    break
        return found_items

# Concurrency Issues Examples
class ConcurrencyBugs:
    """Collection of thread-safety issues"""
    
    def __init__(self):
        self.counter = 0
        self.shared_list = []
        self.balance = 1000
    
    def unsafe_increment(self):
        """Race condition in counter increment"""
        temp = self.counter
        time.sleep(0.0001)  # Simulate processing
        self.counter = temp + 1
    
    def unsafe_list_operations(self, worker_id):
        """Race condition in list operations"""
        for i in range(100):
            # Multiple threads modifying same list
            self.shared_list.append(f"worker_{worker_id}_item_{i}")
            
            if len(self.shared_list) > 50:
                self.shared_list.pop(0)  # Race condition here
    
    def unsafe_bank_operations(self, amount):
        """Race condition in balance updates"""
        if self.balance >= amount:
            current_balance = self.balance
            time.sleep(0.001)  # Simulate processing time
            self.balance = current_balance - amount
            return True
        return False
    
    @staticmethod
    def deadlock_example():
        """Potential deadlock scenario"""
        lock1 = threading.Lock()
        lock2 = threading.Lock()
        
        def worker1():
            with lock1:
                print("Worker 1 acquired lock1")
                time.sleep(0.1)
                with lock2:
                    print("Worker 1 acquired lock2")
        
        def worker2():
            with lock2:
                print("Worker 2 acquired lock2")
                time.sleep(0.1)
                with lock1:
                    print("Worker 2 acquired lock1")
        
        thread1 = threading.Thread(target=worker1)
        thread2 = threading.Thread(target=worker2)
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()

# Memory Leak Examples
class MemoryLeaks:
    """Examples of memory management issues"""
    
    def __init__(self):
        self.cache = {}
        self.connections = []
    
    def leaky_cache(self, key, expensive_operation):
        """Cache that never clears - memory leak"""
        if key not in self.cache:
            self.cache[key] = expensive_operation()  # Cache grows indefinitely
        return self.cache[key]
    
    def unclosed_resources(self, filenames):
        """File handles not properly closed"""
        file_contents = {}
        for filename in filenames:
            try:
                f = open(filename, 'r')  # File never closed
                content = f.read()
                file_contents[filename] = content
            except FileNotFoundError:
                file_contents[filename] = None
        return file_contents
    
    def circular_references(self):
        """Objects with circular references"""
        class Node:
            def __init__(self, value):
                self.value = value
                self.parent = None
                self.children = []
            
            def add_child(self, child):
                child.parent = self  # Circular reference
                self.children.append(child)
        
        # Create circular reference structure
        root = Node("root")
        child1 = Node("child1")
        child2 = Node("child2")
        
        root.add_child(child1)
        root.add_child(child2)
        child1.add_child(root)  # Creates cycle
        
        return root

# Integration and API Errors
class IntegrationErrors:
    """Examples of integration and API-related bugs"""
    
    @staticmethod
    def unreliable_api_call(url, retries=0):
        """API calls without proper error handling"""
        import requests
        
        response = requests.get(url)  # No timeout, no error handling
        data = response.json()  # Assumes JSON response
        
        return data['results'][0]['value']  # Assumes specific structure
    
    @staticmethod
    def database_connection_leak():
        """Database connections not properly managed"""
        import sqlite3
        
        conn = sqlite3.connect('example.db')  # Connection never closed
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        results = cursor.fetchall()
        
        return results  # Connection and cursor never closed
    
    @staticmethod
    def configuration_errors():
        """Configuration and environment issues"""
        import os
        
        # Assumes environment variables exist
        api_key = os.environ['API_KEY']  # KeyError if not set
        database_url = os.environ['DATABASE_URL']  # KeyError if not set
        
        # Assumes file exists
        with open('config.json', 'r') as f:  # FileNotFoundError
            config = json.load(f)
        
        return {
            'api_key': api_key,
            'database_url': database_url,
            'config': config
        }

# Test Data Generators
class TestDataGenerator:
    """Generate test data to trigger bugs"""
    
    @staticmethod
    def problematic_user_data():
        """Generate user data that triggers various errors"""
        return [
            # Valid user
            {'first_name': 'John', 'last_name': 'Doe', 'age': 30, 'email': 'john@example.com'},
            
            # Missing last_name
            {'first_name': 'Jane', 'age': 25, 'email': 'jane@example.com'},
            
            # Age as string
            {'first_name': 'Bob', 'last_name': 'Smith', 'age': '35', 'email': 'bob@example.com'},
            
            # Invalid email
            {'first_name': 'Alice', 'last_name': 'Johnson', 'age': 28, 'email': 'invalid-email'},
            
            # Missing email
            {'first_name': 'Charlie', 'last_name': 'Brown', 'age': 40},
        ]
    
    @staticmethod
    def edge_case_arrays():
        """Generate arrays that trigger edge cases"""
        return {
            'empty': [],
            'single_element': [42],
            'all_negative': [-5, -2, -10, -1],
            'with_zeros': [1, 0, 3, 0, 5],
            'duplicates': [1, 2, 2, 3, 3, 3],
            'large_numbers': [10**9, 10**10, 10**11],
            'mixed_types': [1, '2', 3.0, None],  # Will cause TypeError
        }
    
    @staticmethod
    def malformed_json_strings():
        """Generate JSON strings that cause parsing errors"""
        return [
            '{"valid": "json"}',  # Valid
            '{"missing_quote: "value"}',  # Invalid
            '{"trailing_comma": "value",}',  # Invalid
            '{invalid_key: "value"}',  # Invalid
            '{"unclosed": "string}',  # Invalid
            '',  # Empty string
            'not json at all',  # Not JSON
        ]

# Usage Examples for Testing
if __name__ == "__main__":
    # Test logic errors
    print("Testing logic errors:")
    try:
        result = LogicErrorExamples.calculate_average([])
        print(f"Average of empty list: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test runtime errors
    print("\nTesting runtime errors:")
    problematic_users = TestDataGenerator.problematic_user_data()
    try:
        result = RuntimeErrorExamples.process_user_data(problematic_users)
        print(f"Processed users: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test performance issues
    print("\nTesting performance issues:")
    start_time = time.time()
    result = PerformanceIssues.slow_fibonacci(35)  # This will be slow
    end_time = time.time()
    print(f"Fibonacci(35) = {result}, took {end_time - start_time:.2f} seconds")
    
    # Test concurrency issues
    print("\nTesting concurrency issues:")
    bug_demo = ConcurrencyBugs()
    
    threads = []
    for i in range(5):
        thread = threading.Thread(target=bug_demo.unsafe_increment)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"Counter value: {bug_demo.counter} (expected: 5, actual shows race condition)")