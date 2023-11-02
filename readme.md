# Pre-Requisites

## Table of Contents
1. [Modules Required](requirements.txt)
2. [Using OS Environment Variables](#using-os-environment-variables)
3. [MySQL Connection](mysql-config.py)
4. [Hosting in Ubuntu VM](hosting-in-ubuntu-vm)


## Using OS Environment Variables

I have used OS Environment Variables in many places like, specifying email, password, MySQL connection variables, etc.

To use OS Environment Variables,

1. For Windows Powershell,
`$env:EMAIL_ID = "aanshojha@zohomail.in"`

2. For Bash,
`export EMAIL="aanshojha@zohomail.in"`

3. Python code to test:
```py
import os

# Get the value of the environment variable 'EMAIL'
email_value = os.environ.get('EMAIL')

# Check if the variable is set
if email_value is not None:
    print(f"The value of the environment variable 'EMAIL' is: {email_value}")
else:
    print("The environment variable 'EMAIL' is not set.")

```

### ⚠️ **Warning**

In the same terminal, same directory, same terminal session,
1. environment variable declaration,
2. running of python file

should be done. Otherwise use global variables or other options.


## Hosting in Ubuntu VM
1. Git clone this reposoitory.
2. Go to the folder
3. Create virtual environment
   ```sh
   sudo apt install python3.8-venv
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install the modules
```sh
pip install -r requirements.txt
```
5. Configure MySQL
```sh
sudo apt mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql_secure_installation
```
Follow the on-screen instructions.

6. Set MySQL password
```sh
sudo mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_new_password';
FLUSH PRIVILEGES;
EXIT;
```
7. Afer this, login to MySQL (Just to check MySQL is configured properly.)
```sh
mysql -u root -p
```
Don't forget to exit; MySQL :)





