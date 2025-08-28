# Exercise 2: Code Quality Enhancement

## Objective
Master Amazon Q's code quality improvement capabilities through systematic refactoring and best practices implementation.

**Time:** 7 minutes  
**Difficulty:** Intermediate

---

## Setup Instructions

### Create Code Quality Workspace
```bash
mkdir code-quality-improvement
cd code-quality-improvement
```

---

## Part A: Code Structure and Design Improvements (3 minutes)

### Task A1: Refactoring Poor Code Structure

**Create file:** `legacy_code.py`
```python
import json
import requests
import sqlite3
from datetime import datetime

# Global variables (poor practice)
db_connection = None
api_cache = {}
user_sessions = {}

def process_orders(orders):
    # Long function with multiple responsibilities
    results = []
    total_revenue = 0
    processed_count = 0
    error_count = 0
    
    for order in orders:
        try:
            # Nested conditions and complex logic
            if order['status'] == 'pending':
                if order['payment_method'] == 'credit_card':
                    if order['amount'] > 0:
                        if validate_credit_card(order['card_number']):
                            # Process credit card payment
                            payment_result = charge_credit_card(
                                order['card_number'], 
                                order['amount'],
                                order['cvv'],
                                order['expiry']
                            )
                            if payment_result['success']:
                                order['status'] = 'paid'
                                order['payment_id'] = payment_result['transaction_id']
                                total_revenue += order['amount']
                                processed_count += 1
                                
                                # Update inventory
                                for item in order['items']:
                                    update_inventory(item['product_id'], item['quantity'])
                                
                                # Send confirmation email
                                send_email(order['customer_email'], 'Order Confirmed', 
                                         f"Your order #{order['id']} has been confirmed")
                                
                                # Log transaction
                                log_transaction(order['id'], order['amount'], 'success')
                            else:
                                order['status'] = 'payment_failed'
                                error_count += 1
                                log_transaction(order['id'], order['amount'], 'failed')
                        else:
                            order['status'] = 'invalid_card'
                            error_count += 1
                    else:
                        order['status'] = 'invalid_amount'
                        error_count += 1
                elif order['payment_method'] == 'paypal':
                    # Similar nested logic for PayPal
                    paypal_result = process_paypal_payment(order['paypal_email'], order['amount'])
                    if paypal_result:
                        order['status'] = 'paid'
                        total_revenue += order['amount']
                        processed_count += 1
                    else:
                        order['status'] = 'payment_failed'
                        error_count += 1
                elif order['payment_method'] == 'bank_transfer':
                    # Bank transfer logic
                    order['status'] = 'awaiting_transfer'
                    processed_count += 1
            elif order['status'] == 'cancelled':
                # Refund logic
                if order.get('payment_id'):
                    refund_result = process_refund(order['payment_id'], order['amount'])
                    if refund_result:
                        order['status'] = 'refunded'
                    else:
                        order['status'] = 'refund_failed'
                        error_count += 1
            
            results.append(order)
            
        except Exception as e:
            print(f"Error processing order {order.get('id', 'unknown')}: {str(e)}")
            error_count += 1
    
    # Generate report
    report = {
        'total_orders': len(orders),
        'processed_orders': processed_count,
        'failed_orders': error_count,
        'total_revenue': total_revenue,
        'processing_date': datetime.now().isoformat()
    }
    
    # Save report to database
    save_report_to_db(report)
    
    return {
        'orders': results,
        'report': report
    }

def get_user_data(user_id):
    # Multiple data sources, no error handling
    user_info = fetch_user_from_db(user_id)
    user_preferences = fetch_user_preferences(user_id)
    user_orders = fetch_user_orders(user_id)
    user_payments = fetch_user_payments(user_id)
    
    # Data transformation without validation
    full_user_data = {
        'id': user_info['id'],
        'name': user_info['first_name'] + ' ' + user_info['last_name'],
        'email': user_info['email'],
        'phone': user_info['phone'],
        'address': user_info['address'],
        'preferences': user_preferences,
        'order_history': user_orders,
        'payment_methods': user_payments,
        'total_spent': sum([order['amount'] for order in user_orders]),
        'order_count': len(user_orders),
        'last_order_date': max([order['date'] for order in user_orders]) if user_orders else None
    }
    
    return full_user_data

def calculate_shipping_cost(order):
    # Complex calculation with hardcoded values
    base_cost = 5.99
    weight_factor = 0.5
    distance_factor = 0.1
    
    total_weight = 0
    for item in order['items']:
        product = get_product_details(item['product_id'])
        total_weight += product['weight'] * item['quantity']
    
    # Hardcoded shipping zones
    if order['shipping_address']['country'] == 'US':
        if order['shipping_address']['state'] in ['CA', 'NY', 'TX']:
            zone_multiplier = 1.0
        elif order['shipping_address']['state'] in ['FL', 'IL', 'PA']:
            zone_multiplier = 1.2
        else:
            zone_multiplier = 1.5
    elif order['shipping_address']['country'] == 'CA':
        zone_multiplier = 1.8
    elif order['shipping_address']['country'] in ['UK', 'DE', 'FR']:
        zone_multiplier = 2.5
    else:
        zone_multiplier = 3.0
    
    # Express shipping
    if order.get('express_shipping', False):
        express_multiplier = 2.0
    else:
        express_multiplier = 1.0
    
    shipping_cost = (base_cost + (total_weight * weight_factor)) * zone_multiplier * express_multiplier
    
    # Free shipping threshold
    if order['subtotal'] > 100:
        shipping_cost = 0
    
    return round(shipping_cost, 2)

class DataProcessor:
    # Class with too many responsibilities
    def __init__(self):
        self.db_connection = sqlite3.connect('app.db')
        self.api_client = requests.Session()
        self.cache = {}
        self.processed_items = []
        self.error_log = []
    
    def process_data_file(self, filename):
        # File processing
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Data validation
        validated_data = []
        for item in data:
            if self.validate_item(item):
                validated_data.append(item)
            else:
                self.error_log.append(f"Invalid item: {item}")
        
        # Data transformation
        transformed_data = []
        for item in validated_data:
            transformed_item = self.transform_item(item)
            transformed_data.append(transformed_item)
        
        # Data enrichment
        enriched_data = []
        for item in transformed_data:
            enriched_item = self.enrich_item(item)
            enriched_data.append(enriched_item)
        
        # Save to database
        for item in enriched_data:
            self.save_to_db(item)
        
        # Generate report
        report = self.generate_report(enriched_data)
        
        return {
            'processed_count': len(enriched_data),
            'error_count': len(self.error_log),
            'report': report
        }
    
    def validate_item(self, item):
        # Validation logic
        required_fields = ['id', 'name', 'type', 'value']
        return all(field in item for field in required_fields)
    
    def transform_item(self, item):
        # Transformation logic
        return {
            'id': item['id'],
            'name': item['name'].upper(),
            'type': item['type'].lower(),
            'value': float(item['value']),
            'processed_at': datetime.now().isoformat()
        }
    
    def enrich_item(self, item):
        # API call for enrichment
        if item['id'] not in self.cache:
            response = self.api_client.get(f'https://api.example.com/items/{item["id"]}')
            if response.status_code == 200:
                self.cache[item['id']] = response.json()
        
        enrichment_data = self.cache.get(item['id'], {})
        item.update(enrichment_data)
        return item
    
    def save_to_db(self, item):
        # Database save
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO items (id, name, type, value, data) VALUES (?, ?, ?, ?, ?)",
            (item['id'], item['name'], item['type'], item['value'], json.dumps(item))
        )
        self.db_connection.commit()
    
    def generate_report(self, data):
        # Report generation
        return {
            'total_items': len(data),
            'average_value': sum(item['value'] for item in data) / len(data),
            'types': list(set(item['type'] for item in data))
        }

# Helper functions with poor implementation
def validate_credit_card(card_number):
    return len(card_number) == 16 and card_number.isdigit()

def charge_credit_card(card_number, amount, cvv, expiry):
    # Simulated payment processing
    return {'success': True, 'transaction_id': 'txn_123'}

def process_paypal_payment(email, amount):
    return True

def process_refund(payment_id, amount):
    return True

def update_inventory(product_id, quantity):
    pass

def send_email(to_email, subject, body):
    pass

def log_transaction(order_id, amount, status):
    pass

def save_report_to_db(report):
    pass

def fetch_user_from_db(user_id):
    return {'id': user_id, 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'phone': '123-456-7890', 'address': '123 Main St'}

def fetch_user_preferences(user_id):
    return {'theme': 'dark', 'notifications': True}

def fetch_user_orders(user_id):
    return [{'id': 1, 'amount': 100, 'date': '2023-01-01'}]

def fetch_user_payments(user_id):
    return [{'type': 'credit_card', 'last_four': '1234'}]

def get_product_details(product_id):
    return {'weight': 1.5, 'name': 'Product'}
```

