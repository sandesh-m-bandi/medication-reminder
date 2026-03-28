import psycopg2
import os

def get_db_connection():
    database_url = os.getenv("postgresql://face_attendence_user:0InGHVSZlus5CJFoUXopnGSezs0ibk4S@dpg-d73av49r0fns739ao8q0-a.oregon-postgres.render.com/face_attendence")

    if not database_url:
        raise Exception("DATABASE_URL is not set in environment variables")

    conn = psycopg2.connect(database_url)
    return conn
