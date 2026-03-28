from flask import Blueprint, jsonify
from config import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users;")
    
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    users = []
    for row in rows:
        users.append(dict(zip(columns, row)))

    cur.close()
    conn.close()

    return jsonify(users)
