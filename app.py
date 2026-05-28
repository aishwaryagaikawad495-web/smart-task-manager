from flask import Flask, render_template, session,redirect,request,flash, send_file
from datetime import datetime,timedelta
from collections import Counter
from werkzeug.security import generate_password_hash, check_password_hash
import re

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def add_history(username, action):

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    c.execute("""
        INSERT INTO history (username, action, created_at)
        VALUES (?, ?, ?)
    """, (username, action, created_at))

    conn.commit()
    conn.close()


def is_strong_password(password):
    """
    Returns (True, message) if password is strong
    Returns (False, error_message) if weak
    """

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"

    return True, "Password is strong"

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
# app.secret_key="mysecretkey"
import os
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret")

import sqlite3

with sqlite3.connect("data.db") as conn:
    c = conn.cursor()

#user table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'user'
)
""")
#tasks table
c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        task TEXT,
        status TEXT DEFAULT 'pending',
        deadline TEXT,
        priority TEXT DEFAULT 'Medium',
        created_at TEXT,
        completed_at TEXT
    )
    """)

#History table
c.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT,
    created_at TEXT
)
""")

# Create default admin user
c.execute("SELECT * FROM users WHERE username=?", ('admin',))
admin = c.fetchone()

# if admin:
#     c.execute("UPDATE users SET role='admin',password='admin123' WHERE username='admin'")
#     print("✅ Admin updated")

# else:
#     c.execute("""
#         INSERT INTO users (username, password, role)
#         VALUES (?, ?, ?)
#     """, ('admin', 'admin123', 'admin'))

#     print("✅ Admin created")
hashed_admin = generate_password_hash("Abcd1234@")

if admin:
    c.execute(
        "UPDATE users SET role=?, password=? WHERE username=?",
        ('admin', hashed_admin, 'admin')
    )
    print("✅ Admin updated")

else:
    c.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, ('admin', hashed_admin, 'admin'))

    print("✅ Admin created")

conn.commit()
conn.close()



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=?",
                  (username,))

        user = c.fetchone()
        if user and check_password_hash(user[2], password):
            add_history(username, "Logged into account")
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user'] = user[1]   # username
            session['role'] = user[3]   # role
            flash("✅ Login Successful", "success")
            if user[3] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/tasks')
        else:
            flash("❌ Invalid Credentials","error")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_valid, message = is_strong_password(password)

        if not is_valid:
            flash(message, "error")
            return redirect('/register')

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        # Check if user already exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            flash("❌ Username already exists. Try another one.", "error")
            return redirect('/register')

        # Insert new user
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, hashed_password, "user"))

        conn.commit()
        add_history(username, "Registered new account")
        conn.close()
        flash("✅ Registration successful! Please login.", "success")

        return redirect('/login')

    return render_template('register.html')



