from flaskalbum import mysql, bcrypt

class User:
    def register_user(self, name, email, username, password):
        cursor = mysql.connection.cursor()

        # Check if the username or email already exists in the database
        cursor.execute("SELECT * FROM creds WHERE username = %s", (username,))
        user_with_username = cursor.fetchone()
        cursor.execute("SELECT * FROM creds WHERE email = %s", (email,))
        user_with_email = cursor.fetchone()

        if user_with_username:
            return 'Username already exists!'
        elif user_with_email:
            return 'Email address already exists!'
        else:
            # Hash the password before storing it in the database
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Insert the user data into the database
            cursor.execute("INSERT INTO creds (name, email, username, password) VALUES (%s, %s, %s, %s)",
                           (name, email, username, hashed_password))
            mysql.connection.commit()
            cursor.close() 

            return 'Account created successfully. You can now log in.'
