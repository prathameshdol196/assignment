


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

    new_user = User(username=username, email=email, password_hash=password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
