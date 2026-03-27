from flask import Blueprint, jsonify
import MySQLdb
from config import get_db_connection


appointments_blueprint = Blueprint("appointments", __name__)

def get_db():
    return get_db_connection(

        host="localhost",
        user="root",
        password="",
        database="med_reminder"
    )

@appointments_blueprint.route("/doctors/all", methods=["GET"])
def get_all_doctors():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, name, specialization, hospital_name, contact_no FROM doctors")
    doctors = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(doctors)