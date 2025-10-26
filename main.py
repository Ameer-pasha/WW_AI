import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash




# ==========================
# FLASK & DATABASE SETUP
# ==========================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'workwise.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# ==========================
# DATABASE MODELS
# ==========================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Manager or Employee

    # Metrics for manager only
    goals_assigned = db.Column(db.Integer, default=0)
    goals_total = db.Column(db.Integer, default=0)
    team_health_score = db.Column(db.Float, default=0)
    feedbacks_received = db.Column(db.Integer, default=0)
    recognition_received = db.Column(db.Integer, default=0)

    employees = db.relationship('Employee', foreign_keys='Employee.manager_id', backref='manager', lazy=True)
    employee_profile = db.relationship('Employee', foreign_keys='Employee.user_id', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Add user_id to match models.py
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, unique=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    position = db.Column(db.String(50))
    department = db.Column(db.String(50))
    performance_score = db.Column(db.Integer, default=75)
    review = db.Column(db.Text)
    ai_summary = db.Column(db.String(500), default="")
    recent_activities = db.Column(db.PickleType, default=[])

    # Fields for detailed metrics
    work_logs = db.Column(db.String(50))
    commits = db.Column(db.Integer)
    reward = db.Column(db.String(50))

    hire_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    target = db.Column(db.Integer)
    completed = db.Column(db.Integer)
    month = db.Column(db.String(20))


class Bonus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    month = db.Column(db.String(20))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))


class LeadershipActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))


@app.template_filter()
def format_number(value):
    try:
        return "{:,.2f}".format(value)
    except (ValueError, TypeError):
        return value

# ==========================
# DATABASE INIT & DUMMY DATA
# ==========================
def init_db():
    # Delete old DB
    db_path = os.path.join(BASE_DIR, "workwise.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️  Old database deleted.")

    # Create fresh tables
    db.create_all()
    print("✅ Database tables created.")

    # Manager
    manager = User(name="John Manager", email="manager@example.com", role="Manager",
                   goals_assigned=5, goals_total=8, team_health_score=82,
                   feedbacks_received=12, recognition_received=7)
    manager.set_password("Password123!")
    db.session.add(manager)
    db.session.commit()
    print("✅ Manager created.")

    # Employees (50 dummy)
    import random

    names = [
        "Aarav Sharma", "Neha Patel", "Priya Singh", "Rahul Verma", "Sneha Reddy",
        "Karan Mehta", "Riya Kapoor", "Aditya Joshi", "Isha Desai", "Vikram Rao",
        "Anjali Nair", "Sameer Khan", "Pooja Bhatt", "Rohit Sinha", "Tara Malhotra",
        "Sahil Gupta", "Meera Iyer", "Varun Choudhary", "Nina Thomas", "Arjun Dutt",
        "Shreya Agarwal", "Kunal Bhatia", "Divya Rani", "Manish Yadav", "Alisha Singh",
        "Raj Malhotra", "Simran Kaur", "Devansh Gupta", "Aisha Sharma", "Tarun Kumar",
        "Neelam Joshi", "Ritesh Mehra", "Maya Nair", "Kartik Verma", "Ananya Reddy",
        "Vivek Kapoor", "Sana Khan", "Irfan Shaikh", "Nisha Patel", "Harshad Rao",
        "Priti Deshmukh", "Ankit Joshi", "Rupal Mehta", "Yash Sharma", "Aditi Kapoor",
        "Raghav Malhotra", "Sonali Singh", "Kabir Choudhary", "Rhea Thomas", "Nikhil Gupta"
    ]

    positions = ["Frontend Developer", "Backend Developer", "UI/UX Designer",
                 "DevOps Engineer", "Product Manager", "Data Scientist"]

    for i in range(50):
        emp = Employee(
            name=names[i],
            user_id=None,  # Not linked to a User account
            position=random.choice(positions),
            department="Engineering",
            performance_score=random.randint(55, 100),
            manager_id=manager.id,
            ai_summary=f"{names[i]} has shown consistent performance this month.",
            work_logs=f"{random.randint(35, 45)} hrs/week",
            commits=random.randint(50, 100),
            reward=random.choice(["Bonus", "Recognition", "Gift Voucher"])
        )
        emp.recent_activities = [
            {"action": f"Completed task {j}", "time_ago": f"{random.randint(1, 24)} hours ago"}
            for j in range(1, 4)
        ]
        db.session.add(emp)

    db.session.commit()
    print("✅ 50 Employees created.")

    # Goals & Bonuses
    current_month = datetime.now().strftime("%B-%Y")
    if not Goal.query.filter_by(month=current_month).first():
        goal = Goal(title="Q4 Goals", target=10, completed=6, month=current_month)
        db.session.add(goal)
        print("✅ Goal created.")

    if not Bonus.query.filter_by(month=current_month).first():
        first_employee = Employee.query.first()
        if first_employee:
            bonus = Bonus(amount=15000, month=current_month, employee_id=first_employee.id)
            db.session.add(bonus)
            print("✅ Bonus created.")

    # Leadership Activities
    activities = [
        "Approved bonus for Aarav Sharma",
        "Completed quarterly team review",
        "Set new team goals for Q2",
        "Recognized Priya Singh for design excellence"
    ]
    for act in activities:
        db.session.add(LeadershipActivity(action=act, manager_id=manager.id))

    db.session.commit()
    print("✅ Leadership activities created.")
    print("\n🎉 Database initialized successfully with all dummy data!")


