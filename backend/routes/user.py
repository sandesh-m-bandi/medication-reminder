from flask import Blueprint, jsonify, request
from config import get_db_connection

users_bp = Blueprint('users', __name__)

# -------------------------------
# GET ALL USERS
# -------------------------------
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


# -------------------------------
# LOGIN USER
# -------------------------------
# -------------------------------
# SIGNUP USER
# -------------------------------
@users_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if user already exists
    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        conn.close()
        return jsonify({
            "success": False,
            "message": "User already exists"
        })

    # Insert new user
    cur.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s);",
        (username, email, password)
    )
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "User registered successfully"
    })
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    # 🔍 Check user in database
    cur.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s;",
        (email, password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "email": email
            }
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        })
    return jsonify(users)
