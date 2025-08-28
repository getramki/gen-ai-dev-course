# Exercise 2: Documentation Generation

## Objective
Master Amazon Q's documentation generation capabilities for functions, classes, and projects.

**Time:** 13 minutes  
**Difficulty:** Intermediate

---

## Setup Instructions

### Create Documentation Workspace
```bash
mkdir documentation-project
cd documentation-project
```

---

## Part A: Function Documentation (4 minutes)

### Task A1: Financial Calculation Functions

**Create file:** `financial_calculator.py`
```python
import math

def calculate_loan_payment(principal, annual_rate, years, payment_frequency=12):
    if annual_rate == 0:
        return principal / (years * payment_frequency)
    
    monthly_rate = annual_rate / payment_frequency
    total_payments = years * payment_frequency
    
    payment = principal * (monthly_rate * (1 + monthly_rate)**total_payments) / \
              ((1 + monthly_rate)**total_payments - 1)
    
    return round(payment, 2)

def calculate_compound_interest(principal, annual_rate, years, compound_frequency=12):
    amount = principal * (1 + annual_rate/compound_frequency)**(compound_frequency * years)
    return round(amount - principal, 2)

def calculate_roi(initial_investment, final_value, years):
    if initial_investment <= 0:
        raise ValueError("Initial investment must be positive")
    
    roi = ((final_value - initial_investment) / initial_investment) * 100
    annualized_roi = ((final_value / initial_investment)**(1/years) - 1) * 100
    
    return {
        'total_roi': round(roi, 2),
        'annualized_roi': round(annualized_roi, 2)
    }

def calculate_mortgage_amortization(principal, annual_rate, years):
    monthly_rate = annual_rate / 12
    total_payments = years * 12
    monthly_payment = calculate_loan_payment(principal, annual_rate, years, 12)
    
    schedule = []
    remaining_balance = principal
    
    for payment_num in range(1, total_payments + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        
        schedule.append({
            'payment_number': payment_num,
            'payment_amount': monthly_payment,
            'principal_payment': round(principal_payment, 2),
            'interest_payment': round(interest_payment, 2),
            'remaining_balance': round(max(0, remaining_balance), 2)
        })
    
    return schedule
```

**Documentation Tasks:**

1. **Generate Complete Docstrings:**
```
@financial_calculator.py Generate comprehensive docstrings for all functions in this file, including parameters, return values, examples, and mathematical formulas used
```

2. **Add Usage Examples:**
```
Add practical usage examples to each function's documentation showing real-world scenarios
```

3. **Document Mathematical Formulas:**
```
Explain the mathematical formulas used in each calculation function
```

**Expected Output Example:**
```python
def calculate_loan_payment(principal, annual_rate, years, payment_frequency=12):
    """
    Calculate periodic loan payment using the standard loan payment formula.
    
    This function calculates the fixed payment amount for a loan based on
    the principal amount, interest rate, and loan term using the formula:
    
    PMT = P * [r(1+r)^n] / [(1+r)^n - 1]
    
    Where:
    - PMT = Payment amount
    - P = Principal loan amount
    - r = Periodic interest rate (annual_rate / payment_frequency)
    - n = Total number of payments (years * payment_frequency)
    
    Args:
        principal (float): The loan principal amount in dollars
        annual_rate (float): Annual interest rate as a decimal (e.g., 0.05 for 5%)
        years (int): Loan term in years
        payment_frequency (int, optional): Number of payments per year. Defaults to 12 (monthly)
    
    Returns:
        float: The periodic payment amount rounded to 2 decimal places
    
    Raises:
        ValueError: If principal is negative or payment_frequency is zero
    
    Examples:
        >>> calculate_loan_payment(200000, 0.05, 30)
        1073.64
        
        >>> calculate_loan_payment(50000, 0.04, 5, 12)
        920.03
        
        Calculate monthly payment for a $200,000 mortgage at 5% for 30 years:
        >>> monthly_payment = calculate_loan_payment(200000, 0.05, 30)
        >>> print(f"Monthly payment: ${monthly_payment}")
        Monthly payment: $1073.64
    
    Note:
        For zero interest rate loans, the payment is simply the principal
        divided by the total number of payments.
    """
```

### Task A2: Data Validation Functions

