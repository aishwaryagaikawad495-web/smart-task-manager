# smart-task-manager( Flask + SQlite)

A simple web application built using Flask, SQLite, HTML, CSS, and JavaScript.  
Users can register, login, manage tasks, and admins can monitor all tasks through an admin dashboard.

# Features
- User Registration system
- User Login and Logout
- SQLite database integration
- Session-based authentication
- Password visibility toggle
- Clean and responsive UI design
-Admin Dashboard
-User Profile dashboard
-Flash messages
-Create, Read, Update, Delete (CRUD) Tasks
-Task deadlines support

# Tech Stack
- Python 
-Flask
- SQLite3
- HTML5
- CSS3
- JavaScript

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
│
├── /static
│   ├── style.css
│   └── script.js
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
Password: admin123
```

---

# Future Improvements

- Password Hashing
- Task Categories
- Email Authentication
- REST API Integration
- Dark Mode
- Deployment on Render/Heroku

---

# Author

Aishwarya Gaikawad