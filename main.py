


from flask import Flask, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, login_required, UserMixin, current_user, logout_user, login_user

import logging

from flask_sqlalchemy import SQLAlchemy

from models import db, User, Task  # Import db, User and Task from models.py

app = Flask(__name__)

login_manager = LoginManager(app)

app.config["SECRET_KEY"] = "888-dg885v5-v685fv-5xc4vvf-gjgh5cvb-5gh413v"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mytaskpool.db"  # SQLite database URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking for SQLAlchemy

db.init_app(app)


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
    # Retrieve tasks for the current user sorted by the average score in descending order
    # Query the database for tasks sorted by average score in descending order
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.average_score.desc()).limit(10).all()

    # Serialize tasks to JSON format
    serialized_tasks = [{"id": task.id, "title": task.title, "description": task.description, "impact": task.impact, "ease": task.ease,
                         "confidence": task.confidence, "average_score": task.average_score} for task in tasks]

    return jsonify(serialized_tasks)


@app.route("/delete_task", methods=["DELETE"])
@login_required
def delete_task():
    task_id = request.args.get("task_id")
    print(task_id)

    # Find the task in database
    task = Task.query.filter_by(id=task_id).first()

    print(task.id, task.title)

    if task and task.user_id == current_user.id:
        # Delete the task
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'message': 'Task not found'}), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