**Create file:** `validators.py`
```python
import re
from datetime import datetime
from typing import Union, List, Dict

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone_number(phone, country_code='US'):
    patterns = {
        'US': r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$',
        'UK': r'^\+?44[-.\s]?([0-9]{4})[-.\s]?([0-9]{6})$',
        'CA': r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'
    }
    
    pattern = patterns.get(country_code, patterns['US'])
    return re.match(pattern, phone) is not None

def validate_credit_card(card_number):
    # Remove spaces and dashes
    card_number = re.sub(r'[-\s]', '', card_number)
    
    # Check if all digits
    if not card_number.isdigit():
        return False
    
    # Luhn algorithm
    def luhn_check(card_num):
        digits = [int(d) for d in card_num]
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        return sum(digits) % 10 == 0
    
    return luhn_check(card_number)

def validate_password_strength(password):
    criteria = {
        'length': len(password) >= 8,
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'lowercase': bool(re.search(r'[a-z]', password)),
        'digit': bool(re.search(r'\d', password)),
        'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    }
    
    score = sum(criteria.values())
    strength_levels = {
        0: 'Very Weak',
        1: 'Very Weak', 
        2: 'Weak',
        3: 'Fair',
        4: 'Good',
        5: 'Strong'
    }
    
    return {
        'score': score,
        'strength': strength_levels[score],
        'criteria_met': criteria,
        'is_valid': score >= 4
    }
```

**Documentation Tasks:**
```
@validators.py Generate detailed documentation for these validation functions, including supported formats, validation rules, and return value explanations
```

---

## Part B: Class Documentation (4 minutes)

### Task B1: E-commerce Shopping Cart

**Create file:** `shopping_cart.py`
```python
from datetime import datetime
from typing import Dict, List, Optional
from decimal import Decimal

class ShoppingCart:
    def __init__(self, user_id: str, currency: str = 'USD'):
        self.user_id = user_id
        self.currency = currency
        self.items = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.discount_code = None
        self.discount_amount = Decimal('0.00')
    
    def add_item(self, product_id: str, quantity: int, price: Decimal, 
                 name: str = None, metadata: Dict = None):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        if product_id in self.items:
            self.items[product_id]['quantity'] += quantity
        else:
            self.items[product_id] = {
                'name': name or f"Product {product_id}",
                'quantity': quantity,
                'unit_price': price,
                'metadata': metadata or {}
            }
        
        self.updated_at = datetime.now()
        return self.items[product_id]
    
    def remove_item(self, product_id: str, quantity: Optional[int] = None):
        if product_id not in self.items:
            raise KeyError(f"Product {product_id} not in cart")
        
        if quantity is None:
            del self.items[product_id]
        else:
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            
            current_quantity = self.items[product_id]['quantity']
            if quantity >= current_quantity:
                del self.items[product_id]
            else:
                self.items[product_id]['quantity'] -= quantity
        
        self.updated_at = datetime.now()
    
    def apply_discount(self, discount_code: str, discount_amount: Decimal):
        self.discount_code = discount_code
        self.discount_amount = discount_amount
        self.updated_at = datetime.now()
    
    def calculate_subtotal(self):
        subtotal = Decimal('0.00')
        for item in self.items.values():
            subtotal += item['unit_price'] * item['quantity']
        return subtotal
    
    def calculate_total(self, tax_rate: Decimal = Decimal('0.00')):
        subtotal = self.calculate_subtotal()
        discounted_subtotal = subtotal - self.discount_amount
        tax_amount = discounted_subtotal * tax_rate
        return discounted_subtotal + tax_amount
    
    def get_item_count(self):
        return sum(item['quantity'] for item in self.items.values())
    
    def clear_cart(self):
        self.items.clear()
        self.discount_code = None
        self.discount_amount = Decimal('0.00')
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'currency': self.currency,
            'items': self.items,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'discount_code': self.discount_code,
            'discount_amount': float(self.discount_amount),
            'subtotal': float(self.calculate_subtotal()),
            'item_count': self.get_item_count()
        }
```

**Documentation Tasks:**

1. **Generate Class Documentation:**
```
@shopping_cart.py Generate comprehensive class documentation including class purpose, attributes, methods, and usage examples
```

2. **Document All Methods:**
```
Add detailed docstrings to all methods in the ShoppingCart class with parameters, return values, and exceptions
```

3. **Create Usage Examples:**
```
Generate practical usage examples showing how to use the ShoppingCart class in an e-commerce application
```

---

## Part C: API Documentation (5 minutes)

### Task C1: REST API Endpoints

