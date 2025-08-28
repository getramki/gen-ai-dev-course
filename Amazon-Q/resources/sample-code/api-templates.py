# Sample API Templates for Module 2 Exercises

from flask import Flask, request, jsonify
from datetime import datetime
import json
import csv
import pandas as pd

app = Flask(__name__)

# Sample data structures for exercises
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30, "department": "Engineering"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 25, "department": "Marketing"},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "age": 35, "department": "Engineering"}
]

products = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 1200, "stock": 5},
    {"id": 2, "name": "Phone", "category": "Electronics", "price": 800, "stock": 10},
    {"id": 3, "name": "Python Guide", "category": "Books", "price": 45, "stock": 20},
    {"id": 4, "name": "Desk Chair", "category": "Furniture", "price": 250, "stock": 8}
]

# Basic REST API template - students will expand this using Amazon Q completions
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# Template for user management endpoints
@app.route('/users', methods=['GET'])
def get_users():
    """Get all users - to be completed with Amazon Q"""
    pass

@app.route('/users', methods=['POST'])
def create_user():
    """Create new user - to be completed with Amazon Q"""
    pass

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user - to be completed with Amazon Q"""
    pass

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user - to be completed with Amazon Q"""
    pass

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user - to be completed with Amazon Q"""
    pass

# Template for product management endpoints
@app.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional category filter"""
    pass

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product"""
    pass

# Utility functions for data processing exercises
def load_csv_data(filename):
    """Template for CSV loading - to be completed with Amazon Q"""
    pass

def process_employee_data(data):
    """Template for employee data processing - to be completed with Amazon Q"""
    pass

def transform_product_data(products):
    """Template for product data transformation - to be completed with Amazon Q"""
    pass

# Validation class template
class DataValidator:
    """Template for data validation - to be completed with Amazon Q"""
    
    def validate_email(self, email):
        """Email validation method"""
        pass
    
    def validate_password(self, password):
        """Password strength validation"""
        pass
    
    def validate_age(self, age):
        """Age range validation"""
        pass
    
    def validate_user_data(self, user_data):
        """Complete user data validation"""
        pass

# Algorithm templates
def binary_search_dict(data, key, value):
    """Binary search in list of dictionaries - to be completed with Amazon Q"""
    pass

def custom_sort_students(students):
    """Custom sorting algorithm - to be completed with Amazon Q"""
    pass

def quicksort_implementation(arr):
    """Quicksort algorithm - to be completed with Amazon Q"""
    pass

# Configuration manager template
class ConfigManager:
    """Configuration management class - to be completed with Amazon Q"""
    
    def __init__(self, config_file):
        """Initialize with config file"""
        pass
    
    def get(self, key_path):
        """Get configuration value using dot notation"""
        pass
    
    def set(self, key_path, value):
        """Set configuration value using dot notation"""
        pass
    
    def save(self):
        """Save configuration to file"""
        pass
    
    def validate_required_fields(self, required_fields):
        """Validate required configuration fields"""
        pass

if __name__ == '__main__':
    app.run(debug=True)

# Sample test data for exercises
sample_employees = [
    {"name": "Alice Johnson", "department": "Engineering", "salary": 75000, "years_experience": 7},
    {"name": "Bob Smith", "department": "Marketing", "salary": 65000, "years_experience": 4},
    {"name": "Carol Davis", "department": "Engineering", "salary": 85000, "years_experience": 10},
    {"name": "David Wilson", "department": "Sales", "salary": 60000, "years_experience": 6},
    {"name": "Eve Brown", "department": "Marketing", "salary": 70000, "years_experience": 8}
]

sample_students = [
    {"name": "John", "grade": 85},
    {"name": "Alice", "grade": 92},
    {"name": "Bob"},  # Missing grade
    {"name": "Carol", "grade": 85},
    {"name": "David", "grade": 78}
]

sample_config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp",
        "username": "admin"
    },
    "api": {
        "version": "v1",
        "rate_limit": 1000,
        "timeout": 30
    },
    "features": {
        "authentication": True,
        "logging": True,
        "caching": False
    }
}