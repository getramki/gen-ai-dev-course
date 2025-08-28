# Module 2 Exercise Solutions
# These are reference implementations for instructors

from flask import Flask, request, jsonify
import pandas as pd
import csv
import json
import re
from typing import List, Dict, Optional, Any
from datetime import datetime

app = Flask(__name__)

# Global data storage
users = []
user_id_counter = 1

# Exercise 1 Solution: Complete REST API
@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    # Email validation
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    user = {
        'id': user_id_counter,
        'name': data['name'],
        'email': data['email'],
        'age': data.get('age', 0),
        'created_at': datetime.now().isoformat()
    }
    
    users.append(user)
    user_id_counter += 1
    
    return jsonify(user), 201

@app.route('/users', methods=['GET'])
def get_users():
    age_filter = request.args.get('min_age', type=int)
    
    if age_filter:
        filtered_users = [user for user in users if user.get('age', 0) >= age_filter]
        return jsonify(filtered_users)
    
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        user['email'] = data['email']
    if 'age' in data:
        user['age'] = data['age']
    
    user['updated_at'] = datetime.now().isoformat()
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    users = [u for u in users if u['id'] != user_id]
    return jsonify({'message': 'User deleted successfully'}), 200

# Exercise 2 Solutions: Natural Language Generation

# Task A1: CSV Data Analysis
def analyze_employee_data(csv_file_path: str) -> Dict[str, float]:
    """
    Reads employee CSV data, filters by experience > 5 years,
    returns average salary by department
    """
    try:
        df = pd.read_csv(csv_file_path)
        
        # Filter employees with more than 5 years experience
        experienced = df[df['years_experience'] > 5]
        
        # Calculate average salary by department
        avg_salary_by_dept = experienced.groupby('department')['salary'].mean().to_dict()
        
        return avg_salary_by_dept
    
    except FileNotFoundError:
        raise Exception(f"File {csv_file_path} not found")
    except KeyError as e:
        raise Exception(f"Required column missing: {e}")
    except Exception as e:
        raise Exception(f"Error processing data: {e}")

# Task A2: JSON Data Transformation
def transform_products_by_category(products: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Groups products by category and sorts by price descending within each category
    """
    result = {}
    
    for product in products:
        category = product.get('category', 'Uncategorized')
        
        if category not in result:
            result[category] = []
        
        result[category].append(product)
    
    # Sort each category by price descending
    for category in result:
        result[category].sort(key=lambda x: x.get('price', 0), reverse=True)
    
    return result

# Task B1: Binary Search Algorithm
def binary_search_dict(data: List[Dict], key: str, value: Any) -> int:
    """
    Binary search in sorted list of dictionaries by specified key
    Returns index of found item or -1 if not found
    """
    left, right = 0, len(data) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_value = data[mid].get(key)
        
        if mid_value == value:
            return mid
        elif mid_value < value:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Task B2: Custom Sorting
def sort_students(students: List[Dict]) -> List[Dict]:
    """
    Sorts students by grade (descending), then by name (ascending)
    Treats missing grades as 0
    """
    def sort_key(student):
        grade = student.get('grade', 0)
        name = student.get('name', '')
        return (-grade, name)  # Negative grade for descending order
    
    return sorted(students, key=sort_key)

# Task C1: Data Validation Class
class UserValidator:
    """Validates user registration data with detailed error messages"""
    
    def validate_email(self, email: str) -> tuple[bool, str]:
        """Validate email format using regex"""
        if not email:
            return False, "Email is required"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, ""
    
    def validate_password(self, password: str) -> tuple[bool, str]:
        """Validate password strength"""
        if not password:
            return False, "Password is required"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        return True, ""
    
    def validate_age(self, age: int) -> tuple[bool, str]:
        """Validate age range"""
        if age is None:
            return False, "Age is required"
        
        if not isinstance(age, int):
            return False, "Age must be a number"
        
        if age < 18:
            return False, "Age must be at least 18"
        
        if age > 120:
            return False, "Age must be less than 120"
        
        return True, ""
    
    def validate(self, user_data: Dict) -> Dict[str, Any]:
        """Validate complete user data"""
        errors = []
        
        # Validate email
        email_valid, email_error = self.validate_email(user_data.get('email', ''))
        if not email_valid:
            errors.append(email_error)
        
        # Validate password
        password_valid, password_error = self.validate_password(user_data.get('password', ''))
        if not password_valid:
            errors.append(password_error)
        
        # Validate age
        age_valid, age_error = self.validate_age(user_data.get('age'))
        if not age_valid:
            errors.append(age_error)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

# Task C2: Configuration Manager
class ConfigManager:
    """Manages configuration with dot notation support and file persistence"""
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = {}
        self.load()
    
    def load(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in config file: {e}")
    
    def get(self, key_path: str, default=None):
        """Get configuration value using dot notation"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to parent of target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the final value
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            raise Exception(f"Error saving config: {e}")
    
    def validate_required_fields(self, required_fields: List[str]) -> Dict[str, Any]:
        """Validate that required fields exist"""
        missing_fields = []
        
        for field in required_fields:
            if self.get(field) is None:
                missing_fields.append(field)
        
        return {
            'valid': len(missing_fields) == 0,
            'missing_fields': missing_fields
        }

# Additional utility functions for testing
def create_sample_csv():
    """Create sample CSV file for testing"""
    data = [
        ["name", "department", "salary", "years_experience"],
        ["Alice Johnson", "Engineering", "75000", "7"],
        ["Bob Smith", "Marketing", "65000", "4"],
        ["Carol Davis", "Engineering", "85000", "10"],
        ["David Wilson", "Sales", "60000", "6"],
        ["Eve Brown", "Marketing", "70000", "8"]
    ]
    
    with open('employees.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def test_all_functions():
    """Test all implemented functions"""
    print("Testing Module 2 Solutions...")
    
    # Test CSV analysis
    create_sample_csv()
    result = analyze_employee_data('employees.csv')
    print(f"Average salary by department: {result}")
    
    # Test product transformation
    products = [
        {"id": 1, "name": "Laptop", "category": "Electronics", "price": 1200, "stock": 5},
        {"id": 2, "name": "Phone", "category": "Electronics", "price": 800, "stock": 10},
        {"id": 3, "name": "Python Guide", "category": "Books", "price": 45, "stock": 20}
    ]
    transformed = transform_products_by_category(products)
    print(f"Products by category: {transformed}")
    
    # Test binary search
    data = [{"id": 1}, {"id": 3}, {"id": 5}, {"id": 7}]
    index = binary_search_dict(data, "id", 5)
    print(f"Binary search result: {index}")
    
    # Test student sorting
    students = [
        {"name": "John", "grade": 85},
        {"name": "Alice", "grade": 92},
        {"name": "Bob"},
        {"name": "Carol", "grade": 85}
    ]
    sorted_students = sort_students(students)
    print(f"Sorted students: {sorted_students}")
    
    # Test validation
    validator = UserValidator()
    result = validator.validate({
        "email": "test@example.com",
        "password": "SecurePass123",
        "age": 25
    })
    print(f"Validation result: {result}")

if __name__ == '__main__':
    test_all_functions()
    app.run(debug=True)