# ==========================
# LOGIN HELPERS
# ==========================
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def login_required(view):
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "danger")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    wrapped_view.__name__ = view.__name__
    return wrapped_view


# ==========================
# ROUTES
# ==========================
@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = get_user_by_email(email)
        if not user or not user.check_password(password):
            flash("Invalid credentials!", "danger")
            return redirect(url_for("login"))
        session.clear()
        session["user_id"] = user.id
        session["role"] = user.role
        flash(f"Logged in as {user.role}", "success")
        if user.role == "Manager":
            return redirect(url_for("team_dashboard"))
        return redirect(url_for("your_dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


# ==========================
# DASHBOARDS
# ==========================
@app.route("/your-dashboard")
@login_required
def your_dashboard():
    user = get_user_by_id(session["user_id"])

    if user.role == "Manager":
        # Manager's personal dashboard
        team_members = Employee.query.filter_by(manager_id=user.id).all()

        # Calculate manager metrics
        goal_progress = (user.goals_assigned / user.goals_total * 100) if user.goals_total > 0 else 0

        summary_cards = [
            {
                "title": "Goals Assigned",
                "main_value": f"{user.goals_assigned}/{user.goals_total}",
                "subtitle": f"{goal_progress:.0f}% completion",
                "icon": "flag",
                "css_class": "summary-card",
                "progress_percent": goal_progress
            },
            {
                "title": "Team Health Score",
                "main_value": f"{user.team_health_score}%",
                "subtitle": "Overall wellbeing",
                "icon": "favorite",
                "css_class": "summary-card",
                "icon_class": "icon-red"
            },
            {
                "title": "Feedbacks Received",
                "main_value": user.feedbacks_received,
                "subtitle": "From team members",
                "icon": "feedback",
                "css_class": "summary-card"
            },
            {
                "title": "Recognition Received",
                "main_value": user.recognition_received,
                "subtitle": "Awards & mentions",
                "icon": "emoji_events",
                "css_class": "summary-card",
                "icon_class": "icon-orange"
            }
        ]

        # AI Reflection for manager
        ai_reflection = f"You've successfully assigned {user.goals_assigned} out of {user.goals_total} goals this quarter. Your team health score of {user.team_health_score}% indicates strong morale. Consider scheduling 1-on-1s with team members to maintain engagement."

        # Recent leadership activities
        activities_query = LeadershipActivity.query.filter_by(manager_id=user.id) \
            .order_by(LeadershipActivity.timestamp.desc()).limit(5).all()

        recent_activities = []
        for activity in activities_query:
            time_diff = datetime.utcnow() - activity.timestamp
            if time_diff.days > 0:
                time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
            elif time_diff.seconds > 3600:
                time_ago = f"{time_diff.seconds // 3600} hour{'s' if time_diff.seconds // 3600 > 1 else ''} ago"
            else:
                time_ago = f"{time_diff.seconds // 60} minute{'s' if time_diff.seconds // 60 > 1 else ''} ago"

            recent_activities.append({
                "title": activity.action,
                "time_ago": time_ago,
                "dot_class": "dot-green"
            })

        return render_template(
            "your_dashboard.html",
            user=user,
            summary_cards=summary_cards,
            ai_reflection=ai_reflection,
            recent_activities=recent_activities
        )

    else:
        # Employee's personal dashboard
        employee = Employee.query.filter_by(user_id=user.id).first()

        if not employee:
            # If employee profile doesn't exist, create a basic one
            employee = Employee(
                name=user.name,
                user_id=user.id,
                position="Employee",
                department="General",
                performance_score=75,
                work_logs="40 hrs/week",
                commits=60,
                ai_summary="Welcome! Your performance data will be updated soon."
            )

        # Calculate employee metrics
        current_month = datetime.now().strftime("%B-%Y")
        bonus_this_month = Bonus.query.filter_by(employee_id=employee.id, month=current_month).first()
        bonus_amount = bonus_this_month.amount if bonus_this_month else 0

        # Get employee rank
        all_employees = Employee.query.all()
        sorted_employees = sorted(all_employees, key=lambda e: e.performance_score, reverse=True)
        employee_rank = next((i + 1 for i, e in enumerate(sorted_employees) if e.id == employee.id), 0)

        summary_cards = [
            {
                "title": "Performance Score",
                "main_value": f"{employee.performance_score}/100",
                "subtitle": f"Rank #{employee_rank} in team",
                "icon": "trending_up",
                "css_class": "summary-card"
            },
            {
                "title": "Work Hours",
                "main_value": employee.work_logs or "40 hrs/week",
                "subtitle": "This week",
                "icon": "schedule",
                "css_class": "summary-card"
            },
            {
                "title": "Code Commits",
                "main_value": employee.commits or 0,
                "subtitle": "This month",
                "icon": "code",
                "css_class": "summary-card"
            },
            {
                "title": "Bonus Earned",
                "main_value": f"₹{bonus_amount:,.0f}" if bonus_amount else "₹0",
                "subtitle": "This month",
                "icon": "payments",
                "css_class": "summary-card",
                "icon_class": "icon-green"
            }
        ]

        # AI Reflection for employee
        if employee.performance_score >= 90:
            ai_reflection = f"Excellent work! Your performance score of {employee.performance_score}/100 places you in the top tier. Keep up the great work and consider mentoring junior team members."
        elif employee.performance_score >= 75:
            ai_reflection = f"You're performing well with a score of {employee.performance_score}/100. Focus on consistency and look for opportunities to take on challenging projects to boost your score."
        else:
            ai_reflection = f"Your current score is {employee.performance_score}/100. We recommend focusing on code quality and meeting deadlines. Consider reaching out to your manager for guidance."

        # Recent activities for employee
        recent_activities = []
        if employee.recent_activities:
            for activity in employee.recent_activities[:5]:
                recent_activities.append({
                    "title": activity.get("action", "Activity"),
                    "time_ago": activity.get("time_ago", "Recently"),
                    "dot_class": "dot-blue"
                })

        return render_template(
            "your_dashboard.html",
            user=user,
            summary_cards=summary_cards,
            ai_reflection=ai_reflection,
            recent_activities=recent_activities,
            is_employee=True
        )


@app.route("/team-dashboard")
@login_required
def team_dashboard():
    user = get_user_by_id(session["user_id"])

    # Only managers can access team dashboard
    if user.role != "Manager":
        flash("Access denied. Only managers can access Team Dashboard.", "danger")
        return redirect(url_for("your_dashboard"))

    team_members = Employee.query.filter_by(manager_id=user.id).all()

    # Calculate metrics
    avg_performance = sum([e.performance_score for e in team_members]) / len(team_members) if team_members else 0
    total_commits = sum([e.commits or 0 for e in team_members])

    # Get current month goal
    current_month = datetime.now().strftime("%B-%Y")
    current_goal = Goal.query.filter_by(month=current_month).first()
    goals_completed = current_goal.completed if current_goal else 0
    goals_target = current_goal.target if current_goal else 10
    goal_progress = (goals_completed / goals_target * 100) if goals_target > 0 else 0

    # Summary cards data for the template
    summary_cards = [
        {
            "title": "Team Size",
            "main_value": len(team_members),
            "subtitle": "Total employees",
            "icon": "group",
            "css_class": "summary-card",
            "value_class": ""
        },
        {
            "title": "Avg Performance",
            "main_value": f"{avg_performance:.1f}%",
            "subtitle": "Team average score",
            "icon": "trending_up",
            "css_class": "summary-card",
            "value_class": "highlight-green" if avg_performance >= 75 else "highlight-orange"
        },
        {
            "title": "Goals Completed",
            "main_value": f"{goals_completed}/{goals_target}",
            "subtitle": f"{goal_progress:.0f}% completion rate",
            "icon": "flag",
            "css_class": "summary-card",
            "value_class": "",
            "progress_max": goals_target,
            "progress_percent": goal_progress
        },
        {
            "title": "Total Commits",
            "main_value": total_commits,
            "subtitle": "This month",
            "icon": "code",
            "css_class": "summary-card",
            "value_class": ""
        }
    ]

    # Employee list data for the template
    employee_list = []
    for emp in team_members:
        # Get initials
        name_parts = emp.name.split()
        initials = "".join([part[0].upper() for part in name_parts[:2]])

        # Determine score color
        if emp.performance_score >= 90:
            score_color = "score-high"
        elif emp.performance_score >= 75:
            score_color = "score-medium"
        else:
            score_color = "score-low"

        employee_list.append({
            "id": emp.id,
            "name": emp.name,
            "role": emp.position or "Employee",
            "score": emp.performance_score,
            "initials": initials,
            "score_color": score_color
        })

    # Sort by performance score descending
    employee_list.sort(key=lambda e: e["score"], reverse=True)

    return render_template(
        "team_dashboard.html",
        user=user,
        summary_cards=summary_cards,
        employee_list=employee_list
    )


@app.route("/employee/<int:employee_id>")
@login_required
def employee_detail(employee_id):
    user = get_user_by_id(session["user_id"])
    if user.role != "Manager" and user.id != employee_id:
        flash("Access denied.", "danger")
        return redirect(url_for("your_dashboard"))

    employee = Employee.query.get(employee_id)
    return render_template("employee-detail-view.html", employee=employee)


@app.route("/insights")
@login_required
def insights():
    user = get_user_by_id(session["user_id"])

    # Only managers can access insights
    if user.role != "Manager":
        flash("Access denied. Only managers can access AI Insights.", "danger")
        return redirect(url_for("your_dashboard"))

    team_members = Employee.query.filter_by(manager_id=user.id).all()

    # Top Performers (top 5)
    top_performers = sorted(team_members, key=lambda e: e.performance_score, reverse=True)[:5]

    # Attention Needed (bottom 5)
    attention_needed = sorted(team_members, key=lambda e: e.performance_score)[:5]

    # Calculate metrics
    avg_performance = sum([e.performance_score for e in team_members]) / len(team_members) if team_members else 0

    # Goal completion rate
    current_month = datetime.now().strftime("%B-%Y")
    current_goal = Goal.query.filter_by(month=current_month).first()
    goal_completion_rate = int(
        (current_goal.completed / current_goal.target * 100)) if current_goal and current_goal.target > 0 else 0

    # AI Suggestions based on data analysis
    ai_suggestions = []

    # Suggestion 1: Low performers
    if len([e for e in team_members if e.performance_score < 70]) > 0:
        low_count = len([e for e in team_members if e.performance_score < 70])
        ai_suggestions.append({
            "type": "alert",
            "title": "Performance Alert",
            "text": f"{low_count} team member{'s' if low_count > 1 else ''} below 70% performance. Schedule 1-on-1 meetings to provide support and set improvement goals."
        })

    # Suggestion 2: High performers recognition
    high_performers_count = len([e for e in team_members if e.performance_score >= 90])
    if high_performers_count > 0:
        ai_suggestions.append({
            "type": "success",
            "title": "Recognition Opportunity",
            "text": f"You have {high_performers_count} top performer{'s' if high_performers_count > 1 else ''} (90+). Consider public recognition or bonus rewards to maintain motivation."
        })

    # Suggestion 3: Goal completion
    if goal_completion_rate < 50:
        ai_suggestions.append({
            "type": "alert",
            "title": "Goal Progress Behind Schedule",
            "text": f"Only {goal_completion_rate}% of goals completed. Review blockers with team and adjust timelines if needed."
        })
    elif goal_completion_rate > 80:
        ai_suggestions.append({
            "type": "success",
            "title": "Excellent Goal Progress",
            "text": f"Team is at {goal_completion_rate}% goal completion. Consider setting stretch goals for high performers."
        })

    # Suggestion 4: Work-life balance
    avg_work_hours = sum([int(e.work_logs.split()[0]) for e in team_members if e.work_logs]) / len(
        [e for e in team_members if e.work_logs]) if any(e.work_logs for e in team_members) else 40
    if avg_work_hours > 45:
        ai_suggestions.append({
            "type": "info",
            "title": "Work-Life Balance Check",
            "text": f"Team averaging {avg_work_hours:.0f} hrs/week. Monitor for burnout and ensure adequate rest periods."
        })

    # Suggestion 5: Code quality
    avg_commits = sum([e.commits or 0 for e in team_members]) / len(team_members) if team_members else 0
    if avg_commits < 60:
        ai_suggestions.append({
            "type": "info",
            "title": "Development Activity Low",
            "text": f"Average commits at {avg_commits:.0f}/month. Investigate if there are blockers affecting productivity."
        })

    return render_template(
        "insights.html",
        user=user,
        top_performers=top_performers,
        attention_needed=attention_needed,
        avg_performance=f"{avg_performance:.1f}",
        goal_completion_rate=goal_completion_rate,
        ai_suggestions=ai_suggestions
    )


@app.route("/leaderboard")
@login_required
def leaderboard():
    user = get_user_by_id(session["user_id"])

    # Only managers can access leaderboard
    if user.role != "Manager":
        flash("Access denied. Only managers can access Leaderboard.", "danger")
        return redirect(url_for("your_dashboard"))

    role_filter = request.args.get('role', 'All Roles')
    sort_option = request.args.get('sort', 'performance_desc')

    # Base query: all employees
    query = Employee.query

    # Filter by role
    if role_filter != 'All Roles':
        query = query.filter_by(position=role_filter)

    employees = query.all()

    # Sorting
    if sort_option == 'performance_desc':
        employees.sort(key=lambda e: e.performance_score, reverse=True)
    elif sort_option == 'performance_asc':
        employees.sort(key=lambda e: e.performance_score)
    elif sort_option == 'commits_desc':
        employees.sort(key=lambda e: e.commits or 0, reverse=True)
    elif sort_option == 'commits_asc':
        employees.sort(key=lambda e: e.commits or 0)

    # Prepare leaderboard data for template
    leaderboard_data = []
    for idx, emp in enumerate(employees, start=1):
        leaderboard_data.append({
            "rank": idx,
            "name": emp.name,
            "role": emp.position,
            "score": emp.performance_score,
            # "work_hours": emp.work_logs,
            "commits": emp.commits,
            "initials": "".join([n[0] for n in emp.name.split()][:2]).upper(),
            "initials_class": "initials-blue",
            "score_class": "top-score" if idx == 1 else "",
        })

    # For filter dropdowns
    all_employees = Employee.query.all()
    roles_filter = ["All Roles"] + sorted(set(e.position for e in all_employees if e.position))
    sort_options = [
        {"key": "performance_desc", "label": "Performance ↓"},
        {"key": "performance_asc", "label": "Performance ↑"},
        {"key": "commits_desc", "label": "Commits ↓"},
        {"key": "commits_asc", "label": "Commits ↑"},
    ]

    # AI tip example (replace with real AI insights later)
    ai_tip = {"text": "Top performers have consistent weekly commits. Reward and motivate them!"}

    return render_template(
        "leaderboard.html",
        leaderboard_data=leaderboard_data,
        current_role_filter=role_filter,
        current_sort_filter=dict((o['key'], o['label']) for o in sort_options).get(sort_option, "Performance ↓"),
        roles_filter=roles_filter,
        sort_options=sort_options,
        ai_tip=ai_tip
    )


# ==========================
# RUN APP
# ==========================
if __name__ == "__main__":
    with app.app_context():
        if not os.path.exists(os.path.join(BASE_DIR, "workwise.db")):
            init_db()
        else:
            print("ℹ️  Database already exists. Delete 'workwise.db' to reinitialize.")
    app.run(debug=True)