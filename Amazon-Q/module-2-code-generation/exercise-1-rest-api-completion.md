# Exercise 1: Building REST API with Auto-Completion

## Objective
Experience Amazon Q's intelligent code completion by building a complete Flask REST API.

**Time:** 15 minutes  
**Difficulty:** Intermediate

---

## Setup Instructions

### Step 1: Create Project Structure
```bash
mkdir user-api
cd user-api
touch user_api.py
touch requirements.txt
```

### Step 2: Install Dependencies
Add to `requirements.txt`:
```
Flask==2.3.3
```

---

## Exercise Walkthrough

### Phase 1: Basic Setup (3 minutes)

**Task:** Set up Flask application with auto-completion

**Instructions:**
1. Open `user_api.py`
2. Type this comment and wait for suggestions:
```python
# Create a Flask REST API for user management with CRUD operations
```

3. Start typing the imports and accept Amazon Q suggestions:
```python
from flask import
```

4. Continue with app initialization:
```python
app = Flask(__name__)

# In-memory user storage for demo purposes
users = []
user_id_counter = 1
```

**Expected Behavior:**
- Amazon Q should suggest complete import statements
- Variable initialization should be auto-completed
- Comments should trigger relevant code suggestions

### Phase 2: Create User Endpoint (4 minutes)

**Task:** Build POST endpoint with validation

**Instructions:**
1. Type this comment:
```python
# POST /users - Create a new user with name, email, and age validation
```

2. Start typing the route decorator:
```python
@app.route('/users', methods=['POST'])
def create_user():
```

3. Let Amazon Q complete the function body
4. Accept suggestions for:
   - Request data extraction
   - Input validation
   - User creation logic
   - Response formatting

**Expected Completion:**
```python
@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.get_json()
    
    # Validation
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    user = {
        'id': user_id_counter,
        'name': data['name'],
        'email': data['email'],
        'age': data.get('age', 0)
    }
    
    users.append(user)
    user_id_counter += 1
    
    return jsonify(user), 201
```

### Phase 3: Read Operations (3 minutes)

**Task:** Create GET endpoints

**Instructions:**
1. Type comment for get all users:
```python
# GET /users - Retrieve all users with optional filtering by age
```

2. Start typing and accept completions:
```python
@app.route('/users', methods=['GET'])
def get_users():
```

3. Add get single user endpoint:
```python
# GET /users/<id> - Retrieve specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
```

**Expected Features:**
- Query parameter handling for filtering
- User lookup by ID
- Proper error responses for not found
- JSON formatting

### Phase 4: Update and Delete (3 minutes)

**Task:** Complete CRUD operations

**Instructions:**
1. Type comments and let Amazon Q complete:
```python
# PUT /users/<id> - Update user information
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
```

2. Add delete endpoint:
```python
# DELETE /users/<id> - Remove user from system
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
```

**Expected Completions:**
- User existence validation
- Data update logic
- Proper HTTP status codes
- Error handling

### Phase 5: Application Runner (2 minutes)

**Task:** Add main execution block

**Instructions:**
1. Type comment:
```python
# Run the Flask application in debug mode
```

2. Accept completion for:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

---

## Testing Your API

### Manual Testing Commands

**Create User:**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'
```

**Get All Users:**
```bash
curl http://localhost:5000/users
```

**Get Single User:**
```bash
curl http://localhost:5000/users/1
```

**Update User:**
```bash
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John Smith", "email": "johnsmith@example.com", "age": 31}'
```

**Delete User:**
```bash
curl -X DELETE http://localhost:5000/users/1
```

---

## Completion Quality Checklist

Verify your auto-completed code includes:

### Basic Functionality
- [ ] All CRUD operations implemented
- [ ] Proper HTTP methods and routes
- [ ] JSON request/response handling
- [ ] Input validation

### Error Handling
- [ ] Missing data validation
- [ ] User not found responses
- [ ] Proper HTTP status codes
- [ ] JSON error messages

### Code Quality
- [ ] Consistent naming conventions
- [ ] Appropriate comments
- [ ] Clean function structure
- [ ] Proper imports

---

## Common Completion Patterns

### What Amazon Q Should Suggest

**Route Decorators:**
```python
@app.route('/endpoint', methods=['GET', 'POST'])
```

**Request Handling:**
```python
data = request.get_json()
if not data:
    return jsonify({'error': 'Invalid JSON'}), 400
```

**Response Formatting:**
```python
return jsonify(result), 200
```

**Error Responses:**
```python
return jsonify({'error': 'Not found'}), 404
```

### Improving Completions

**Better Context:**
- Write descriptive comments before functions
- Use consistent variable naming
- Import all necessary modules first
- Define data structures clearly

**Iterative Refinement:**
- Accept initial completion
- Add specific requirements in comments
- Use follow-up completions for edge cases
- Combine multiple suggestions

---

## Troubleshooting

### No Completions Appearing
1. **Check Connection:** Ensure Amazon Q is connected
2. **Manual Trigger:** Use Alt+C (Option+C on Mac)
3. **Context:** Add more descriptive comments
4. **Position:** Ensure cursor is at end of line

### Poor Quality Completions
1. **Add Context:** Write detailed comments
2. **Examples:** Provide sample data structures
3. **Imports:** Include all necessary libraries
4. **Patterns:** Follow consistent coding patterns

### Incomplete Suggestions
1. **Accept Partial:** Use Tab to accept what's useful
2. **Continue Typing:** Trigger additional completions
3. **Chat Fallback:** Use Amazon Q chat for complex logic
4. **Manual Completion:** Fill in missing pieces

---

## Success Criteria

You've successfully completed this exercise when:
- [ ] Complete REST API with all CRUD operations
- [ ] Proper error handling and validation
- [ ] Clean, readable code structure
- [ ] API responds correctly to test requests
- [ ] Understanding of Amazon Q completion patterns

**Next:** Exercise 2 - Natural Language Code Generation