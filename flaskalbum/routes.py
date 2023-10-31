import smtplib
from flask import render_template, request, url_for, redirect, session, flash
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

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
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
        
    return render_template('login.html', title='Login')
    
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


def send_reset_email(user):
    token = user.get_reset_token()
    email_user = "aanshojha@zohomail.in"
    email_pwd = "Chalhatt@109"
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
    
    server.sendmail(email_user, [TO], BODY)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        if email:
            cursor = mysql.connection.cursor()

            cursor.execute("SELECT email FROM creds WHERE email = %s", (email,))
            user_email = cursor.fetchone()

            if not user_email:
                flash('No user found with that email address.', 'warning')
                return redirect('/reset_request')

            user = User()
            user.email = user_email[0]

            send_reset_email(user)

            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect('/login')
        
    return render_template('reset_request.html', title='Reset Password')


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):

    # Verify the reset token
    user = User.verify_reset_token(token)
    
    # Check if the token is invalid or expired
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/')
    

    if request.method == 'POST':

        email = user

        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect('/')

        password = request.form['password']

        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE creds SET password = %s WHERE email = %s", (hashed_password, email))
            mysql.connection.commit()

            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect('/login')
    return render_template('reset_token.html', title='Reset Password')
