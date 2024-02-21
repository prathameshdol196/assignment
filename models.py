from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
