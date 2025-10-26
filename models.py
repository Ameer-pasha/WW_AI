import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and role management."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Metrics for managers
    goals_assigned = db.Column(db.Integer, default=0)
    goals_total = db.Column(db.Integer, default=5)
    team_health_score = db.Column(db.Integer, default=75)
    feedbacks_received = db.Column(db.Integer, default=0)
    recognition_received = db.Column(db.Integer, default=0)

    # Relationships
    employees = db.relationship(
        'Employee',
        foreign_keys='Employee.manager_id',
        backref='manager_user',
        lazy='dynamic'
    )

    employee_profile = db.relationship(
        'Employee',
        foreign_keys='Employee.user_id',
        backref='user',
        uselist=False
    )

    def set_password(self, password):
        """Hash and set user password."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def get_team_size(self):
        """Get number of direct reports."""
        if self.role == 'Manager':
            return self.employees.count()
        return 0

    def get_team_avg_performance(self):
        """Calculate average team performance score."""
        if self.role != 'Manager':
            return None

        team = self.employees.all()
        if not team:
            return 0

        total_score = sum(emp.performance_score for emp in team)
        return round(total_score / len(team), 1)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Employee(db.Model):
    """Employee model for performance tracking."""
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Link to the User account (optional - not all employees have login)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, unique=True)

    # Link to the manager
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)

    # Job information
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))

    # Performance metrics
    performance_score = db.Column(db.Integer, default=75)
    review = db.Column(db.Text)

    # Timestamps
    hire_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def performance_level(self):
        """Get performance level category."""
        if self.performance_score >= 90:
            return 'Exceptional'
        elif self.performance_score >= 75:
            return 'Meets Expectations'
        elif self.performance_score >= 60:
            return 'Needs Improvement'
        else:
            return 'Unsatisfactory'

    @property
    def performance_color(self):
        """Get color code for performance display."""
        if self.performance_score >= 90:
            return 'success'
        elif self.performance_score >= 75:
            return 'primary'
        elif self.performance_score >= 60:
            return 'warning'
        else:
            return 'danger'

    def __repr__(self):
        return f"<Employee {self.name} - {self.position} (Score: {self.performance_score})>"


class LeadershipActivity(db.Model):
    """Track leadership actions and activities."""
    __tablename__ = 'leadership_activities'

    id = db.Column(db.Integer, primary_key=True)

    # Manager who performed the action
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Description of the action
    action = db.Column(db.String(500), nullable=False)

    # Category of activity
    category = db.Column(db.String(50), default='General')  # e.g., 'Recognition', 'Goal Setting', 'Feedback'

    # Optional link to a specific employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)

    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    manager = db.relationship(
        'User',
        backref=db.backref('activities', lazy='dynamic'),
        foreign_keys=[manager_id]
    )
    employee = db.relationship(
        'Employee',
        backref=db.backref('activities', lazy='dynamic'),
        foreign_keys=[employee_id]
    )

    @property
    def time_ago(self):
        """Get human-readable time since activity."""
        now = datetime.utcnow()
        diff = now - self.timestamp

        if diff.days > 365:
            return f"{diff.days // 365} year{'s' if diff.days // 365 > 1 else ''} ago"
        elif diff.days > 30:
            return f"{diff.days // 30} month{'s' if diff.days // 30 > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hour{'s' if diff.seconds // 3600 > 1 else ''} ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minute{'s' if diff.seconds // 60 > 1 else ''} ago"
        else:
            return "Just now"

    def __repr__(self):
        return f"<LeadershipActivity Manager:{self.manager_id} '{self.action[:50]}...'>"


# Database utility functions
def get_or_create(session, model, **kwargs):
    """Get existing instance or create new one."""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance, True