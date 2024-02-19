


from flask import Flask, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, login_required, UserMixin, current_user, logout_user, login_user

import logging

# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager

from flask_sqlalchemy import SQLAlchemy

from models import db, User, Task  # Import db, User and Task from models.py

app = Flask(__name__)

login_manager = LoginManager(app)

app.config['SECRET_KEY'] = '888-dg885v5-v685fv-5xc4vvf-gjgh5cvb-5gh413v'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mytaskpool.db'  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for SQLAlchemy

db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return 'Hello, World!'


# Register User
@app.route("/register", methods=["POST"])
def register():

    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'message': 'Username or email already exists'}), 400

    password_hash = generate_password_hash(password)

    new_user = User(username=username, email=email, password_hash=password_hash)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    # Return registration success response with JWT token
    return jsonify({'message': 'User registered successfully'}), 201


@app.route("/login", methods=["POST"])
def login():
    # Retrieve login credentials from the request
    email = request.args.get('email')
    password = request.args.get('password')

    print(email)
    print(password)

    # Find the user in the database
    user = User.query.filter_by(email=email).first()  # i think somwthing is wrong here

    print(user)
    print(User.query.filter_by(email=email).all())
    print(user.username, user.email, user.password_hash)

    if user and check_password_hash(user.password_hash, password):
        print("Inside if user")

        # Log in the user
        print("inside if login")
        login_user(user)
        return jsonify({'message': 'Login successful'})

    # Return an error message if login fails
    return jsonify({'message': 'Invalid username or password'}), 401


# Logout user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


# Route for adding a task (login required)
@app.route("/tasks", methods=["POST"])
@login_required
def add_task():
    # Get task data from request
    title = request.json.get('title')
    description = request.json.get('description')
    impact = request.json.get('impact')
    ease = request.json.get('ease')
    confidence = request.json.get('confidence')

    # Validate input
    if not all([title, description, impact, ease, confidence]):
        return jsonify({'message': 'All fields are required'}), 400

    # Create new task
    new_task = Task(title=title, description=description, impact=impact, ease=ease, confidence=confidence, user_id=get_jwt_identity())
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task added successfully'}), 201


# Route for retrieving tasks (login required)
@app.route("/tasks", methods=["GET"])
@login_required
def get_tasks():
    pass


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