@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #  Add task
    if request.method == 'POST':
        task = request.form['task']
        deadline = request.form['deadline']
        username = session['user']
        priority = request.form["priority"]

        created_at = datetime.now().strftime("%Y-%m-%d")

        c.execute("""
            INSERT INTO tasks
            (username, task, deadline, priority, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, task, deadline, priority, created_at))
        conn.commit()
        add_history(username, f'Added task "{task}"')

    #  Show tasks for logged-in user
    c.execute("SELECT * FROM tasks WHERE username=?",
              (session['user'],))
    data = c.fetchall()

    conn.close()
    today = datetime.now().date()

    updated_tasks = []

    for task in data:
        try:
            deadline_date = datetime.strptime(task[4], "%Y-%m-%d").date()
        except ValueError:
            deadline_date = None

        updated_tasks.append(
        (
            task[0],#id
            task[1],#username
            task[2],#task
            task[3],#status
            deadline_date,
            task[5] #priority
        )
    )
    return render_template('tasks.html', tasks=updated_tasks,today=today)


@app.route('/search')
def search_tasks():

    if 'user' not in session:
        return redirect('/login')

    query = request.args.get('query', '').strip()

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    # ADMIN SEARCH
    if session.get('role') == 'admin':

        c.execute("""
            SELECT * FROM tasks
            WHERE task LIKE ?
        """, ('%' + query + '%',))

    # USER SEARCH
    else:

        c.execute("""
            SELECT * FROM tasks
            WHERE username=? AND task LIKE ?
        """, (session['user'], '%' + query + '%'))

    tasks = c.fetchall()

    conn.close()

    today = datetime.now().date()

    updated_tasks = []

    for task in tasks:

        try:
            deadline_date = datetime.strptime(
                task[4],
                "%Y-%m-%d"
            ).date()

        except:
            deadline_date = None

        updated_tasks.append((
            task[0],
            task[1],
            task[2],
            task[3],
            deadline_date,
            task[5]
        ))

    return render_template(
        'tasks.html',
        tasks=updated_tasks,
        today=today,
        search_query=query
    )


@app.route('/complete/<int:id>')
def complete_task(id):

    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    completed_at = datetime.now().strftime("%Y-%m-%d")

    c.execute(
    "SELECT task FROM tasks WHERE id=? AND username=?",
    (id, session['user'])
    )

    task_data = c.fetchone()

    task_name = task_data[0]

    c.execute("""
        UPDATE tasks
        SET status='completed',
        completed_at=?
        WHERE id=? AND username=?
        """,
        (completed_at, id, session['user'])
    )

    conn.commit()
    add_history(session['user'],f'Completed task "{task_name}"')
    conn.close()

    return redirect('/tasks')


@app.route('/delete/<int:id>')
def delete_task(id):
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute(
    "SELECT task FROM tasks WHERE id=? AND username=?",
    (id, session['user'])
)

    task_data = c.fetchone()

    task_name = task_data[0]
    c.execute(
    "DELETE FROM tasks WHERE id=? AND username=?",
    (id, session['user'])
)

    conn.commit()
    add_history(
    session['user'],f'Deleted task "{task_name}"')
    conn.close()

    return redirect('/tasks')


@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "❌ Access Denied"

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    # All tasks
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()

    # Total tasks
    c.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = c.fetchone()[0]

    # Pending tasks
    c.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'")
    pending_tasks = c.fetchone()[0]

    # Completed tasks
    c.execute("SELECT COUNT(*) FROM tasks WHERE status='completed'")
    completed_tasks = c.fetchone()[0]

    # Total users
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]


    conn.close()

    return render_template(
        'admin.html',
        tasks=tasks,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        total_users=total_users
    )



@app.route('/profile')
def profile():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    username = session['user']

    # Total tasks
    c.execute(
        "SELECT COUNT(*) FROM tasks WHERE username=?",
        (username,)
    )
    total_tasks = c.fetchone()[0]

    # Completed tasks
    c.execute(
        "SELECT COUNT(*) FROM tasks WHERE username=? AND status='completed'",
        (username,)
    )
    completed_tasks = c.fetchone()[0]

    # Pending tasks
    c.execute(
        "SELECT COUNT(*) FROM tasks WHERE username=? AND status='pending'",
        (username,)
    )
    pending_tasks = c.fetchone()[0]


    if total_tasks > 0:
        completion_percentage = int(
            (completed_tasks / total_tasks) * 100
        )
    else:
        completion_percentage = 0


# User Level
    if completed_tasks >= 20:
        user_level = "Task Master"

    elif completed_tasks >= 10:
        user_level = "Productive User"

    else:
        user_level = "Beginner"


    conn.close()

    return render_template(
    'profile.html',

    username=username,
    role=session['role'],

    total_tasks=total_tasks,
    completed_tasks=completed_tasks,
    pending_tasks=pending_tasks,

    completion_percentage=completion_percentage,
    user_level=user_level
)


@app.route('/get-started')
def get_started():

    if 'user' in session:
        return redirect('/tasks')

    return redirect('/register')




@app.route("/edit/<int:id>", methods=["GET", "POST"])

def edit_task(id):
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    if request.method == "POST":

        updated_task = request.form["task"]
        updated_deadline = request.form["deadline"]
        updated_priority = request.form["priority"]

        c.execute(
        "SELECT task FROM tasks WHERE id=? AND username=?",
        (id, session['user'])
        )

        old_task = c.fetchone()[0]
        c.execute(
            """
            UPDATE tasks
            SET task=?, deadline=?, priority=?
            WHERE id=? AND username=?
            """,
            (updated_task, updated_deadline, updated_priority, id, session['user'])
        )

        conn.commit()
        add_history(
    session['user'],f'Edited task "{old_task}" to "{updated_task}"')
        conn.close()

        return redirect("/tasks")

    c.execute(
        "SELECT * FROM tasks WHERE id=? AND username=?",
        (id, session['user'])
    )
    task = c.fetchone()

    conn.close()

    return render_template("edit_task.html", task=task)


@app.route('/weekly-report')
def weekly_report():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    username = session['user']

    # Get all tasks of user
    c.execute(
        "SELECT * FROM tasks WHERE username=?",
        (username,)
    )

    tasks = c.fetchall()

    conn.close()

    total_tasks = len(tasks)

    completed_tasks = 0
    pending_tasks = 0
    overdue_tasks = 0

    high_priority = 0
    medium_priority = 0
    low_priority = 0

    today = datetime.now().date()

    completed_days = []
    
    weekly_chart = {
        "Mon": 0,
        "Tue": 0,
        "Wed": 0,
        "Thu": 0,
        "Fri": 0,
        "Sat": 0,
        "Sun": 0
    }


    for task in tasks:
        status = task[3]
        deadline = task[4]
        priority = task[5]

        # Completed / Pending
        if status == "completed":
            completed_tasks += 1
        else:
            pending_tasks += 1

        # Overdue
        if deadline and status != "completed":

            try:
                deadline_date = datetime.strptime(
                    deadline,
                    "%Y-%m-%d"
                ).date()

                if deadline_date < today:
                    overdue_tasks += 1

            except ValueError:
                pass

        # Priority Count
        if priority == "High":
            high_priority += 1

        elif priority == "Medium":
            medium_priority += 1

        elif priority == "Low":
            low_priority += 1

        # Weekly chart
        completed_at = task[7]

        if status == "completed" and completed_at:

            try:
                date_obj = datetime.strptime(
                    completed_at,
                    "%Y-%m-%d"
                )

                day_name = date_obj.strftime("%a")

                if day_name in weekly_chart:
                    weekly_chart[day_name] += 1

                completed_days.append(day_name)

            except ValueError:
                pass

    weekly_values = list(weekly_chart.values())
    total_week_activity = sum(weekly_values)
    # Productivity
    if total_tasks > 0:
        productivity = int(
            (completed_tasks / total_tasks) * 100
        )
    else:
        productivity = 0


    if productivity >= 80:
        insight = "🔥 Excellent Productivity"
    elif productivity >= 50:
        insight = "👍 Good Performance"
    else:
        insight = "⚠️ Needs Improvement"

    # Most productive day
    if completed_days:
        most_productive_day = Counter(
            completed_days
        ).most_common(1)[0][0]
    else:
        most_productive_day = "No Data"


    completion_streak = 0
    sorted_dates = []

    for task in tasks:

        completed_at = task[7]

        if completed_at:

            try:

                completed_date = datetime.strptime(
                completed_at,
                "%Y-%m-%d"
                ).date()

                sorted_dates.append(completed_date)

            except ValueError:
                pass

    sorted_dates = sorted(set(sorted_dates), reverse=True)

    current_day = today

    for d in sorted_dates:

        if d == current_day:

            completion_streak += 1
            current_day = current_day - timedelta(days=1)

        else:
            break

    completion_durations = []

    for task in tasks:

        created_at = task[6]
        completed_at = task[7]

        if created_at and completed_at:

            try:

                    created_date = datetime.strptime(
                    created_at,
                "%Y-%m-%d"
            )

                    completed_date = datetime.strptime(
                completed_at,
                "%Y-%m-%d"
            )

                    diff = (
                completed_date - created_date
            ).days

                    completion_durations.append(diff)

            except ValueError:
                pass

    if completion_durations:

        avg_days = sum(completion_durations) / len(completion_durations)

        avg_completion_time = f"{round(avg_days, 1)} Days"

    else:

        avg_completion_time = "0 Days"
    

    # Overdue %
    if total_tasks > 0:
        overdue_percentage = int(
            (overdue_tasks / total_tasks) * 100
        )
    else:
        overdue_percentage = 0
    return render_template(

        "weekly_report.html",

        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks,

        productivity=productivity,

        weekly_chart=weekly_chart,

        high_priority=high_priority,
        medium_priority=medium_priority,
        low_priority=low_priority,

        most_productive_day=most_productive_day,

        completion_streak=completion_streak,

        avg_completion_time=avg_completion_time,

        overdue_percentage=overdue_percentage,
        weekly_values=weekly_values,
        total_week_activity=total_week_activity,
        insight=insight
    )


@app.route('/history')
def history():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    # ADMIN
    if session.get('role') == 'admin':

        c.execute("""
            SELECT username, action, created_at
            FROM history
            ORDER BY id DESC
        """)

    # USER
    else:

        c.execute("""
            SELECT username, action, created_at
            FROM history
            WHERE username=?
            ORDER BY id DESC
        """, (session['user'],))

    history_data = c.fetchall()
    # Total logs
    total_logs = len(history_data)

# Completed count
    completed_count = len([
        x for x in history_data
        if "Completed" in x[1]
        ])

# Deleted count
    deleted_count = len([
        x for x in history_data
        if "Deleted" in x[1]
        ])
    conn.close()
#Edited count
    edited_count = len([
        x for x in history_data
        if "Edited task" in x[1]
        ])
        
    return render_template(
    "history.html",
    history_data=history_data,
    total_logs=total_logs,
    completed_count=completed_count,
    deleted_count=deleted_count,
    edited_count=edited_count
)



@app.route('/download-report')
def download_report():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    username = session['user']

    c.execute("SELECT * FROM tasks WHERE username=?", (username,))
    tasks = c.fetchall()
    conn.close()

    total_tasks = len(tasks)
    completed_tasks = 0
    pending_tasks = 0
    overdue_tasks = 0

    today = datetime.now().date()

    high_priority = 0
    medium_priority = 0
    low_priority = 0

    weekly_chart = {
        "Mon": 0,
        "Tue": 0,
        "Wed": 0,
        "Thu": 0,
        "Fri": 0,
        "Sat": 0,
        "Sun": 0
    }

    completed_days = []

    # ---------------- DATA PROCESSING ----------------
    for task in tasks:
        status = task[3]
        deadline = task[4]
        priority = task[5]
        completed_at = task[7]

        # status
        if status == "completed":
            completed_tasks += 1
        else:
            pending_tasks += 1

        # overdue
        if deadline and status != "completed":
            try:
                d = datetime.strptime(deadline, "%Y-%m-%d").date()
                if d < today:
                    overdue_tasks += 1
            except:
                pass

        # priority
        if priority == "High":
            high_priority += 1
        elif priority == "Medium":
            medium_priority += 1
        elif priority == "Low":
            low_priority += 1

        # weekly chart
        if status == "completed" and completed_at:
            try:
                date_obj = datetime.strptime(completed_at, "%Y-%m-%d")
                day = date_obj.strftime("%a")
                if day in weekly_chart:
                    weekly_chart[day] += 1
                    completed_days.append(day)
            except:
                pass

    productivity = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

    insight = (
        "🔥 Excellent Productivity" if productivity > 80
        else "👍 Good Performance" if productivity > 50
        else "⚠️ Needs Improvement"
    )

    # ---------------- PDF START ----------------
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # ✔ 1. TITLE
    elements.append(Paragraph(
        "<b>Smart Task Manager - Weekly Report</b>",
        styles['Title']
    ))
    elements.append(Spacer(1, 20))

    # ✔ 2. USER INFO
    elements.append(Paragraph(f"<b>User:</b> {username}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # ✔ 3. AI INSIGHT
    elements.append(Paragraph(f"<b>AI Insight:</b> {insight}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # ✔ 4. SUMMARY TABLE
    summary_data = [
        ["Metric", "Value"],
        ["Total Tasks", total_tasks],
        ["Completed", completed_tasks],
        ["Pending", pending_tasks],
        ["Overdue", overdue_tasks],
        ["Productivity", f"{productivity}%"]
    ]

    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # ✔ 5. PRIORITY TABLE
    priority_data = [
        ["Priority", "Count"],
        ["High", high_priority],
        ["Medium", medium_priority],
        ["Low", low_priority]
    ]

    priority_table = Table(priority_data)
    priority_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkred),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(priority_table)
    elements.append(Spacer(1, 20))

    # ✔ 6. WEEKLY BREAKDOWN (FIXED)
    elements.append(Paragraph("<b>Weekly Activity Breakdown</b>", styles['Heading2']))

    for day, value in weekly_chart.items():
        elements.append(Paragraph(f"{day}: {value} tasks", styles['Normal']))

    elements.append(Spacer(1, 20))

    # ✔ 7. TASK TABLE
    task_data = [["Task", "Status", "Priority", "Deadline"]]

    for task in tasks:
        task_data.append([task[2], task[3], task[5], task[4]])

    task_table = Table(task_data)
    task_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.green),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(task_table)

    # BUILD PDF
    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer,
                     as_attachment=True,
                     download_name="Weekly_Report.pdf",
                     mimetype="application/pdf")





@app.route('/logout')
def logout():
    if 'user' in session:
        add_history(session['user'], "Logged out")
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)