**Create file:** `api_endpoints.py`
```python
from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Missing required fields',
            'required': required_fields
        }), 400
    
    # Simulate user creation
    user = {
        'id': str(uuid.uuid4()),
        'username': data['username'],
        'email': data['email'],
        'created_at': datetime.now().isoformat(),
        'is_active': True
    }
    
    return jsonify(user), 201

@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # Simulate user lookup
    user = {
        'id': user_id,
        'username': 'john_doe',
        'email': 'john@example.com',
        'created_at': '2023-01-01T00:00:00',
        'is_active': True,
        'profile': {
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'Software developer'
        }
    }
    
    return jsonify(user)

@app.route('/api/v1/users/<user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', None)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    
    # Validate pagination parameters
    if page < 1:
        return jsonify({'error': 'Page must be >= 1'}), 400
    
    if per_page < 1 or per_page > 100:
        return jsonify({'error': 'Per page must be between 1 and 100'}), 400
    
    # Simulate order data
    orders = [
        {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'status': 'completed',
            'total_amount': 99.99,
            'currency': 'USD',
            'created_at': '2023-01-15T10:30:00',
            'items': [
                {
                    'product_id': 'prod_123',
                    'name': 'Widget',
                    'quantity': 2,
                    'unit_price': 49.99
                }
            ]
        }
    ]
    
    # Apply filters
    if status:
        orders = [order for order in orders if order['status'] == status]
    
    return jsonify({
        'orders': orders,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': 1,
            'total_items': len(orders)
        },
        'filters': {
            'status': status,
            'start_date': start_date,
            'end_date': end_date
        }
    })

@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    # Validate order data
    required_fields = ['user_id', 'items']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Missing required fields',
            'required': required_fields
        }), 400
    
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return jsonify({'error': 'Items must be a non-empty array'}), 400
    
    # Validate each item
    for item in data['items']:
        item_required = ['product_id', 'quantity', 'unit_price']
        if not all(field in item for field in item_required):
            return jsonify({
                'error': 'Invalid item format',
                'required_item_fields': item_required
            }), 400
    
    # Calculate total
    total_amount = sum(item['quantity'] * item['unit_price'] for item in data['items'])
    
    # Create order
    order = {
        'id': str(uuid.uuid4()),
        'user_id': data['user_id'],
        'status': 'pending',
        'total_amount': total_amount,
        'currency': data.get('currency', 'USD'),
        'created_at': datetime.now().isoformat(),
        'items': data['items']
    }
    
    return jsonify(order), 201
```

**Documentation Tasks:**

1. **Generate OpenAPI Documentation:**
```
@api_endpoints.py Generate comprehensive OpenAPI/Swagger documentation for all API endpoints including request/response schemas, parameters, and error codes
```

2. **Create API Usage Guide:**
```
Create a detailed API usage guide with authentication, rate limiting, and example requests for each endpoint
```

3. **Document Error Responses:**
```
Document all possible error responses, status codes, and error message formats for the API
```

**Expected Documentation Structure:**
```yaml
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0
  description: RESTful API for user and order management

paths:
  /api/v1/users:
    post:
      summary: Create a new user
      description: Creates a new user account with the provided information
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - username
                - email
                - password
              properties:
                username:
                  type: string
                  description: Unique username for the account
                  example: "john_doe"
                email:
                  type: string
                  format: email
                  description: User's email address
                  example: "john@example.com"
                password:
                  type: string
                  description: User's password (minimum 8 characters)
                  example: "SecurePass123"
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Invalid input data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
```

---

## Project Documentation Task

### Task: Complete Project README

**Create file:** `README.md`

**Ask Amazon Q:**
```
Generate a comprehensive README.md file for this financial calculator and e-commerce project, including installation instructions, usage examples, API documentation, and contribution guidelines
```

**Expected Sections:**
- Project description and features
- Installation and setup instructions
- Usage examples and tutorials
- API documentation links
- Testing instructions
- Contributing guidelines
- License information

---

## Documentation Quality Checklist

### Function Documentation
- [ ] Clear purpose description
- [ ] All parameters documented with types
- [ ] Return values explained
- [ ] Exceptions and error conditions listed
- [ ] Practical usage examples included
- [ ] Mathematical formulas explained (if applicable)

### Class Documentation
- [ ] Class purpose and responsibilities
- [ ] All attributes documented
- [ ] Method descriptions with parameters/returns
- [ ] Usage patterns and examples
- [ ] Inheritance relationships explained

### API Documentation
- [ ] All endpoints documented
- [ ] Request/response formats specified
- [ ] Authentication requirements
- [ ] Error codes and messages
- [ ] Rate limiting information
- [ ] Example requests and responses

---

## Success Criteria

You've mastered documentation generation when you can:
- [ ] Generate comprehensive docstrings for any function
- [ ] Create complete class documentation with examples
- [ ] Produce professional API documentation
- [ ] Write project-level README files
- [ ] Maintain consistent documentation standards
- [ ] Include practical examples and use cases

**Completion Time:** 13 minutes  
**Next:** Module 4 - Debugging and Troubleshooting