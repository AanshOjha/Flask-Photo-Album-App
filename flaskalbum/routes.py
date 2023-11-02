import os
import smtplib
from flask import render_template, request, url_for, redirect, session, flash
from flaskalbum import app, bcrypt, mysql
from flaskalbum.models import User

# Create an instance of the User class from models.py
user = User()

# Route for the home page (login page)
@app.route('/')
def index(): 
    return render_template('login.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve user registration form data
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Call register_user method to handle user registration
        message = user.register_user(name, email, username, password)
        flash(message, 'danger' if 'error' in message.lower() else 'success')
        if 'success' in message.lower():
            return redirect('/')

    # Render the registration form for GET requests
    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Retrieve user login form data
        username = request.form['username']
        password = request.form['password']

        # Retrieve user data from the database and validate login credentials
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username, password FROM creds WHERE username = %s OR email = %s", (username, username))
        user_row = cursor.fetchone()

        # Check if the user exists and the password is correct
        if user_row and bcrypt.check_password_hash(user_row[1], password):
            # Store the username in the session and redirect to the home page
            session['username'] = user_row[0]
            return redirect('/home')
        else:
            # Display an error message for unsuccessful login attempts
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect('/')
        
    # Render the login page for GET requests
    return render_template('login.html', title='Login')

# Route for the home page after successful login
@app.route('/home')
def home():
    # Check if the user is logged in, if not, redirect to the login page
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect('/')

# Route for user logout
@app.route('/logout')
def logout():
    # Remove the username from the session and redirect to the home page
    session.pop('username', None)
    return redirect('/')

# Function to send a password reset email to the user
def send_reset_email(user):
    # Generate a password reset token and construct the reset email content
    token = user.get_reset_token()
    
    # Email configuration and content
    email_user = os.environ.get('EMAIL_ID')
    email_pwd = os.environ.get('EMAIL_PASS')

    TO = [user.email]
    SUBJECT = "Password Reset Request"
    TEXT = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    
    This link is valid for 10 minutes.
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    server = smtplib.SMTP('smtp.zoho.in', 587)
    server.ehlo()
    server.starttls()
    server.login(email_user, email_pwd)
    BODY = '\r\n'.join(['To: %s' % TO,
            'From: %s' % email_user,
            'Subject: %s' % SUBJECT,
            '', TEXT])
    
    # Send the email using SMTP
    server.sendmail(email_user, [TO], BODY)

# Route for initiating a password reset request
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        if email:
            cursor = mysql.connection.cursor()

            # Check if the provided email address exists in the database
            cursor.execute("SELECT email FROM creds WHERE email = %s", (email,))
            user_email = cursor.fetchone()

            # If no user found with the provided email, display a warning message
            if user_email is None:
                flash('No user found with that email address.', 'warning')
                return redirect('/reset_password')

            # Create a User object and send the password reset email
            user = User()
            user.email = user_email[0]
            send_reset_email(user)

            # Display a success message and redirect to the login page
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect('/login')
        
    # Render the password reset request form for GET requests
    return render_template('reset_request.html', title='Reset Password')

# Route for handling password reset with the provided token
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # Verify the reset token
    user = User.verify_reset_token(token)
    
    # Check if the token is invalid or expired
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/')
    
    # Handle POST request for password reset
    if request.method == 'POST':
        email = user

        # Retrieve and update the user's password
        password = request.form['password']
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE creds SET password = %s WHERE email = %s", (hashed_password, email))
            mysql.connection.commit()

            # Display a success message and redirect to the login page
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect('/login')
    
    # Render the password reset form for GET requests
    return render_template('reset_token.html', title='Reset Password')