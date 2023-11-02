import mysql.connector

# Establish a connection to MySQL server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)

# Create a cursor object to interact with the database
mycursor = mydb.cursor()

# Create a database named 'mydatabase'
mycursor.execute("CREATE DATABASE IF NOT EXISTS users_db")

# Switch to the 'mydatabase' database
mycursor.execute("USE users_db")

# Create a table 'customers' with columns 'name' and 'address'
mycursor.execute("CREATE TABLE IF NOT EXISTS user_credentials (name VARCHAR(120), email VARCHAR(120), username VARCHAR(120), password VARCHAR(120))")

# Close the cursor and connection
mycursor.close()
mydb.close()

