# Create a Flask REST API for user management with CRUD operations
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)
# In-memory user storage for demo purposes
users = []
user_id_counter = 1

# POST /users - Create a new user with name, email, and age validation
@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    if not name or not email or not age:
        return jsonify({'error': 'Name, email, and age are required'}), 400
    if not isinstance(age, int) or age < 0:
        return jsonify({'error': 'Age must be a positive integer'}), 400
    user = {'id': user_id_counter, 'name': name, 'email': email, 'age': age}
    users.append(user)
    user_id_counter += 1
    return jsonify(user), 201

# GET /users - Retrieve a list of all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# PUT /users/<id> - Update user information
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    for user in users:
        if user['id'] == user_id:
            if name:
                user['name'] = name
            if email:
                user['email'] = email
            if age:
                if not isinstance(age, int) or age < 0:
                    return jsonify({'error': 'Age must be a positive integer'}), 400
                user['age'] = age
            return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# DELETE /users/<id> - Remove user from system
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return '', 204
    return jsonify({'error': 'User not found'}), 404

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)