from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret'

def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (email, password, role))
            conn.commit()
        except:
            return "User already exists"
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['email'] = user[1]
            session['role'] = user[3]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    if session['role'] == 'teacher':
        return render_template('teacher_dashboard.html')
    else:
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("SELECT subject, score FROM results WHERE student_email=?", (session['email'],))
        results = c.fetchall()
        conn.close()
        return render_template('student_dashboard.html', results=results)

@app.route('/upload_result', methods=['POST'])
def upload_result():
    if 'email' in session and session['role'] == 'teacher':
        student_email = request.form['student_email']
        subject = request.form['subject']
        score = request.form['score']
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("INSERT INTO results (student_email, subject, score) VALUES (?, ?, ?)", (student_email, subject, score))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return "Unauthorized"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
