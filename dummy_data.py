# """
# Dummy data for WorkWise application
# Contains realistic test data for users, employees, and activities
# """
# from datetime import datetime, timedelta
# import random
#
# # ======================================================
# # USER DATA
# # ======================================================
# USERS_DATA = [
#     {
#         'name': 'Sarah Johnson',
#         'email': 'manager@example.com',
#         'password': 'Password123!',
#         'role': 'Manager',
#         'goals_assigned': 15,
#         'goals_total': 20,
#         'team_health_score': 84,
#         'feedbacks_received': 28,
#         'recognition_received': 12
#     },
#     {
#         'name': 'Michael Chen',
#         'email': 'manager2@example.com',
#         'password': 'Password123!',
#         'role': 'Manager',
#         'goals_assigned': 12,
#         'goals_total': 15,
#         'team_health_score': 78,
#         'feedbacks_received': 18,
#         'recognition_received': 8
#     },
#     {
#         'name': 'Alice Johnson',
#         'email': 'employee@example.com',
#         'password': 'Password123!',
#         'role': 'Employee',
#         'goals_assigned': 0,
#         'goals_total': 0,
#         'team_health_score': 0,
#         'feedbacks_received': 5,
#         'recognition_received': 3
#     }
# ]
#
# # ======================================================
# # EMPLOYEE DATA
# # ======================================================
# EMPLOYEES_DATA = [
#     # Team 1 - Under Sarah Johnson (Manager 1)
#     {
#         'name': 'Alice Johnson',
#         'position': 'Senior Software Engineer',
#         'department': 'Engineering',
#         'performance_score': 92,
#         'review': 'Exceptional technical leadership and mentorship. Consistently delivers high-quality code and helps junior developers grow. Led the migration to microservices architecture.',
#         'hire_date': datetime(2021, 3, 15).date()
#     },
#     {
#         'name': 'Bob Smith',
#         'position': 'UX Designer',
#         'department': 'Design',
#         'performance_score': 85,
#         'review': 'Creative designs with strong user focus. Excellent collaboration with product team. Redesigned the mobile app interface, increasing user engagement by 25%.',
#         'hire_date': datetime(2022, 1, 10).date()
#     },
#     {
#         'name': 'Charlie Brown',
#         'position': 'Data Scientist',
#         'department': 'Analytics',
#         'performance_score': 71,
#         'review': 'Strong analytical skills but needs improvement in communication. Working on presenting insights more clearly to stakeholders. Recent ML model showed promising results.',
#         'hire_date': datetime(2023, 6, 1).date()
#     },
#     {
#         'name': 'Dana Scully',
#         'position': 'Product Manager',
#         'department': 'Product',
#         'performance_score': 98,
#         'review': 'Outstanding strategic thinking and execution. Successfully launched 3 major features this quarter. Excellent stakeholder management and team collaboration.',
#         'hire_date': datetime(2020, 9, 20).date()
#     },
#     {
#         'name': 'Emily Rodriguez',
#         'position': 'Backend Developer',
#         'department': 'Engineering',
#         'performance_score': 88,
#         'review': 'Reliable and efficient developer. Excellent at optimizing database queries. Recently reduced API response time by 40%. Great team player.',
#         'hire_date': datetime(2022, 7, 12).date()
#     },
#     {
#         'name': 'Frank Williams',
#         'position': 'DevOps Engineer',
#         'department': 'Engineering',
#         'performance_score': 90,
#         'review': 'Expert in CI/CD pipelines and cloud infrastructure. Implemented automated deployment system that reduced release time by 60%. Proactive problem solver.',
#         'hire_date': datetime(2021, 11, 5).date()
#     },
#     {
#         'name': 'Grace Lee',
#         'position': 'UI Designer',
#         'department': 'Design',
#         'performance_score': 82,
#         'review': 'Strong visual design skills. Creates beautiful and functional interfaces. Working on improving design system documentation. Collaborative and open to feedback.',
#         'hire_date': datetime(2023, 2, 18).date()
#     },
#     {
#         'name': 'Henry Taylor',
#         'position': 'QA Engineer',
#         'department': 'Engineering',
#         'performance_score': 86,
#         'review': 'Thorough and detail-oriented. Catches critical bugs before production. Implemented automated testing framework. Good knowledge of both manual and automated testing.',
#         'hire_date': datetime(2022, 4, 22).date()
#     },
#     {
#         'name': 'Isabella Martinez',
#         'position': 'Content Strategist',
#         'department': 'Marketing',
#         'performance_score': 87,
#         'review': 'Creates compelling content that resonates with users. Increased blog traffic by 45%. Excellent understanding of SEO and content marketing strategies.',
#         'hire_date': datetime(2022, 10, 8).date()
#     },
#     {
#         'name': 'James Anderson',
#         'position': 'Security Engineer',
#         'department': 'Engineering',
#         'performance_score': 94,
#         'review': 'Expert in cybersecurity. Implemented security best practices across the organization. Conducted successful penetration testing. Stays updated with latest security threats.',
#         'hire_date': datetime(2021, 5, 30).date()
#     },
#
#     # Team 2 - Under Michael Chen (Manager 2)
#     {
#         'name': 'Karen Thompson',
#         'position': 'Frontend Developer',
#         'department': 'Engineering',
#         'performance_score': 89,
#         'review': 'Excellent React skills. Creates responsive and accessible web applications. Mentors junior developers. Recently led the component library project.',
#         'hire_date': datetime(2021, 8, 14).date()
#     },
#     {
#         'name': 'Liam O\'Brien',
#         'position': 'Data Analyst',
#         'department': 'Analytics',
#         'performance_score': 83,
#         'review': 'Good at identifying trends in data. Creates insightful dashboards. Needs to work on advanced statistical modeling. Collaborative team member.',
#         'hire_date': datetime(2023, 1, 9).date()
#     },
#     {
#         'name': 'Maria Garcia',
#         'position': 'Customer Success Manager',
#         'department': 'Customer Success',
#         'performance_score': 91,
#         'review': 'Exceptional client relationships. Customer retention rate increased to 95% under her management. Proactive in addressing customer concerns.',
#         'hire_date': datetime(2020, 12, 3).date()
#     },
#     {
#         'name': 'Nathan Kim',
#         'position': 'Mobile Developer',
#         'department': 'Engineering',
#         'performance_score': 86,
#         'review': 'Strong iOS and Android development skills. Built several features that improved app store ratings. Good at optimizing mobile performance.',
#         'hire_date': datetime(2022, 5, 25).date()
#     },
#     {
#         'name': 'Olivia Patel',
#         'position': 'Product Designer',
#         'department': 'Design',
#         'performance_score': 93,
#         'review': 'Outstanding UX research and design skills. Conducts thorough user testing. Designs are both beautiful and highly functional. Strong advocate for accessibility.',
#         'hire_date': datetime(2021, 2, 17).date()
#     }
# ]
#
#
# # ======================================================
# # LEADERSHIP ACTIVITIES DATA
# # ======================================================
# def generate_activities_data(manager_id, start_date=None):
#     """Generate realistic leadership activities for a manager."""
#     if start_date is None:
#         start_date = datetime.now() - timedelta(days=30)
#
#     activity_templates = [
#         # Goal Setting
#         "Set quarterly performance goals with {employee}",
#         "Reviewed and updated OKRs with {employee}",
#         "Created development roadmap with {employee}",
#         "Aligned team goals with company objectives for {employee}",
#
#         # Feedback & Coaching
#         "Conducted weekly 1-on-1 meeting with {employee}",
#         "Provided constructive feedback on recent project to {employee}",
#         "Coaching session on time management with {employee}",
#         "Discussed career growth opportunities with {employee}",
#         "Mentored {employee} on technical leadership skills",
#
#         # Recognition
#         "Issued recognition to {employee} for outstanding project delivery",
#         "Nominated {employee} for Employee of the Month award",
#         "Publicly acknowledged {employee}'s contribution in team meeting",
#         "Submitted spot bonus recommendation for {employee}",
#         "Celebrated {employee}'s 2-year work anniversary",
#
#         # Performance Management
#         "Completed mid-year performance review for {employee}",
#         "Reviewed quarterly metrics with {employee}",
#         "Documented exceptional performance by {employee}",
#         "Addressed performance concerns with {employee}",
#
#         # Team Development
#         "Approved training budget for {employee}",
#         "Enrolled {employee} in leadership development program",
#         "Approved conference attendance for {employee}",
#         "Assigned {employee} as mentor to new team member",
#
#         # Compensation & Benefits
#         "Approved salary increase for {employee}",
#         "Recommended promotion for {employee}",
#         "Approved $500 performance bonus for {employee}",
#         "Submitted equity refresh request for {employee}",
#
#         # Project & Task Management
#         "Assigned new strategic project to {employee}",
#         "Reviewed project milestone completion with {employee}",
#         "Discussed workload balance with {employee}",
#         "Approved PTO request for {employee}",
#
#         # Team Building
#         "Organized team lunch to celebrate project success",
#         "Facilitated team retrospective meeting",
#         "Conducted team-building workshop",
#         "Recognized team achievements in all-hands meeting"
#     ]
#
#     employee_names = [
#         'Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Dana Scully',
#         'Emily Rodriguez', 'Frank Williams', 'Grace Lee', 'Henry Taylor',
#         'Isabella Martinez', 'James Anderson', 'Karen Thompson', 'Liam O\'Brien',
#         'Maria Garcia', 'Nathan Kim', 'Olivia Patel'
#     ]
#
#     activities = []
#
#     # Generate 30-50 activities over the past 30 days
#     num_activities = random.randint(30, 50)
#
#     for i in range(num_activities):
#         # Random timestamp within the past 30 days
#         days_ago = random.randint(0, 30)
#         hours = random.randint(8, 18)  # Business hours
#         minutes = random.choice([0, 15, 30, 45])
#
#         timestamp = start_date + timedelta(days=days_ago, hours=hours, minutes=minutes)
#
#         # Select random template and employee
#         template = random.choice(activity_templates)
#         employee = random.choice(employee_names)
#
#         action = template.format(employee=employee)
#
#         activities.append({
#             'action': action,
#             'manager_id': manager_id,
#             'timestamp': timestamp
#         })
#
#     # Sort by timestamp (most recent first)
#     activities.sort(key=lambda x: x['timestamp'], reverse=True)
#
#     return activities
#
#
# # ======================================================
# # SPECIFIC NOTABLE ACTIVITIES
# # ======================================================
# NOTABLE_ACTIVITIES = [
#     {
#         'action': 'Reviewed Q3 goals with Alice Johnson. All targets exceeded by 15%.',
#         'days_ago': 1,
#         'hour': 10,
#         'minute': 30
#     },
#     {
#         'action': 'Issued recognition to Bob Smith for exceptional UI redesign work.',
#         'days_ago': 1,
#         'hour': 14,
#         'minute': 0
#     },
#     {
#         'action': 'Created 3 new coaching goals for Charlie Brown focusing on communication skills.',
#         'days_ago': 2,
#         'hour': 9,
#         'minute': 0
#     },
#     {
#         'action': 'Approved $500 performance bonus for Dana Scully for excellent Q3 results.',
#         'days_ago': 3,
#         'hour': 16,
#         'minute': 45
#     },
#     {
#         'action': 'Conducted leadership training workshop for senior team members.',
#         'days_ago': 4,
#         'hour': 13,
#         'minute': 0
#     },
#     {
#         'action': 'Completed annual performance reviews for entire team.',
#         'days_ago': 5,
#         'hour': 11,
#         'minute': 0
#     },
#     {
#         'action': 'Approved promotions for Emily Rodriguez and James Anderson.',
#         'days_ago': 7,
#         'hour': 15,
#         'minute': 30
#     },
#     {
#         'action': 'Organized team offsite for Q4 planning and team building.',
#         'days_ago': 10,
#         'hour': 9,
#         'minute': 0
#     },
#     {
#         'action': 'Implemented new weekly 1-on-1 schedule with all direct reports.',
#         'days_ago': 14,
#         'hour': 10,
#         'minute': 0
#     },
#     {
#         'action': 'Launched new employee recognition program "Above & Beyond Awards".',
#         'days_ago': 20,
#         'hour': 14,
#         'minute': 0
#     }
# ]
#
#
# def get_notable_activities(manager_id):
#     """Convert notable activities with relative dates to actual datetimes."""
#     now = datetime.now()
#     activities = []
#
#     for activity in NOTABLE_ACTIVITIES:
#         timestamp = now - timedelta(
#             days=activity['days_ago'],
#             hours=(now.hour - activity['hour']),
#             minutes=(now.minute - activity['minute'])
#         )
#
#         activities.append({
#             'action': activity['action'],
#             'manager_id': manager_id,
#             'timestamp': timestamp
#         })
#
#     return activities
#
#
# # ======================================================
# # HELPER FUNCTIONS
# # ======================================================
# def get_all_activities(manager_id, include_generated=True):
#     """
#     Get all activities for a manager.
#
#     Args:
#         manager_id: The manager's ID
#         include_generated: If True, includes auto-generated activities
#
#     Returns:
#         List of activity dictionaries
#     """
#     activities = get_notable_activities(manager_id)
#
#     if include_generated:
#         # Add generated activities (excluding the time range of notable activities)
#         start_date = datetime.now() - timedelta(days=60)
#         generated = generate_activities_data(manager_id, start_date)
#         activities.extend(generated)
#
#     # Sort by timestamp
#     activities.sort(key=lambda x: x['timestamp'], reverse=True)
#
#     return activities
#
#
# def get_employees_for_manager(manager_number=1):
#     """
#     Get employees for a specific manager.
#
#     Args:
#         manager_number: 1 for first manager, 2 for second manager
#
#     Returns:
#         List of employee dictionaries
#     """
#     if manager_number == 1:
#         return EMPLOYEES_DATA[:10]  # First 10 employees
#     else:
#         return EMPLOYEES_DATA[10:]  # Remaining employees
#
#
# # ======================================================
# # DATA STATISTICS
# # ======================================================
# def get_data_stats():
#     """Get statistics about the dummy data."""
#     return {
#         'total_users': len(USERS_DATA),
#         'total_employees': len(EMPLOYEES_DATA),
#         'departments': list(set(emp['department'] for emp in EMPLOYEES_DATA)),
#         'avg_performance_score': sum(emp['performance_score'] for emp in EMPLOYEES_DATA) / len(EMPLOYEES_DATA),
#         'positions': list(set(emp['position'] for emp in EMPLOYEES_DATA))
#     }
#
#
# if __name__ == '__main__':
#     # Print data statistics when run directly
#     stats = get_data_stats()
#     print("Dummy Data Statistics")
#     print("=" * 50)
#     print(f"Total Users: {stats['total_users']}")
#     print(f"Total Employees: {stats['total_employees']}")
#     print(f"Average Performance Score: {stats['avg_performance_score']:.1f}")
#     print(f"\nDepartments: {', '.join(stats['departments'])}")
#     print(f"\nPositions ({len(stats['positions'])}):")
#     for pos in sorted(stats['positions']):
#         print(f"  - {pos}")



