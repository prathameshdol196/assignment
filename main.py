


from flask import Flask, request, jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from flask_sqlalchemy import SQLAlchemy

from models import db, User, Task  # Import db, User and Task from models.py

app = Flask(__name__)

app.config['SECRET_KEY'] = '888-dg885v5-v685fv-5xc4vvf-gjgh5cvb-5gh413v'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mytaskpool.db'  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for SQLAlchemy

db.init_app(app)


@app.route('/')
def index():
    # Example route
    return 'Hello, World!'


@app.route("/register", methods=["POST"])
def register():

    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'message': 'Username or email already exists'}), 400

    new_user = User(username=username, email=email, password_hash=password)

    db.session.add(new_user)
    db.session.commit()

    # Generate JWT token for the new user
    access_token = create_access_token(identity=new_user.id)

    # Return registration success response with JWT token
    return jsonify({'message': 'User registered successfully', 'access_token': access_token}), 201


# Route for adding a task (login required)
@app.route("/tasks", methods=["POST"])
@jwt_required()
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
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.serialize() for task in tasks])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
