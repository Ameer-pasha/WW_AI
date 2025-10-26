# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User,Employee, Goal, Bonus, PerformanceTrend

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables & sample users on first run
@app.before_first_request
def create_tables():
    db.create_all()
    # Add sample users if none exist
    if User.query.count() == 0:
        manager = User(email='manager@workwise.ai', role='manager')
        manager.set_password('password123')
        employee = User(email='employee@workwise.ai', role='employee')
        employee.set_password('password123')
        db.session.add(manager)
        db.session.add(employee)
        db.session.commit()

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        user = User.query.filter_by(email=email, role=role).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard', role=role))
        else:
            flash('Invalid email, password, or role.', 'error')

    return render_template('login.html')

@app.route('/dashboard/<role>')
@login_required
def dashboard(role):
    if current_user.role != role:
        flash('Access denied.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', role=role)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/dashboard/<role>')
@login_required
def dashboard(role):
    if current_user.role != role:
        flash('Access denied.', 'error')
        return redirect(url_for('login'))

    # Fetch dashboard metrics
    team_members = Employee.query.count()
    active_members = Employee.query.filter(Employee.performance_score > 0).count()  # Mock "active"

    # Get current month's goal
    current_month = "2025-04"  # You can use datetime.now().strftime("%Y-%m")
    goal = Goal.query.filter_by(month=current_month).first()
    goals_completed = goal.completed if goal else 0
    goals_total = goal.target if goal else 5

    # Get bonus for current month
    bonus = Bonus.query.filter_by(month=current_month).first()
    bonus_amount = bonus.amount if bonus else 0

    # Get attention needed (low performers)
    attention_needed = Employee.query.filter(Employee.performance_score < 80).count()

    # Get performance trend data for chart
    trends = PerformanceTrend.query.filter_by(month=current_month).order_by(PerformanceTrend.week).all()
    weeks = [t.week for t in trends]
    current_data = [t.current_month for t in trends]
    previous_data = [t.previous_month for t in trends]

    # Get all employees (for search section)
    employees = Employee.query.all()

    return render_template(
        'dashboard.html',
        role=role,
        team_members=team_members,
        active_members=active_members,
        goals_completed=goals_completed,
        goals_total=goals_total,
        bonus_amount=bonus_amount,
        attention_needed=attention_needed,
        weeks=weeks,
        current_data=current_data,
        previous_data=previous_data,
        employees=employees
    )


if __name__ == '__main__':
    app.run(debug=True)