"""
Dummy data for WorkWise application
"""
from datetime import datetime

# Users
USERS_DATA = [
    {
        'email': 'manager@example.com',
        'password': 'Password123!',
        'role': 'Manager',
        'goals_assigned': 3,
        'goals_total': 5,
        'team_health_score': 84,
        'feedbacks_received': 12,
        'recognition_received': 5
    },
    {
        'email': 'employee@example.com',
        'password': 'Password123!',
        'role': 'Employee'
    }
]

# Employees
EMPLOYEES_DATA = [
    {'name': 'Alice Johnson', 'job_title': 'Lead Developer', 'performance_score': 92},
    {'name': 'Bob Smith', 'job_title': 'UX Designer', 'performance_score': 85},
    {'name': 'Charlie Brown', 'job_title': 'Data Scientist', 'performance_score': 71},
    {'name': 'Dana Scully', 'job_title': 'Product Manager', 'performance_score': 98},
    {'name': 'Emily Rodriguez', 'job_title': 'Backend Developer', 'performance_score': 88},
    {'name': 'Frank Williams', 'job_title': 'DevOps Engineer', 'performance_score': 90},
    {'name': 'Grace Lee', 'job_title': 'UI Designer', 'performance_score': 82},
    {'name': 'Henry Taylor', 'job_title': 'QA Engineer', 'performance_score': 86},
    {'name': 'Isabella Martinez', 'job_title': 'Content Strategist', 'performance_score': 87},
    {'name': 'James Anderson', 'job_title': 'Security Engineer', 'performance_score': 94},
    {'name': 'Karen Thompson', 'job_title': 'Frontend Developer', 'performance_score': 89},
    {'name': 'Liam O\'Brien', 'job_title': 'Data Analyst', 'performance_score': 83},
    {'name': 'Maria Garcia', 'job_title': 'Customer Success Manager', 'performance_score': 91},
    {'name': 'Nathan Kim', 'job_title': 'Mobile Developer', 'performance_score': 86},
    {'name': 'Olivia Patel', 'job_title': 'Product Designer', 'performance_score': 93}
]