**Amazon Q Code Quality Tasks:**

1. **Structural Analysis:**
```
@legacy_code.py Analyze this code for structural issues and suggest refactoring to improve maintainability and readability
```

2. **Single Responsibility Principle:**
```
Identify functions and classes that violate the Single Responsibility Principle and suggest how to break them down
```

3. **Design Pattern Application:**
```
Suggest appropriate design patterns that could improve this code structure
```

4. **Error Handling Improvement:**
```
Add comprehensive error handling and input validation throughout the code
```

**Expected Improvements:**
- Break down large functions into smaller, focused functions
- Apply Single Responsibility Principle
- Implement proper error handling
- Remove global variables
- Add input validation
- Use design patterns (Strategy, Factory, etc.)
- Improve naming conventions
- Add proper documentation

### Task A2: Object-Oriented Design Improvements

**Amazon Q OOP Enhancement Tasks:**

1. **Class Design:**
```
Refactor the DataProcessor class to follow SOLID principles and proper separation of concerns
```

2. **Inheritance and Composition:**
```
Design a proper class hierarchy for the payment processing system using inheritance and composition
```

3. **Interface Design:**
```
Create interfaces/abstract classes for the payment processors to enable polymorphism
```

---

## Part B: Testing and Documentation Enhancement (4 minutes)

