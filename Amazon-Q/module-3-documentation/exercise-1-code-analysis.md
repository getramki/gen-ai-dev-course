# Exercise 1: Code Analysis and Explanation

## Objective
Master Amazon Q's code explanation capabilities by analyzing complex algorithms and patterns.

**Time:** 12 minutes  
**Difficulty:** Intermediate

---

## Setup Instructions

### Create Analysis Workspace
```bash
mkdir code-analysis
cd code-analysis
```

Create the following files for analysis:

---

## Part A: Algorithm Analysis (4 minutes)

### Task A1: Sorting Algorithm Deep Dive

**Create file:** `sorting_algorithms.py`
```python
def merge_sort(arr):
    """Merge sort implementation"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quicksort(arr, low=0, high=None):
    """Quicksort with random pivot"""
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)
    
    return arr

def partition(arr, low, high):
    """Partition function for quicksort"""
    import random
    
    # Random pivot selection
    random_index = random.randint(low, high)
    arr[random_index], arr[high] = arr[high], arr[random_index]
    
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**Amazon Q Analysis Tasks:**

1. **Basic Understanding:**
```
@sorting_algorithms.py Explain how the merge sort algorithm works step by step
```

2. **Complexity Analysis:**
```
What is the time and space complexity of both merge sort and quicksort in this file?
```

3. **Comparison Analysis:**
```
Compare the merge sort and quicksort implementations. When would you use each one?
```

4. **Optimization Review:**
```
Are there any optimizations or improvements you would suggest for these algorithms?
```

**Expected Learning:**
- Understanding of divide-and-conquer algorithms
- Time/space complexity analysis
- Algorithm trade-offs and use cases
- Code optimization opportunities

---

## Part B: Design Pattern Analysis (4 minutes)

### Task B1: Authentication and Security Pattern

**Create file:** `auth_system.py`
```python
from flask import Flask, request, jsonify
from functools import wraps
import jwt
import datetime
import hashlib
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

class UserManager:
    def __init__(self):
        self.users = {}
        self.sessions = {}
    
    def hash_password(self, password):
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        return salt + password_hash.hex()
    
    def verify_password(self, password, stored_hash):
        """Verify password against stored hash"""
        salt = stored_hash[:32]
        stored_password = stored_hash[32:]
        password_hash = hashlib.pbkdf2_hmac('sha256',
                                          password.encode('utf-8'),
                                          salt.encode('utf-8'),
                                          100000)
        return password_hash.hex() == stored_password

