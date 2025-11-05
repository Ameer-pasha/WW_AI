import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests




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
    employee_profile = db.relationship('Employee', foreign_keys='Employee.user_id', backref='user', uselist=False) #ye wala line

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
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))  # FIXED
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    completion_date = db.Column(db.Date, nullable=True)
    employee = db.relationship('Employee', backref='goals')


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


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Who receives
    giver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Who gives
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='received_feedbacks')
    giver = db.relationship('User', foreign_keys=[giver_id], backref='given_feedbacks')

    def to_dict(self, anonymous=False):
        """Return feedback dict for template rendering"""
        return {
            "comment": self.comment,
            "giver_name": "Anonymous Employee" if anonymous else self.giver.name,
            "created_at": self.created_at.strftime("%d %b %Y, %H:%M")
        }

@app.template_filter()
def format_number(value):
    try:
        return "{:,.2f}".format(value)
    except (ValueError, TypeError):
        return value

def get_user_dashboard(user_id):
    user = User.query.get(user_id)
    employee = Employee.query.filter_by(user_id=user.id).first()
    if not employee:
        return None
    goals = Goal.query.filter_by(employee_id=employee.id).all()

    total_goals = len(goals)
    completed_goals = len([goal for goal in goals if goal.status == "Completed"])
    completion = (completed_goals / total_goals) * 100 if total_goals else 0

    # Feedback
    feedback_count = Feedback.query.filter_by(user_id=user.id).count()

    # Recognition / Bonus
    bonus_count = Bonus.query.filter_by(employee_id=employee.id).count()
    total_bonus = sum(b.amount for b in Bonus.query.filter_by(employee_id=employee.id).all())

    # Leadership / Team Activity
    leadership_activities = LeadershipActivity.query.filter_by(manager_id=user.id).count()

    dashboard_data = {
        "user": user,
        "completion": round(completion, 2),
        "feedback_count": feedback_count,
        "bonus_count": bonus_count,
        "total_bonus": total_bonus,
        "leadership_activities": leadership_activities
    }

    return dashboard_data


# ==========================
# DATABASE INIT & DUMMY DATA
# ==========================



def init_db():


    """
    Initialize database and create tables if they don't exist.
    Only adds sample data if database is empty.
    """
    db_path = os.path.join(BASE_DIR, "workwise.db")
    is_new_db = not os.path.exists(db_path)

    # Create tables if they don't exist (doesn't delete existing DB)
    db.create_all()

    if is_new_db:
        print("✅ New database created with tables.")
    else:
        print("ℹ️  Database already exists. Tables verified.")

    # Check if database is empty (no users)
    user_count = User.query.count()

    if user_count == 0:
        print("📝 Database is empty. Adding sample data...")
    else:
        print("ℹ️  Database already has users. Skipping sample data.")
        return
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
        user = User(
            name=names[i],
            email=f"employee{i + 1}@example.com",
            role="Employee"
        )
        user.set_password("Password123!")
        db.session.add(user)
        db.session.commit()  # ✅ Commit here

        emp = Employee(
            name=names[i],
            user_id=user.id,
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

    db.session.commit()  # Commit all employees at the end


# ==========================
# LOGIN HELPERS
# ==========================

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "danger")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
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
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")  # Manager or Employee from hidden input

        user = get_user_by_email(email)

        if not user:
            flash("No user found with this email.", "danger")
            return redirect(url_for("login"))

        if not user.check_password(password):
            flash("Incorrect password.", "danger")
            return redirect(url_for("login"))

        if user.role != role:
            flash(f"Role mismatch. You are registered as {user.role}.", "danger")
            return redirect(url_for("login"))

        # Login successful
        session.clear()
        session["user_id"] = user.id
        session["role"] = user.role

        flash(f"Logged in as {user.role}", "success")

        # Redirect based on role
        if user.role == "Manager":
            return redirect(url_for("team_dashboard"))
        else:
            return redirect(url_for("your_dashboard"))

    return render_template("login.html")



@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))

@app.route("/feedback", methods=["GET", "POST"])
@login_required
def give_feedback():
    user = User.query.get(session["user_id"])
    if request.method == "POST":
        comment = request.form.get("comment").strip()
        if comment:
            employee = Employee.query.filter_by(user_id=user.id).first()
            if not employee or not employee.manager_id:
                flash("Manager not found.", "danger")
                return redirect(url_for("your_dashboard"))

            feedback = Feedback(
                user_id=employee.manager_id,  # ✅ Correct
                giver_id=user.id,
                comment=comment
            )
            db.session.add(feedback)
            db.session.commit()
            flash("Feedback submitted successfully!", "success")
            return redirect(url_for("your_dashboard"))
        else:
            flash("Comment cannot be empty.", "warning")

    return render_template("feedback_form.html", user=user)

