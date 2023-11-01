from datetime import datetime, timedelta
from flaskalbum import mysql, bcrypt, app
import jwt
from jwt import encode, decode

class User:
    # Method to register a new user in the database
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

    # Method to generate a JWT token with an expiration time
    def get_reset_token(self, expires_sec=600):
        # Generates a JWT token with an expiration time.
        payload = {
            "email": self.email,
            "expiration": str(datetime.utcnow() + timedelta(seconds=expires_sec))
        }

        token = jwt.encode(payload, app.config["SECRET_KEY"])
        return token

    # Static method to verify the validity of a reset token
    @staticmethod
    def verify_reset_token(token):
        try:
            # Decode the token and extract email and expiration time
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=['HS256'])
            email = payload['email']
            expiration = datetime.strptime(payload['expiration'], '%Y-%m-%d %H:%M:%S.%f')
            
            # Check if the token has expired
            if expiration < datetime.utcnow():
                return None
            
            return email
            
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return None
        except jwt.InvalidTokenError:
            # Handle invalid token
            return None
        
    # Representation of User object for debugging and logging
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}', '{self.name}')"