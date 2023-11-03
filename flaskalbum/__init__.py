from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from envconfig import MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
bcrypt = Bcrypt(app)

# MySQL Configuration 
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASS
app.config['MYSQL_DB'] = MYSQL_DB

mysql = MySQL(app)

from flaskalbum import routes