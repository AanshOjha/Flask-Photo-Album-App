from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
EMAIL_ID = os.getenv('EMAIL_ID')
EMAIL_PASS = os.getenv('EMAIL_PASS')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASS')
MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_TABLE = os.getenv('MYSQL_TABLE')