from flask import Flask, render_template, session,redirect

app = Flask(__name__)
app.secret_key="mysecretkey"
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    session['user']="Aishwarya"
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)








