import datetime
import jwt
from jwt import encode, decode


payload = {
        "email": 'aanshojha@zohomail.in',
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)
    }
token = jwt.encode(payload, '5791628bb0b13ce0c676dfde280ba245', algorithm="HS256")

def get_reset_token():
    payload = {
        "email": 'aanshojha@zohomail.in',
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)
    }
    token = jwt.encode(payload, '5791628bb0b13ce0c676dfde280ba245', algorithm="HS256")
    
    print(jwt.decode(token, '5791628bb0b13ce0c676dfde280ba245', algorithms=['HS256'])) 
    print(token)

@staticmethod
def verify_reset_token():
    payload = jwt.decode(token, '5791628bb0b13ce0c676dfde280ba245', algorithms=['HS256'])
    email = payload['email']
    cursor.execute("SELECT * FROM creds WHERE email = %s", (email,))
    user_with_email = cursor.fetchone()
    return email==user_with_email

get_reset_token()
verify_reset_token()
