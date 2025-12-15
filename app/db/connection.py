import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

def create_connection():
    """Connect to MySQL database using .env config"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None