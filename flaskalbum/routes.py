from flask import render_template, request, redirect, session, flash
from flaskalbum import app, bcrypt, mysql
from flaskalbum.models import User
from envconfig import MYSQL_TABLE
from flaskalbum.utils import send_reset_email

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

        authenticated_user = user.authenticate_user(username, password)

        # Check if the user exists and the password is correct
        if authenticated_user:
            # Store the username in the session and redirect to the home page
            session['username'] = authenticated_user
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

# Route for initiating a password reset request
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        if email:
            user_data = user.get_user_by_email(email)

            # If no user found with the provided email, display a warning message
            if user_data is None:
                flash('No user found with that email address.', 'warning')
                return redirect('/reset_password')

            # Send the password reset email
            user.email = user_data[1]
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
    email_from_token = user.verify_reset_token(token)
    
    # Check if the token is invalid or expired
    if email_from_token is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/')
    
    # Handle POST request for password reset
    if request.method == 'POST':
        # Retrieve and update the user's password
        password = request.form['password']
        if password:
            user.update_password(email_from_token, password)

            # Display a success message and redirect to the login page
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect('/login')
    
    # Render the password reset form for GET requests
    return render_template('reset_token.html', title='Reset Password')