@app.route("/feedback-received")
@login_required
def feedback_received():
    user = User.query.get(session["user_id"])
    if user.role != "Manager":
        flash("Access denied.", "danger")
        return redirect(url_for("your_dashboard"))

    feedbacks = Feedback.query.filter_by(user_id=user.id).order_by(Feedback.created_at.desc()).all()
    feedback_list = [f.to_dict(anonymous=True) for f in feedbacks]

    return render_template("feedback_received.html", user=user, feedback_list=feedback_list)

@app.route("/feedback-given")
@login_required
def feedback_given():
    user = User.query.get(session["user_id"])
    feedbacks = Feedback.query.filter_by(giver_id=user.id).order_by(Feedback.created_at.desc()).all()
    feedback_list = [f.to_dict() for f in feedbacks]

    return render_template("feedback_given.html", user=user, feedback_list=feedback_list)



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
            db.session.add(employee)
            db.session.commit()

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
            is_employee=False
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

    # Get goals for this manager's team
    from datetime import datetime, timedelta

    # Get all goals for team members
    team_employee_ids = [e.id for e in team_members]
    all_goals = Goal.query.filter(Goal.employee_id.in_(team_employee_ids)).all() if team_employee_ids else []

    # Calculate goal completion
    goals_completed = len([g for g in all_goals if g.status == "Completed"])
    goals_target = len(all_goals) if all_goals else 10  # Default to 10 if no goals
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
    employee = Employee.query.get(employee_id)
    if user.role != "Manager" and employee.user_id != user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("your_dashboard"))

    employee = Employee.query.get(employee_id)
    return render_template("employee-detail-view.html", employee=employee, active_page="employees")


