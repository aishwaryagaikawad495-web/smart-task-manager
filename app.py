from flask import Flask, render_template, session,redirect,request,flash
from datetime import datetime

app = Flask(__name__)
app.secret_key="mysecretkey"


import sqlite3

conn = sqlite3.connect("data.db")
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
        deadline TEXT
    )
    """)

# Create default admin user
c.execute("SELECT * FROM users WHERE username=?", ('admin',))
admin = c.fetchone()

if admin:
    c.execute("UPDATE users SET role='admin',password='admin123' WHERE username='admin'")
    print("✅ Admin updated")

else:
    c.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, ('admin', 'admin123', 'admin'))

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

        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))

        user = c.fetchone()
        conn.close()

        if user:
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
                  (username, password, "user"))

        conn.commit()
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

        c.execute("INSERT INTO tasks (username, task,deadline) VALUES (?, ?,?)",
                  (username, task,deadline))
        conn.commit()

    #  Show tasks for logged-in user
    c.execute("SELECT * FROM tasks WHERE username=?",
              (session['user'],))
    data = c.fetchall()

    conn.close()
    today = datetime.now().date()

    updated_tasks = []

    for task in data:

        deadline_date = datetime.strptime(
            task[4],
            "%Y-%m-%d"
    ).date()

        updated_tasks.append(
        (
            task[0],
            task[1],
            task[2],
            task[3],
            deadline_date
        )
    )
    return render_template('tasks.html', tasks=updated_tasks,today=today)



@app.route('/complete/<int:id>')
def complete_task(id):

    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute(
    "UPDATE tasks SET status='completed' WHERE id=? AND username=?",
    (id, session['user'])
)

    conn.commit()
    conn.close()

    return redirect('/tasks')


@app.route('/delete/<int:id>')
def delete_task(id):
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute(
    "DELETE FROM tasks WHERE id=? AND username=?",
    (id, session['user'])
)

    conn.commit()
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


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)








