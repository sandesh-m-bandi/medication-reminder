import MySQLdb
import os
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    conn = MySQLdb.connect(
        host=os.environ.get("dpg-d73av49r0fns739ao8q0-a"),
        user=os.environ.get("face_attendence_user"),
        passwd=os.environ.get("0InGHVSZlus5CJFoUXopnGSezs0ibk4S"),
        db=os.environ.get("face_attendence")
    )
    return conn
