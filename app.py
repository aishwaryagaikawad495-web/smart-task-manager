from flask import Flask, render_template, session,redirect,request

app = Flask(__name__)
app.secret_key="mysecretkey"


import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'user'
)
""")

conn.commit()
conn.close()




@app.route('/')
def home():
    return render_template('index.html')


# ✅ LOGIN (GET + POST)
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
            return redirect('/')

        return "❌ Invalid Credentials"

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        # 🔴 Check if user already exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            return "❌ Username already exists. Try another one."

        # ✅ Insert new user
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, password, "user"))

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)








