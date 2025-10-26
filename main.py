import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_cli import with_appcontext
import click
from datetime import datetime

from models import db, User, Employee, LeadershipActivity

# ======================================================
# 1. FLASK SETUP & CONFIGURATION
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '0c59828d5e1657c913f412c1f8b4d6a782a0b1e4c7d0e9f65342a1b07698c1d2'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "workwise.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# ======================================================
# 2. DATABASE INITIALIZATION LOGIC
# ======================================================
def init_db(app_context=None):
    """Drops existing tables, creates new ones, and adds dummy data."""
    context = app_context if app_context else app.app_context()
    with context:
        db.drop_all()
        db.create_all()

        # --- Dummy Users ---
        manager = User(
            email='manager@example.com',
            role='Manager',
            goals_assigned=3,
            goals_total=5,
            team_health_score=84,
            feedbacks_received=12,
            recognition_received=5
        )
        manager.set_password('Password123!')
        db.session.add(manager)
        db.session.commit()  # get manager.id

        employee = User(email='employee@example.com', role='Employee')
        employee.set_password('Password123!')
        db.session.add(employee)
        db.session.commit()

        # --- Dummy Employees ---
        employees = [
            {'name': 'Alice Johnson', 'job_title': 'Lead Developer', 'performance_score': 92, 'manager_id': manager.id},
            {'name': 'Bob Smith', 'job_title': 'UX Designer', 'performance_score': 85, 'manager_id': manager.id},
            {'name': 'Charlie Brown', 'job_title': 'Data Scientist', 'performance_score': 71, 'manager_id': manager.id},
            {'name': 'Dana Scully', 'job_title': 'Product Manager', 'performance_score': 98, 'manager_id': manager.id},
        ]
        for emp_data in employees:
            db.session.add(Employee(**emp_data))

        # --- Dummy Leadership Activities ---
        activities = [
            {'action': 'Reviewed Q3 goals with Alice Johnson.', 'manager_id': manager.id,
             'timestamp': datetime(2025, 10, 25, 10, 30)},
            {'action': 'Issued recognition for Bob Smith\'s contribution.', 'manager_id': manager.id,
             'timestamp': datetime(2025, 10, 25, 14, 0)},
            {'action': 'Created 3 new coaching goals for Charlie Brown.', 'manager_id': manager.id,
             'timestamp': datetime(2025, 10, 24, 9, 0)},
            {'action': 'Approved $500 bonus for Dana Scully.', 'manager_id': manager.id,
             'timestamp': datetime(2025, 10, 23, 16, 45)},
        ]
        for act in activities:
            db.session.add(LeadershipActivity(**act))

        db.session.commit()
        print("Database initialized and dummy data added.")


@app.cli.command('init-db')
@with_appcontext
def init_db_command():
    """Flask CLI command to initialize the database."""
    init_db(app.app_context())
    click.echo("Database initialized via CLI.")


# ======================================================
# 3. AUTH HELPERS
# ======================================================
def get_user(email, role):
    """Fetch user by email and role."""
    with app.app_context():
        return User.query.filter_by(email=email, role=role).first()


def get_user_by_id(user_id):
    """Fetch user by ID."""
    with app.app_context():
        return User.query.get(user_id)


def login_required(view):
    """Protect routes that require login."""
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))

        user = get_user_by_id(session['user_id'])
        if not user or session.get('role') != user.role:
            session.clear()
            flash('Session expired or role mismatch. Please log in again.', 'danger')
            return redirect(url_for('login'))

        return view(*args, **kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view


# ======================================================
# 4. ROUTES
# ======================================================

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        user = get_user(email, role)

        if not user:
            flash('Incorrect email or role.', 'danger')
        elif not user.check_password(password):
            flash('Incorrect password.', 'danger')
        else:
            session.clear()
            session['user_id'] = user.id
            session['role'] = user.role
            flash(f'Successfully logged in as {user.role}!', 'success')
            return redirect(url_for('team_dashboard') if user.role == 'Manager' else url_for('your_dashboard'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/forgot-password')
def forgot_password():
    flash('This feature is coming soon!', 'info')
    return redirect(url_for('login'))


@app.route('/your-dashboard')
@login_required
def your_dashboard():
    user = get_user_by_id(session['user_id'])

    # Both Employees and Managers use the same dashboard template
    if user.role in ['Employee', 'Manager']:
        return render_template('your_dashboard.html', user=user, current_page='your_dashboard')

    # Fallback for any other role
    flash('You do not have permission to view this dashboard.', 'danger')
    return redirect(url_for('login'))


@app.route('/team-dashboard')
@login_required
def team_dashboard():
    user = get_user_by_id(session['user_id'])
    if user.role != 'Manager':
        flash('You do not have permission to view the team dashboard.', 'danger')
        return redirect(url_for('login'))

    team_members = Employee.query.filter_by(manager_id=user.id).all()
    recent_activities = LeadershipActivity.query.filter_by(manager_id=user.id)\
                            .order_by(LeadershipActivity.timestamp.desc()).limit(4).all()

    return render_template(
        'team_dashboard.html',
        user=user,
        team_members=team_members,
        recent_activities=recent_activities,
        current_page='dashboard'
    )


@app.route('/insights')
@login_required
def insights():
    user = get_user_by_id(session['user_id'])

    if user.role != 'Manager':
        flash('You do not have permission to view AI Insights.', 'danger')
        return redirect(url_for('team_dashboard'))

    # Example AI suggestions
    ai_suggestions = [
        {"title": "Improve Team Communication", "description": "Weekly sync recommended.", "type": "info",
         "icon": "psychology", "icon_class": "icon-blue"},
        {"title": "Focus on High-Priority Projects", "description": "Some projects are lagging behind.",
         "type": "warning", "icon": "warning", "icon_class": "icon-red"},
    ]

    top_performers = Employee.query.order_by(Employee.performance_score.desc()).limit(5).all()
    attention_needed = Employee.query.order_by(Employee.performance_score.asc()).limit(5).all()

    weekly_report_stats = [
        {"label": "Total Goals Assigned", "value": 15, "value_class": "text-primary"},
    ]

    return render_template(
        'insights.html',
        user=user,
        ai_suggestions=ai_suggestions,
        top_performers=top_performers,
        attention_needed=attention_needed,
        weekly_report_stats=weekly_report_stats,
        current_page='insights'
    )

@app.route('/leaderboard')
@login_required
def leaderboard():
    user = get_user_by_id(session['user_id'])

    if user.role != 'Manager':
        flash('You do not have permission to view the leaderboard.', 'danger')
        return redirect(url_for('team_dashboard'))

    # Example leaderboard data
    top_employees = Employee.query.order_by(Employee.performance_score.desc()).limit(5).all()
    attention_needed = Employee.query.order_by(Employee.performance_score.asc()).limit(5).all()

    # Dummy AI tip (replace with actual logic later)
    ai_tip = {
        'text': 'Consider recognizing top performers weekly to boost morale.'
    }

    return render_template(
        'leaderboard.html',
        user=user,
        top_employees=top_employees,
        attention_needed=attention_needed,
        ai_tip=ai_tip,  # <- Pass this!
        current_page='leaderboard'
    )


# ======================================================
# 5. RUN APP
# ======================================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add dummy data only if empty
        if not User.query.first():
            init_db()
    app.run(debug=True)