@app.route("/insights")
@login_required
def insights():
    user = get_user_by_id(session["user_id"])

    ai_suggestions = []

    if user.role == "Manager":
        # Manager-specific insights
        team_members = Employee.query.filter_by(manager_id=user.id).all()

        top_performers = sorted(team_members, key=lambda e: e.performance_score, reverse=True)[:5]
        attention_needed = sorted(team_members, key=lambda e: e.performance_score)[:5]
        avg_performance = sum([e.performance_score for e in team_members]) / len(team_members) if team_members else 0

        team_employee_ids = [e.id for e in team_members]
        all_goals = Goal.query.filter(Goal.employee_id.in_(team_employee_ids)).all() if team_employee_ids else []
        goals_completed = len([g for g in all_goals if g.status == "Completed"])
        goals_target = len(all_goals) if all_goals else 10
        goal_completion_rate = int((goals_completed / goals_target * 100)) if goals_target > 0 else 0

        # AI Suggestions for Manager
        low_count = len([e for e in team_members if e.performance_score < 70])
        if low_count > 0:
            ai_suggestions.append({
                "type": "alert",
                "title": "Performance Alert",
                "text": f"{low_count} team member{'s' if low_count > 1 else ''} below 70% performance. Schedule 1-on-1 meetings to provide support."
            })

        high_count = len([e for e in team_members if e.performance_score >= 90])
        if high_count > 0:
            ai_suggestions.append({
                "type": "success",
                "title": "Recognition Opportunity",
                "text": f"{high_count} top performer{'s' if high_count > 1 else ''} (90+). Consider rewards to maintain motivation."
            })

        if goal_completion_rate < 50:
            ai_suggestions.append({
                "type": "alert",
                "title": "Goal Progress Behind Schedule",
                "text": f"Only {goal_completion_rate}% of goals completed. Review blockers and adjust timelines if needed."
            })
        elif goal_completion_rate > 80:
            ai_suggestions.append({
                "type": "success",
                "title": "Excellent Goal Progress",
                "text": f"Team is at {goal_completion_rate}% goal completion. Consider stretch goals for high performers."
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

    else:
        # Employee-specific insights
        employee = Employee.query.filter_by(user_id=user.id).first()
        personal_score = employee.performance_score if employee else 0
        goal_completion_rate = employee.goal_completion_rate if hasattr(employee, "goal_completion_rate") else 0

        # For template consistency, pass single-item lists for top_performers and attention_needed
        top_performers = [employee] if employee else []
        attention_needed = []

        # AI Suggestions for Employee
        if personal_score < 70:
            ai_suggestions.append({
                "type": "alert",
                "title": "Performance Alert",
                "text": f"Your performance is below 70%. Focus on improving your goals."
            })
        elif personal_score >= 90:
            ai_suggestions.append({
                "type": "success",
                "title": "Great Job!",
                "text": f"Your performance is excellent. Keep up the good work!"
            })

        return render_template(
            "insights.html",
            user=user,
            top_performers=top_performers,
            attention_needed=attention_needed,
            avg_performance=f"{personal_score:.1f}",
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


@app.route('/performance_data')
@login_required
def performance_data():
    try:
        user = User.query.get(session['user_id'])
        print(f"User: {user.name}, Role: {user.role}")

        if user.role == 'Manager':
            # Manager sees all team members
            team_members = Employee.query.filter_by(manager_id=user.id).all()

            data = {
                "labels": [e.name for e in team_members],
                "current_week": [e.performance_score for e in team_members],
                "previous_week": [max(e.performance_score - 5, 0) for e in team_members]
            }
        else:
            # Employee sees only their own data
            employee = Employee.query.filter_by(user_id=user.id).first()

            if not employee:
                return jsonify({"error": "Employee profile not found"}), 404

            # Show employee's performance over last 4 weeks (simulated)
            import random
            current_score = employee.performance_score

            data = {
                "labels": ["Week 1", "Week 2", "Week 3", "Week 4 (Current)"],
                "current_week": [
                    max(current_score - random.randint(10, 20), 50),
                    max(current_score - random.randint(5, 15), 55),
                    max(current_score - random.randint(0, 10), 60),
                    current_score
                ],
                "previous_week": []  # Not needed for employee view
            }

        # print("Performance data:", data)
        return jsonify(data)

    except Exception as e:
        print(f"Error in performance_data: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/personal_performance_data')
@login_required
def personal_performance_data():
    try:
        user = User.query.get(session['user_id'])
        print(f"Personal data - User: {user.name}, Role: {user.role}")

        if user.role == 'Manager':
            # Manager's personal goals
            data = {
                "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
                "planned": [10, 15, 20, 25],
                "actual": [8, 14, 18, 23]
            }
        else:
            # Employee's personal goals
            employee = Employee.query.filter_by(user_id=user.id).first()

            if not employee:
                return jsonify({"error": "Employee profile not found"}), 404

            import random
            planned_base = [10, 15, 20, 25]
            actual_goals = []

            for planned in planned_base:
                actual = planned - random.randint(0, 3)
                actual_goals.append(max(actual, 0))

            data = {
                "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
                "planned": planned_base,
                "actual": actual_goals
            }

        # print("Personal performance data:", data)
        return jsonify(data)

    except Exception as e:
        print(f"Error in personal_performance_data: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/employee_performance_data/<int:employee_id>')
@login_required
def employee_performance_data(employee_id):
    """
    Returns performance data for a specific employee
    Current month vs Previous month comparison
    """
    try:
        user = User.query.get(session['user_id'])
        print(f"Fetching performance data for employee {employee_id} by user: {user.name}")

        # Verify user has permission (must be a manager)
        if user.role != 'Manager':
            return jsonify({"error": "Unauthorized access"}), 403

        # Get the employee
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        # Verify this employee belongs to this manager
        if employee.manager_id != user.id:
            return jsonify({"error": "Unauthorized access to this employee"}), 403

        import random

        # Generate weekly data for current and previous month
        # Week 1, Week 2, Week 3, Week 4
        current_score = employee.performance_score

        # Current month: trending upward to current score
        current_month_data = [
            max(current_score - random.randint(15, 25), 50),
            max(current_score - random.randint(10, 20), 55),
            max(current_score - random.randint(5, 15), 60),
            current_score
        ]

        # Previous month: slightly lower average
        previous_avg = max(current_score - 10, 50)
        previous_month_data = [
            max(previous_avg - random.randint(5, 15), 45),
            max(previous_avg - random.randint(0, 10), 50),
            max(previous_avg + random.randint(0, 5), 50),
            max(previous_avg + random.randint(0, 8), 50)
        ]

        data = {
            "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "current_month": current_month_data,
            "previous_month": previous_month_data,
            "employee_name": employee.name
        }

        # print("Employee performance data:", data)
        return jsonify(data)

    except Exception as e:
        print(f"Error in employee_performance_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/submit-work', methods=['POST'])
@login_required
def submit_work():
    data = request.get_json()
    user = User.query.get(session['user_id'])
    employee = Employee.query.filter_by(user_id=user.id).first()

    title = data.get('title')
    description = data.get('description')

    webhook_data = {
        'employee_name': employee.name if employee else user.name,
        'employee_position': employee.position if employee else 'Employee',
        'title': title,
        'description': description,
        'timestamp': datetime.utcnow().isoformat()
    }

    try:
        response = requests.post(
            'https://cobra34ry.app.n8n.cloud/webhook/ai-linkedin-post',
            json=webhook_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )


        # print("WEBHOOK RESPONSE:", response.text)   # ✅ Debug line
        response.raise_for_status()

        return jsonify({"status": "success", "message": "Work posted to LinkedIn successfully!"}), 200

    except Exception as e:
        print("WEBHOOK ERROR:", e)  # ✅ Debug line
        return jsonify({"status": "error", "message": "Failed to post. Please try again."}), 500

@app.route('/goals')
@login_required
def goals_management():
    user = User.query.get(session['user_id'])

    assigned_goals = (
        db.session.query(Goal)
        .join(Employee)
        .filter(Employee.manager_id == user.id, Goal.status == "Assigned")
        .all()
    )

    completed_goals = (
        db.session.query(Goal)
        .join(Employee)
        .filter(Employee.manager_id == user.id, Goal.status == "Completed")
        .order_by(Goal.id.desc())
        .limit(5)
        .all()
    )

    all_employees = Employee.query.filter_by(manager_id=user.id).all()

    return render_template(
        'goals.html',
        user=user,
        assigned_goals=assigned_goals,
        completed_goals=completed_goals,
        all_employees=all_employees
    )


@app.route('/assign_goal', methods=['POST'])
@login_required
def assign_goal():
    data = request.get_json()
    title = data.get('title')
    employee_id = data.get('employee_id')
    due_date = data.get('due_date')

    if not title or not employee_id or not due_date:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    goal = Goal(
        title=title,
        employee_id=employee_id,
        due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
        status="Assigned"
    )
    db.session.add(goal)
    db.session.commit()

    return jsonify({"success": True, "message": "Goal assigned successfully"})


# ADD THIS NEW ROUTE HERE ⬇️
@app.route('/complete_goal', methods=['POST'])
@login_required
def complete_goal():
    """Mark a goal as completed"""
    try:
        data = request.get_json()
        goal_id = data.get('goal_id')

        if not goal_id:
            return jsonify({"success": False, "message": "Goal ID is required"}), 400

        goal = Goal.query.get(goal_id)

        if not goal:
            return jsonify({"success": False, "message": "Goal not found"}), 404

        # Verify the user is the manager of this employee
        user = User.query.get(session['user_id'])
        if user.role != 'Manager':
            return jsonify({"success": False, "message": "Unauthorized"}), 403

        employee = Employee.query.get(goal.employee_id)
        if not employee or employee.manager_id != user.id:
            return jsonify({"success": False, "message": "Unauthorized to complete this goal"}), 403

        # Mark goal as completed
        goal.status = "Completed"
        goal.completion_date = datetime.utcnow().date()

        db.session.commit()

        return jsonify({"success": True, "message": "Goal marked as complete"})

    except Exception as e:
        print(f"Error completing goal: {str(e)}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
# IN FUTURE FOR DYNAMIC VALUES:
# class GoalTracking(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     week = db.Column(db.String(20))  # "Week 1", "Week 2", etc.
#     planned_goals = db.Column(db.Integer)
#     actual_goals = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#@app.route('/personal_performance_data')
# @login_required
# def personal_performance_data():
#     user_id = session['user_id']
#
#     # Get real data from database
#     goal_records = GoalTracking.query.filter_by(user_id=user_id)\
#         .order_by(GoalTracking.created_at.desc())\
#         .limit(4).all()
#
#     labels = [g.week for g in goal_records]
#     planned = [g.planned_goals for g in goal_records]
#     actual = [g.actual_goals for g in goal_records]
#
#     return jsonify({
#         "labels": labels,
#         "planned": planned,
#         "actual": actual
#     })
# <form action="/update_goals" method="POST">
#     <input type="number" name="planned" placeholder="Planned goals">
#     <input type="number" name="actual" placeholder="Actual goals">
#     <button type="submit">Update</button>
# </form>
# @app.route('/update_goals', methods=['POST'])
# @login_required
# def update_goals():
#     new_goal = GoalTracking(
#         user_id=session['user_id'],
#         week=f"Week {week_number}",
#         planned_goals=request.form.get('planned'),
#         actual_goals=request.form.get('actual')
#     )
#     db.session.add(new_goal)
#     db.session.commit()
#     return redirect(url_for('your_dashboard'))
# <select id="timeRange" onchange="updateChart()">
#     <option value="week">Last Week</option>
#     <option value="month">Last Month</option>
#     <option value="quarter">Last Quarter</option>
# </select>
# function updateChart() {
#     const range = document.getElementById('timeRange').value;
#     fetch(`/personal_performance_data?range=${range}`)
#         .then(response => response.json())
#         .then(data => {
#             myChart.data.labels = data.labels;
#             myChart.data.datasets[0].data = data.actual;
#             myChart.update();
#         });
# }
# 6. API Integration
# @app.route('/performance_data')
# def performance_data():
#     # Fetch from external API
#     response = requests.get('https://api.example.com/goals')
#     external_data = response.json()
#
#     # Transform and return
#     return jsonify(external_data)



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