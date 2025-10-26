# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'employee' or 'manager'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    performance_score = db.Column(db.Integer, nullable=False)  # e.g., 85/100
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Relationship
    manager = db.relationship('User', backref='employees')

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    target = db.Column(db.Integer, nullable=False)  # e.g., 5 goals
    completed = db.Column(db.Integer, default=0)    # e.g., 2 completed
    month = db.Column(db.String(7), nullable=False) # e.g., "2025-04"

class Bonus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # ₹1,25,000
    month = db.Column(db.String(7), nullable=False)       # "2025-04"
    description = db.Column(db.String(200), nullable=True)

class PerformanceTrend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.String(10), nullable=False)     # "Week 1", "Week 2", etc.
    current_month = db.Column(db.Float, nullable=False) # e.g., 75.0
    previous_month = db.Column(db.Float, nullable=False) # e.g., 72.0
    month = db.Column(db.String(7), nullable=False)      # "2025-04"