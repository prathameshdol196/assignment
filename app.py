import os
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, UserMixin, current_user, logout_user, login_user
#from models import db, User, Task  # Import db, User and Task from models.py
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey

app = Flask(__name__)

db = SQLAlchemy(app=app)
db.init_app(app)

login_manager = LoginManager(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")  # Secret key
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")  # SQLite database URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking for SQLAlchemy


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(255))
    impact = db.Column(db.Integer)
    ease = db.Column(db.Integer)
    confidence = db.Column(db.Integer)
    average_score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, description, impact, ease, confidence, average_score, user_id):
        self.title = title
        self.description = description
        self.impact = impact
        self.ease = ease
        self.confidence = confidence
        self.average_score = average_score
        self.user_id = user_id

    def __repr__(self):
        return f'<Task {self.description}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return "Hello, World!"


# Register User
@app.route("/register", methods=["POST"])  # Done
def register():

    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"message": "Username or email already exists"}), 400

    password_hash = generate_password_hash(password)

    new_user = User(username=username, email=email, password_hash=password_hash)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    # Return registration success response with JWT token
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])  # Done
def login():
    # Retrieve login credentials from the request
    email = request.args.get("email")
    password = request.args.get("password")

    # Find the user in the database
    user = User.query.filter_by(email=email).first()  # i think somwthing is wrong here

    if user and check_password_hash(user.password_hash, password):
        print("Inside if user")

        # Log in the user
        print("inside if login")
        login_user(user)
        return jsonify({"message": "Login successful"})

    # Return an error message if login fails
    return jsonify({"message": "Invalid username or password"}), 401


# Logout user
@app.route("/logout")  # Done
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})


# Route for adding a task (login required)
@app.route("/add_task", methods=["POST"])  # Done
@login_required
def add_task():
    # Retrieve task data from the request
    title = request.args.get("title")
    description = request.args.get("description")
    impact = int(request.args.get("impact"))  # Convert to integer
    ease = int(request.args.get("ease"))  # Convert to integer
    confidence = int(request.args.get("confidence"))  # Convert to integer

    # Check if all required fields are present and within valid range
    if not all([title, description]) or not 1 <= impact <= 10 or not 1 <= ease <= 10 or not 1 <= confidence <= 10:
        return jsonify({"message": "All fields are required and scores must be between 1 and 10"}), 400

    average_score = (impact + ease + confidence) / 3

    # Create a new task
    new_task = Task(title=title, description=description, impact=impact, ease=ease, confidence=confidence, user_id=current_user.get_id(), average_score=average_score)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task added successfully"}), 201


# Route for retrieving tasks (login required)
@app.route("/get_tasks", methods=["GET"])  # Done
@login_required
def get_tasks():
    # Query the database for tasks sorted by average score in descending order
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.average_score.desc()).limit(10).all()

    # Serialize tasks to JSON format
    serialized_tasks = [{"id": task.id, "title": task.title, "description": task.description, "impact": task.impact, "ease": task.ease,
                         "confidence": task.confidence, "average_score": task.average_score} for task in tasks]

    return jsonify(serialized_tasks), 200


@app.route("/update_task", methods=["PUT"])  # Done
@login_required
def update_task():
    task_id = request.args.get("task_id")
    
    if not task_id:
        return jsonify({"message": "Please enter a valid task id"}), 404

    # Find the task in database
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    # Update task
    title = request.args.get("title")
    description = request.args.get("description")
    impact = request.args.get("impact")
    ease = request.args.get("ease")
    confidence = request.args.get("confidence")

    if title:
        task.title = title

    if description:
        task.description = description

    if impact:
        task.impact = int(impact)

    if ease:
        task.ease = int(ease)

    if confidence:
        task.confidence = int(confidence)

    task.average_score = (task.impact + task.ease + task.confidence) / 3

    # Commit changes to the database
    db.session.commit()

    return jsonify({"message": "Task updated successfully"}), 200


# Route for deleting a task (login required)
@app.route("/delete_task", methods=["DELETE"])  # Done
@login_required
def delete_task():
    task_id = request.args.get("task_id")
    
    if not task_id:
        return jsonify({"message": "Please enter a valid task id"}), 404

    # Find the task in database
    task = Task.query.filter_by(id=task_id).first()

    if task and task.user_id == current_user.id:
        # Delete the task
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    else:
        return jsonify({"message": "Task not found"}), 404


