import datetime
from flaskalbum import mysql, bcrypt, app
import jwt
from jwt import encode, decode

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

    def get_reset_token(self, expires_sec=1800):
        # Generates a JWT token with an expiration time.
        payload = {
            "email": self.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_sec)
        }

        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
        return token

        

    @staticmethod
    def verify_reset_token(token):
        try:
            payload = jwt.decode(token, '5791628bb0b13ce0c676dfde280ba245', algorithms=['HS256'])
            email = payload['email']
            return email
            
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return None
        except jwt.InvalidTokenError:
            # Handle invalid token
            return None
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}', '{self.name}')"