### Task B1: Test Generation and Coverage

**Amazon Q Testing Tasks:**

1. **Unit Test Generation:**
```
Generate comprehensive unit tests for the refactored code with edge cases, error conditions, and mock dependencies
```

2. **Integration Test Creation:**
```
Create integration tests for the order processing workflow that test the interaction between components
```

3. **Test Data Generation:**
```
Generate realistic test data for testing the order processing and user data functions
```

**Expected Test Structure:**
```python
import unittest
from unittest.mock import Mock, patch
import pytest

class TestOrderProcessor(unittest.TestCase):
    def setUp(self):
        self.order_processor = OrderProcessor()
    
    def test_process_valid_order(self):
        # Test with valid order data
        pass
    
    def test_process_invalid_payment_method(self):
        # Test error handling for invalid payment methods
        pass
    
    def test_process_order_with_insufficient_funds(self):
        # Test payment failure scenarios
        pass
    
    @patch('payment_gateway.charge_credit_card')
    def test_credit_card_processing(self, mock_charge):
        # Test credit card processing with mocked payment gateway
        pass
```

### Task B2: Documentation and Type Hints

**Amazon Q Documentation Tasks:**

1. **Comprehensive Documentation:**
```
Add detailed docstrings to all functions and classes following Google or NumPy documentation style
```

2. **Type Hints Addition:**
```
Add comprehensive type hints to all function parameters and return values
```

3. **API Documentation:**
```
Generate API documentation for the refactored classes and methods
```

