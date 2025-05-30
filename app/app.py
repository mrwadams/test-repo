from flask import Flask, request, render_template_string, redirect, session, send_file
import sqlite3
import os
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'hardcoded-secret-key-123'  # Security issue: hardcoded secret

# Insecure file upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'exe', 'sh', 'py'}  # Security issue: allowing executable files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB - too large

# Database setup with security issues
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Security issue: storing passwords in plain text or weak hash
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            role TEXT
        )
    ''')
    # Security issue: default admin with weak password
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email, role) VALUES ('admin', 'admin123', 'admin@example.com', 'admin')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Security issue: reflecting user input without sanitization
    name = request.args.get('name', 'Guest')
    template = f'''
        <h1>Welcome {name}!</h1>
        <a href="/login">Login</a><br>
        <a href="/upload">Upload File</a><br>
        <a href="/profile">Profile</a>
    '''
    return render_template_string(template)  # Security issue: SSTI vulnerability

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Security issue: SQL injection vulnerability
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[4]
            return redirect('/profile')
        else:
            return 'Invalid credentials'
    
    return '''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/profile')
def profile():
    # Security issue: no authentication check
    user_id = request.args.get('user_id', session.get('user_id'))
    
    if user_id:
        # Security issue: SQL injection via user_id parameter
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Security issue: exposing sensitive user data
            return f'''
                <h2>User Profile</h2>
                ID: {user[0]}<br>
                Username: {user[1]}<br>
                Password Hash: {user[2]}<br>
                Email: {user[3]}<br>
                Role: {user[4]}
            '''
    
    return 'Please login first'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        
        if file:
            # Security issue: not properly validating file extension
            filename = file.filename  # Not using secure_filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Security issue: potential path traversal
            file.save(filepath)
            
            # Security issue: executing uploaded files
            if filename.endswith('.py'):
                os.system(f'python {filepath}')  # Extremely dangerous!
            
            return f'File uploaded successfully: {filename}'
    
    return '''
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    '''

@app.route('/download')
def download():
    # Security issue: path traversal vulnerability
    filename = request.args.get('file')
    if filename:
        # No validation of filename - allows ../../../etc/passwd
        return send_file(filename)
    return 'No file specified'

@app.route('/admin')
def admin():
    # Security issue: weak authorization check
    if session.get('role') == 'admin' or request.args.get('admin') == 'true':
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        
        result = '<h2>Admin Panel - All Users</h2>'
        for user in users:
            result += f'{user}<br>'
        
        return result
    
    return 'Access denied'

@app.route('/search')
def search():
    # Security issue: command injection
    query = request.args.get('q', '')
    if query:
        # Dangerous - allows command injection
        result = os.popen(f'grep -r "{query}" .').read()
        return f'<pre>{result}</pre>'
    
    return '''
        <form>
            Search: <input name="q">
            <input type="submit">
        </form>
    '''

if __name__ == '__main__':
    init_db()
    # Security issue: debug mode enabled in production
    app.run(debug=True, host='0.0.0.0', port=5000)