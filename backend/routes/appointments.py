from flask import Blueprint, jsonify
from config import get_db_connection

appointments_blueprint = Blueprint("appointments", __name__)

def get_db():
    return get_db_connection()   # ✅ no parameters

@appointments_blueprint.route("/doctors/all", methods=["GET"])
def get_all_doctors():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id, name, specialization, hospital_name, contact_no FROM doctors")
    
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    doctors = []
    for row in rows:
        doctors.append(dict(zip(columns, row)))

    cursor.close()
    db.close()

    return jsonify(doctors)