**Expected Documentation Style:**
```python
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

@dataclass
class Order:
    """Represents a customer order with payment and shipping information.
    
    Attributes:
        id: Unique order identifier
        customer_email: Customer's email address
        items: List of ordered items
        payment_method: Payment method (credit_card, paypal, bank_transfer)
        amount: Total order amount in dollars
        status: Current order status
    """
    id: str
    customer_email: str
    items: List[Dict[str, Union[str, int, float]]]
    payment_method: str
    amount: float
    status: str = 'pending'

class OrderProcessor:
    """Handles order processing including payment and inventory management.
    
    This class provides methods to process orders through various payment
    methods while maintaining inventory and generating transaction logs.
    """
    
    def process_order(self, order: Order) -> Dict[str, Union[bool, str, float]]:
        """Process a single order through the payment system.
        
        Args:
            order: Order object containing all order details
            
        Returns:
            Dictionary containing processing results with keys:
            - success: Boolean indicating if processing succeeded
            - transaction_id: Payment transaction identifier (if successful)
            - error_message: Error description (if failed)
            
        Raises:
            ValueError: If order data is invalid
            PaymentError: If payment processing fails
            InventoryError: If insufficient inventory
            
        Example:
            >>> processor = OrderProcessor()
            >>> order = Order(id="123", customer_email="user@example.com", ...)
            >>> result = processor.process_order(order)
            >>> print(result['success'])
            True
        """
        pass
```

### Task B3: Code Quality Metrics and Standards

**Amazon Q Quality Assessment Tasks:**

1. **Code Quality Checklist:**
```
Create a comprehensive code quality checklist based on the improvements made to this legacy code
```

2. **Performance Analysis:**
```
Analyze the refactored code for performance improvements and suggest optimizations
```

3. **Security Review:**
```
Review the refactored code for security best practices and potential vulnerabilities
```

**Expected Quality Improvements:**
- Cyclomatic complexity reduction
- Improved code coverage
- Better error handling
- Enhanced readability
- Proper separation of concerns
- Comprehensive documentation
- Type safety improvements
- Performance optimizations

---

## Code Quality Assessment Framework

### Readability Metrics
- [ ] Clear and descriptive variable names
- [ ] Consistent code formatting
- [ ] Appropriate function and class sizes
- [ ] Logical code organization
- [ ] Meaningful comments and documentation

### Maintainability Metrics
- [ ] Low cyclomatic complexity
- [ ] High cohesion within modules
- [ ] Low coupling between modules
- [ ] Proper error handling
- [ ] Comprehensive test coverage

### Performance Metrics
- [ ] Efficient algorithms and data structures
- [ ] Proper resource management
- [ ] Minimal memory usage
- [ ] Optimized database queries
- [ ] Appropriate caching strategies

### Security Metrics
- [ ] Input validation and sanitization
- [ ] Proper authentication and authorization
- [ ] Secure data handling
- [ ] Protection against common vulnerabilities
- [ ] Secure configuration management

---

## Refactoring Checklist

### Before Refactoring
- [ ] Understand existing functionality
- [ ] Identify code smells and issues
- [ ] Create comprehensive tests
- [ ] Document current behavior
- [ ] Plan refactoring approach

### During Refactoring
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Maintain existing functionality
- [ ] Improve code structure gradually
- [ ] Add documentation as you go

### After Refactoring
- [ ] Verify all tests pass
- [ ] Check performance impact
- [ ] Review security implications
- [ ] Update documentation
- [ ] Conduct code review

---

## Success Criteria

You've mastered code quality enhancement when you can:
- [ ] Identify and fix structural code issues
- [ ] Apply SOLID principles effectively
- [ ] Generate comprehensive tests and documentation
- [ ] Implement proper error handling
- [ ] Create maintainable and readable code
- [ ] Use appropriate design patterns

**Quality Improvement Areas:**
- ✅ Code structure and organization
- ✅ Error handling and validation
- ✅ Testing and documentation
- ✅ Performance optimization
- ✅ Security best practices
- ✅ Design pattern application

**Completion Time:** 7 minutes  
**Next:** Module 6 - Advanced Features and Integration