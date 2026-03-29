import psycopg2
import os

def get_db_connection():
    try:
        # ✅ Correct way: get from environment variable
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise Exception("DATABASE_URL is not set in environment variables")

        conn = psycopg2.connect(database_url)
        return conn

    except Exception as e:
        print("Database connection error:", str(e))
        raise