# Leadership Activities
ACTIVITIES_DATA = [
    {'action': 'Reviewed Q3 goals with Alice Johnson.', 'timestamp': datetime(2025, 10, 25, 10, 30)},
    {'action': 'Issued recognition for Bob Smith\'s contribution.', 'timestamp': datetime(2025, 10, 25, 14, 0)},
    {'action': 'Created 3 new coaching goals for Charlie Brown.', 'timestamp': datetime(2025, 10, 24, 9, 0)},
    {'action': 'Approved $500 bonus for Dana Scully.', 'timestamp': datetime(2025, 10, 23, 16, 45)},
    {'action': 'Conducted 1-on-1 meeting with Emily Rodriguez.', 'timestamp': datetime(2025, 10, 22, 14, 30)},
    {'action': 'Reviewed infrastructure updates with Frank Williams.', 'timestamp': datetime(2025, 10, 22, 11, 0)},
    {'action': 'Provided feedback on UI designs to Grace Lee.', 'timestamp': datetime(2025, 10, 21, 15, 30)},
    {'action': 'Approved training request for Henry Taylor.', 'timestamp': datetime(2025, 10, 21, 10, 0)},
    {'action': 'Celebrated Isabella Martinez\'s work anniversary.', 'timestamp': datetime(2025, 10, 20, 16, 0)},
    {'action': 'Discussed security protocols with James Anderson.', 'timestamp': datetime(2025, 10, 20, 9, 30)},
    {'action': 'Code review session with Karen Thompson.', 'timestamp': datetime(2025, 10, 19, 13, 0)},
    {'action': 'Analyzed quarterly metrics with Liam O\'Brien.', 'timestamp': datetime(2025, 10, 19, 10, 30)},
    {'action': 'Addressed customer escalation with Maria Garcia.', 'timestamp': datetime(2025, 10, 18, 14, 45)},
    {'action': 'Reviewed mobile app features with Nathan Kim.', 'timestamp': datetime(2025, 10, 18, 11, 15)},
    {'action': 'Design review session with Olivia Patel.', 'timestamp': datetime(2025, 10, 17, 15, 0)},
    {'action': 'Set quarterly objectives for the team.', 'timestamp': datetime(2025, 10, 17, 9, 0)},
    {'action': 'Organized team building lunch.', 'timestamp': datetime(2025, 10, 16, 12, 30)},
    {'action': 'Approved promotion for Dana Scully.', 'timestamp': datetime(2025, 10, 15, 16, 0)},
    {'action': 'Career development discussion with Alice Johnson.', 'timestamp': datetime(2025, 10, 15, 10, 0)},
    {'action': 'Performance review with Bob Smith.', 'timestamp': datetime(2025, 10, 14, 14, 0)}
]