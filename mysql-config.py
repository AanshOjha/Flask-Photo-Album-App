import mysql.connector
from envconfig import MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB, MYSQL_TABLE

# Establish a connection to MySQL server
mydb = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS
)

# Create a cursor object to interact with the database
mycursor = mydb.cursor()

# Create a database named 'mydatabase'
mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")

# Switch to the 'mydatabase' database
mycursor.execute(f"USE {MYSQL_DB}")

# Create a table 'customers' with columns 'name' and 'address'
mycursor.execute(f"CREATE TABLE IF NOT EXISTS {MYSQL_TABLE} (name VARCHAR(120), email VARCHAR(120), username VARCHAR(120), password VARCHAR(120))")

# Close the cursor and connection
mycursor.close()
mydb.close()