import MySQLdb
import os
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    conn = MySQLdb.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        passwd=os.environ.get("DB_PASSWORD"),
        db=os.environ.get("DB_NAME")
    )
    return conn
