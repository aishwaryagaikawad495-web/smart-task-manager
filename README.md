# 🚀 Smart Task Manager

A full-stack productivity and task management web application built with **Flask, SQLite, HTML, CSS, and JavaScript**. The application helps users efficiently organize tasks, track productivity, analyze performance trends, and improve workflow through analytics, notifications, and AI-powered suggestions.

Designed with scalability and user experience in mind, the project includes secure authentication, task analytics, PDF reporting, activity tracking, and an admin dashboard for system monitoring.

---

## ✨ Key Features

### 🔐 Authentication & Security

* User Registration & Login
* Secure Password Hashing using Werkzeug
* Strong Password Validation
* Session-Based Authentication
* Role-Based Access Control (Admin/User)

### 📋 Task Management

* Create, Update, and Delete Tasks
* Mark Tasks as Completed
* Priority Levels (High, Medium, Low)
* Automatic Overdue Task Detection
* Task Search Functionality

### 🤖 AI-Powered Task Suggestions

* Intelligent task recommendations
* Productivity improvement suggestions
* Smart guidance based on task activity

### 📜 Activity History

Track all important user actions:

* Task Creation
* Task Updates
* Task Deletion
* Task Completion
* User Login Events
* User Logout Events

### 🏅 Professional Achievement System
* Task Completion Milestone Badges
* Productivity Performance Recognition
* Zero Backlog Achievement Tracking
* Workflow Management Milestones
* Dynamic Badge Unlocking
* Real-Time Achievement Updates
* User Progress Recognition
* Professional Profile Showcase

### 📊 Productivity Analytics

* Weekly Productivity Dashboard
* Task Completion Trends
* Productivity Percentage Calculation
* Most Productive Day Analysis
* Completion Streak Tracking
* Overdue Task Statistics
* Interactive Charts and Visualizations

### 🔔 Smart Notifications

* Due Today Reminders
* Overdue Task Alerts
* Unread Notification Counter
* Automatic Notification Status Updates

### 📄 PDF Report Generation

Generate downloadable productivity reports containing:

* Weekly Task Summary
* Priority Distribution Analysis
* Activity Breakdown
* Performance Insights

### 👤 User Profile Management

* Profile Photo Upload
* Profile Editing
* Personalized Dashboard Experience

### 🛠️ Admin Dashboard

* Monitor Users
* View Task Statistics
* Track Platform Activity
* Administrative Controls

---

## 🏗️ Technology Stack

### Backend

* Python
* Flask
* SQLite
* Werkzeug Security

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates
* Chart.js

### Reporting

* ReportLab (PDF Generation)

---

## 📂 Project Structure

```text
Smart-Task-Manager/
│
├── app.py
├── requirements.txt
├── data.db
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── tasks.html
│   ├── history.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── edit_task.html
│   ├── notifications.html
│   ├── weekly_report.html
│   └── admin.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── script1.js
│   └── uploads/
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Navigate to the Project Directory

```bash
cd Smart-Task-Manager
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

```text
http://127.0.0.1:5000
```

---

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Full-Stack Web Development
* Flask Application Development
* Authentication & Authorization
* Database Management with SQLite
* Data Visualization
* PDF Report Generation
* AI Feature Integration
* Responsive UI Design
* Software Project Organization

---

## 🚀 Future Enhancements

* Task Categories & Labels
* Email Verification
* Email Reminders
* Team Collaboration
* REST API Development
* Cloud Deployment
* Calendar Integration
* Advanced AI Productivity Insights

---

## 👩‍💻 Author

**Aishwarya Gaikawad**

Aspiring Software Developer passionate about building practical web applications using Python, Flask, and modern web technologies.
