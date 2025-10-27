# 🚀 WorkWise AI - Employee Performance Management System

> **Ideathon 2 Project Submission**

WorkWise AI is a comprehensive employee performance management platform built with Flask. It provides managers with powerful tools to track team performance, assign goals, and gain AI-driven insights, while employees can monitor their personal progress and receive feedback.

## ✨ Features

### For Managers
- 📊 **Team Dashboard** - Overview of all team members' performance
- 👥 **Employee Detail View** - In-depth analysis of individual employees
- 🎯 **Goal Tracking** - Assign and monitor team goals
- 🏆 **Leaderboard** - Rank employees by performance metrics
- 💰 **Reward System** - Give bonuses and recognition
- 🤖 **AI Insights** - Smart analytics and recommendations
- 📝 **Feedback Management** - Receive and review team feedback

### For Employees
- 📈 **Personal Dashboard** - Track your own performance metrics
- 🎯 **Goal Progress** - View planned vs actual goal completion
- 💵 **Bonus Tracking** - Monitor earned bonuses
- 💬 **Give Feedback** - Provide feedback to managers
- 🤖 **AI Insights** - Personalized recommendations

### Core Functionality
- 🔐 **Secure Authentication** - Role-based access (Manager/Employee)
- 📊 **Interactive Charts** - Real-time performance visualizations using Chart.js
- 🌓 **Dark Mode** - Toggle between light and dark themes
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 💾 **SQLite Database** - Lightweight data storage

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLAlchemy with SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Charts:** Chart.js
- **Icons:** Material Icons
- **Authentication:** Werkzeug security

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Ameer-pasha/workwise-ai.git
cd workwise-ai
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
python app.py
```
The database will be automatically created with sample data on first run.

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 👤 Default Login Credentials

### Manager Account
- **Email:** manager@example.com
- **Password:** Password123!
- **Role:** Manager

### Employee Accounts
- **Email:** employee1@example.com (through employee50@example.com)
- **Password:** Password123!
- **Role:** Employee

## 📁 Project Structure

```
workwise-ai/
├── app.py                          # Main Flask application
├── workwise.db                     # SQLite database (auto-generated)
├── requirements.txt                # Python dependencies
├── .gitignore                     # Git ignore rules
├── README.md                      # Project documentation
│
├── static/
│   ├── css/
│   │   └── styles.css            # Main stylesheet
│   └── js/
│       ├── theme.js              # Dark mode functionality
│       ├── personal-goals-chart.js        # Personal dashboard chart
│       ├── teamPerformanceChart.js        # Team performance chart
│       └── employeePerformanceChart.js    # Employee detail chart
│
└── templates/
    ├── login.html                # Login page
    ├── your_dashboard.html       # Personal dashboard
    ├── team_dashboard.html       # Manager's team view
    ├── employee-detail-view.html # Individual employee details
    ├── insights.html             # AI insights page
    ├── leaderboard.html          # Employee rankings
    ├── feedback_form.html        # Feedback submission
    ├── feedback_received.html    # View received feedback
    └── feedback_given.html       # View given feedback
```

## 🎨 Key Components

### Database Models
- **User** - Stores user accounts (Manager/Employee)
- **Employee** - Detailed employee profiles and metrics
- **Goal** - Goal tracking system
- **Bonus** - Bonus and reward records
- **Feedback** - Feedback between users
- **LeadershipActivity** - Manager activity logs

### API Endpoints
- `/performance_data` - Team performance metrics
- `/personal_performance_data` - Individual goal tracking
- `/employee_performance_data/<id>` - Specific employee trends

## 🔧 Configuration

### Database
The application uses SQLite by default. To change the database:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
```

### Secret Key
For production, change the secret key in `app.py`:

```python
app.config['SECRET_KEY'] = 'your-secure-secret-key'
```

## 📊 Chart Implementations

### Personal Goals Chart
- Shows planned vs actual goal completion
- Weekly tracking
- Used on "Your Dashboard"

### Team Performance Chart
- Compares current vs previous week
- Shows all team members (for managers)
- Used on "AI Insights" page

### Employee Performance Chart
- Monthly trend analysis
- Current vs previous month comparison
- Used on "Employee Detail" page

## 🌟 Features in Detail

### Performance Scoring
- Score range: 0-100
- Factors: commits, tasks completed, work hours
- AI-generated summaries and recommendations

### Goal Management
- Set monthly/quarterly goals
- Track completion rates
- Visual progress indicators

### Reward System
- Monetary bonuses
- Recognition badges
- Gift vouchers

### Feedback System
- Anonymous feedback to managers
- Transparent feedback from managers
- Timestamped records

## 🐛 Troubleshooting

### Database Issues
If you encounter database errors, delete `workwise.db` and restart the app:
```bash
rm workwise.db  # or del workwise.db on Windows
python app.py
```

### Chart Not Displaying
1. Check browser console (F12) for errors
2. Verify Chart.js CDN is loading
3. Ensure the correct JavaScript file is loaded
4. Check API endpoint responses

### Login Issues
- Ensure you're using the correct role (Manager/Employee)
- Verify email and password are correct
- Check that the database is initialized

## 🔒 Security Notes

- Passwords are hashed using Werkzeug security
- Session-based authentication
- Role-based access control
- CSRF protection recommended for production

## 🚀 Future Enhancements

- [ ] Email notifications
- [ ] Real-time updates with WebSockets
- [ ] Advanced AI insights with ML models
- [ ] Integration with GitHub/Jira APIs
- [ ] Export reports to PDF
- [ ] Multi-language support
- [ ] Mobile app (React Native)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Team

This project was developed by:

**Ameer Pasha** - Project Lead
- GitHub: [@Ameer-pasha](https://github.com/Ameer-pasha)

**Prince**
- GitHub: [@Prince649294u83](https://github.com/Prince649294u83)

**Faizan (Shaik Zan)**
- GitHub: [@shaikzan](https://github.com/shaikzan)

**Tarun (Silent Ghost)**
- GitHub: [@SilentGhost25](https://github.com/SilentGhost25)

## 🙏 Acknowledgments

- Chart.js for beautiful charts
- Material Icons for UI icons
- Flask community for excellent documentation
- Our mentors and supporters at Ideathon 2

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, open an issue on GitHub or contact the team members directly.

---

**Made with ❤️ by Team WorkWise AI | Ideathon 2 Project**