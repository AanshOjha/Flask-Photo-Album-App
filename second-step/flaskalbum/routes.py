from flask import render_template, request, redirect, session, flash
from flaskalbum import app, bcrypt, mysql
from flaskalbum.models import User

user = User()

@app.route('/')
def index(): 
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        message = user.register_user(name, email, username, password)
        flash(message, 'danger' if 'error' in message.lower() else 'success')
        if 'success' in message.lower():
            return redirect('/')

    # For GET requests
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username, password FROM creds WHERE username = %s", (username,))
    user_row = cursor.fetchone()

    if user_row and bcrypt.check_password_hash(user_row[1], password):
        session['username'] = user_row[0]
        return redirect('/home')
    else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
        return redirect('/')
    
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')