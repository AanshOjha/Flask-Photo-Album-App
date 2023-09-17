from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong secret key

# MySQL Configuration 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Alskdj@185'
app.config['MYSQL_DB'] = 'credentials'

mysql = MySQL(app)

@app.route('/')
def index(): 
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM creds WHERE username = %s", (username,))
    user_row = cursor.fetchone()

    if user_row:
        # Get the column names and their corresponding indices
        column_names = [desc[0] for desc in cursor.description]
        id_index = column_names.index('id') 
        password_index = column_names.index('password')

        # Check if the password matches
        if password_index >= 0 and user_row[password_index] == password:
            session['user_id'] = user_row[id_index]
            return redirect('/home')
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect('/')
    else:
        flash('User not found!', 'danger')
        return redirect('/') 

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

#########################################################################################################
# @app.route('/password_forgot', methods=['GET', 'POST'])
# def password_forgot():
#     if request.method == 'POST':
#         email = request.form['email']
#         username = request.form['username'] 

#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT * FROM creds WHERE email = %s AND username = %s", (email, username))
#         user_row = cursor.fetchone()

#         if user_row: 
#             # Valid email and username combination, display a password reset form
#             return render_template('reset_password.html', email=email, username=username)
#         else:
#             flash('Invalid email or username. Please try again.', 'danger')

#     return render_template('password_forgot.html')


# Error in this: werkzeug.exceptions.BadRequestKeyError: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand.
# KeyError: 'password'

# @app.route('/reset_password', methods=['POST'])
# def reset_password():
#     email = request.form['email']
#     username = request.form['username']
#     password = request.form['password']

#     cursor = mysql.connection.cursor()
#     cursor.execute("UPDATE creds SET password = %s WHERE email = %s AND username = %s", (password, email, username))
#     mysql.connection.commit()
#     cursor.close()

#     flash('Password reset successfully. You can now log in with your new password.', 'success')
#     return redirect('/')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        # Check if the username or email already exists in the database
        cursor.execute("SELECT * FROM creds WHERE username = %s", (username,))
        user_with_username = cursor.fetchone()
        cursor.execute("SELECT * FROM creds WHERE email = %s", (email,))
        user_with_email = cursor.fetchone()

        if user_with_username:
            flash('Username already exists!', 'danger')
        elif user_with_email:
            flash('Email address already exists!', 'danger')
        else:
            # Insert the user data into the database
            cursor.execute("INSERT INTO creds (first_name, last_name, email, username, password) VALUES (%s, %s, %s, %s, %s)",
                           (first_name, last_name, email, username, password))
            mysql.connection.commit()
            cursor.close() 

            flash('Account created successfully. You can now log in.', 'success')
            return redirect('/')

    return render_template('register.html') 

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)