def token_required(f):
    """Decorator for protecting routes with JWT tokens"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            
            # Check token expiration
            if datetime.datetime.utcnow() > datetime.datetime.fromtimestamp(data['exp']):
                return jsonify({'message': 'Token has expired'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

@app.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required'}), 400
    
    # In real app, verify against database
    user_manager = UserManager()
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': data['username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'token': token})

@app.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user_id):
    """Protected route example"""
    return jsonify({
        'message': f'Hello {current_user_id}',
        'data': 'This is protected data'
    })
```

**Amazon Q Analysis Tasks:**

1. **Security Pattern Analysis:**
```
@auth_system.py Explain the security patterns and mechanisms used in this authentication system
```

2. **Decorator Pattern:**
```
How does the token_required decorator work? What design pattern is this?
```

3. **Security Assessment:**
```
What security vulnerabilities might exist in this code? How could it be improved?
```

4. **Password Security:**
```
Explain the password hashing mechanism. Why is PBKDF2 used with salt?
```

**Expected Learning:**
- Understanding of authentication patterns
- Decorator pattern implementation
- Security best practices
- JWT token handling

---

## Part C: Data Processing Pipeline Analysis (4 minutes)

### Task C1: Complex Data Transformation

**Create file:** `data_pipeline.py`
```python
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
import logging

class DataPipeline:
    """Advanced data processing pipeline with transformation stages"""
    
    def __init__(self, data_source: str, config: Dict = None):
        self.data_source = data_source
        self.config = config or {}
        self.data = None
        self.transformations = []
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging for pipeline operations"""
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
    
    def load_data(self) -> 'DataPipeline':
        """Load data from various sources"""
        try:
            if self.data_source.endswith('.csv'):
                self.data = pd.read_csv(self.data_source)
            elif self.data_source.endswith('.json'):
                self.data = pd.read_json(self.data_source)
            else:
                raise ValueError(f"Unsupported file format: {self.data_source}")
            
            self.logger.info(f"Loaded {len(self.data)} records from {self.data_source}")
            return self
        
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise
    
    def add_transformation(self, func: Callable, **kwargs) -> 'DataPipeline':
        """Add transformation function to pipeline"""
        self.transformations.append((func, kwargs))
        return self
    
    def clean_data(self, strategies: Dict[str, str] = None) -> 'DataPipeline':
        """Clean data using various strategies"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        strategies = strategies or {
            'duplicates': 'remove',
            'missing_numeric': 'median',
            'missing_categorical': 'mode',
            'outliers': 'iqr'
        }
        
        # Remove duplicates
        if strategies.get('duplicates') == 'remove':
            initial_count = len(self.data)
            self.data = self.data.drop_duplicates()
            removed = initial_count - len(self.data)
            self.logger.info(f"Removed {removed} duplicate records")
        
        # Handle missing values
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        
        if strategies.get('missing_numeric') == 'median':
            self.data[numeric_cols] = self.data[numeric_cols].fillna(
                self.data[numeric_cols].median()
            )
        
        if strategies.get('missing_categorical') == 'mode':
            for col in categorical_cols:
                mode_value = self.data[col].mode().iloc[0] if not self.data[col].mode().empty else 'Unknown'
                self.data[col] = self.data[col].fillna(mode_value)
        
        # Handle outliers using IQR method
        if strategies.get('outliers') == 'iqr':
            for col in numeric_cols:
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers_count = len(self.data[(self.data[col] < lower_bound) | 
                                             (self.data[col] > upper_bound)])
                
                self.data = self.data[(self.data[col] >= lower_bound) & 
                                    (self.data[col] <= upper_bound)]
                
                if outliers_count > 0:
                    self.logger.info(f"Removed {outliers_count} outliers from {col}")
        
        return self
    
    def transform_features(self, transformations: Dict[str, Dict]) -> 'DataPipeline':
        """Apply feature transformations"""
        for column, transform_config in transformations.items():
            if column not in self.data.columns:
                self.logger.warning(f"Column {column} not found, skipping transformation")
                continue
            
            transform_type = transform_config.get('type')
            
            if transform_type == 'normalize':
                # Min-max normalization
                min_val = self.data[column].min()
                max_val = self.data[column].max()
                self.data[column] = (self.data[column] - min_val) / (max_val - min_val)
            
            elif transform_type == 'standardize':
                # Z-score standardization
                mean_val = self.data[column].mean()
                std_val = self.data[column].std()
                self.data[column] = (self.data[column] - mean_val) / std_val
            
            elif transform_type == 'log':
                # Log transformation
                self.data[column] = np.log1p(self.data[column])
            
            elif transform_type == 'categorical_encode':
                # One-hot encoding for categorical variables
                encoded = pd.get_dummies(self.data[column], prefix=column)
                self.data = pd.concat([self.data.drop(column, axis=1), encoded], axis=1)
            
            self.logger.info(f"Applied {transform_type} transformation to {column}")
        
        return self
    
    def aggregate_data(self, group_by: List[str], 
                      agg_functions: Dict[str, str]) -> pd.DataFrame:
        """Aggregate data by specified columns"""
        if not all(col in self.data.columns for col in group_by):
            missing_cols = [col for col in group_by if col not in self.data.columns]
            raise ValueError(f"Columns not found: {missing_cols}")
        
        result = self.data.groupby(group_by).agg(agg_functions).reset_index()
        self.logger.info(f"Aggregated data by {group_by}")
        return result
    
    def execute_pipeline(self) -> pd.DataFrame:
        """Execute all transformations in the pipeline"""
        for func, kwargs in self.transformations:
            self.data = func(self.data, **kwargs)
            self.logger.info(f"Executed transformation: {func.__name__}")
        
        return self.data
    
    def save_results(self, output_path: str, format: str = 'csv') -> None:
        """Save processed data to file"""
        if self.data is None:
            raise ValueError("No data to save")
        
        if format == 'csv':
            self.data.to_csv(output_path, index=False)
        elif format == 'json':
            self.data.to_json(output_path, orient='records')
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        self.logger.info(f"Saved results to {output_path}")
```

**Amazon Q Analysis Tasks:**

1. **Architecture Analysis:**
```
@data_pipeline.py Explain the architecture and design patterns used in this data pipeline class
```

2. **Method Chaining Pattern:**
```
How does the method chaining pattern work in this class? What are its benefits?
```

3. **Error Handling Analysis:**
```
Analyze the error handling strategies used throughout this pipeline. Are they comprehensive?
```

4. **Performance Considerations:**
```
What are the potential performance bottlenecks in this pipeline? How could it be optimized for large datasets?
```

**Expected Learning:**
- Understanding of pipeline architecture
- Method chaining and fluent interface patterns
- Error handling and logging strategies
- Performance optimization considerations

---

## Analysis Quality Checklist

### Effective Questions for Amazon Q

**Algorithm Analysis:**
- [ ] "Explain the algorithm step by step"
- [ ] "What is the time/space complexity?"
- [ ] "Compare this with alternative approaches"
- [ ] "Identify potential optimizations"

**Security Analysis:**
- [ ] "What security vulnerabilities exist?"
- [ ] "How does the authentication mechanism work?"
- [ ] "Are there any security best practices violated?"
- [ ] "How could security be improved?"

**Architecture Analysis:**
- [ ] "Explain the design patterns used"
- [ ] "How do the components interact?"
- [ ] "What are the benefits of this architecture?"
- [ ] "Are there any architectural concerns?"

### Follow-up Questions

After initial explanations, ask:
- "Can you provide a specific example?"
- "What would happen if [edge case]?"
- "How does this compare to [alternative approach]?"
- "What are the trade-offs involved?"

---

## Success Criteria

You've mastered code analysis when you can:
- [ ] Understand complex algorithms through Amazon Q explanations
- [ ] Identify design patterns and architectural decisions
- [ ] Analyze security implications and vulnerabilities
- [ ] Ask effective follow-up questions for deeper understanding
- [ ] Relate explanations to practical development scenarios

**Completion Time:** 12 minutes  
**Next:** Exercise 2 - Documentation Generation