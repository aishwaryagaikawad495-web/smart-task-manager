# smart-task-manager( Flask + SQlite)

A simple web application built using Flask, SQLite, HTML, CSS, and JavaScript.  
Users can register, login, manage tasks, and admins can monitor all tasks through an admin dashboard.This project helps users manage tasks efficiently with analytics, deadlines, priorities, dark mode, and productivity tracking.

# Features
### 🔐 Authentication & Security
- User Registration & Login
- Secure Password Hashing
- Strong Password Validation
- Session Management
- Admin Role Access

### 📋 Task Management
- Add Tasks
- Edit Tasks
- Delete Tasks
- Mark Tasks as Completed
- Priority Levels (High / Medium / Low)
- Automatic Overdue Detection

### 📊 Productivity Analytics
- Weekly Productivity Dashboard
- Doughnut & Line Charts
- Weekly Completion Trends
- Productivity Percentage
- Most Productive Day
- Completion Streak Tracking
- Overdue Task Analytics

### 📄 PDF Reporting
- Download Weekly Productivity Reports
- Task Summary Tables
- Priority Analysis
- Weekly Activity Breakdown

### 🎨 UI Features
- Dark Mode
- Responsive Dashboard
- Animated Charts & Progress Bars
- Admin Dashboard Navigation

# Tech Stack
### Backend
- Python
- Flask
- SQLite3
- Werkzeug

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js
- Jinja2

### PDF Generation
- ReportLab



# Project Structure
Smart-Task-Manager/
│
├── app.py
├── data.db   (optional to include)
├── requirements.txt
│
├── /templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── tasks.html
│   ├── admin.html
│   ├── profile.html
│   ├── base.html
|   ├── edit_task.html
|   ├── weekly_report.html
│
├── /static
│   ├── style.css
│   └── script.js
│   └── script1.js
│
└── README.md

# How to Run This Project
## 1. Clone Repository

```bash
git clone <your-github-repo-link>
```

## 2. Navigate to Project Folder

```bash
cd Smart-Task-Manager
```

## 3. Create Virtual Environment

```bash
python -m venv venv
```

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## 5. Install Dependencies

```bash
pip install flask
```

or

```bash
pip install -r requirements.txt
```

## 6. Run Application

```bash
python app.py
```

## 7. Open in Browser

```bash
http://127.0.0.1:5000/
```

---

# Default Admin Credentials

```bash
Username: admin
Password: Abcd1234@
```

---

# Future Improvements
- Task Categories
- Email Authentication
- REST API Integration
- Deployment on Render/Heroku
-AI Task Suggestions
-Calendar Integration
-Team Collaboration
-Email reminder

---

# Author

Aishwarya Gaikawad