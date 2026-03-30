from flask import Blueprint, request, jsonify
from config import get_db_connection

appointments_bp = Blueprint('appointments_bp', __name__)

# ----------------------------
# ✅ ADD APPOINTMENT
# ----------------------------
@appointments_bp.route('/add', methods=['POST'])
def add_appointment():
    try:
        data = request.get_json()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO appointments
            (patient_name, patient_age, patient_contact, gender, specialization, doctor, appointment_date, appointment_time, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('patientName'),
            data.get('patientAge'),
            data.get('patientContact'),
            data.get('gender'),
            data.get('specialization'),
            data.get('doctor'),
            data.get('date'),
            data.get('time'),
            data.get('notes')
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Appointment added"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# ✅ GET ALL APPOINTMENTS
# ----------------------------
@appointments_bp.route('/all', methods=['GET'])
def get_appointments():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM appointments ORDER BY id DESC;")

        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))

        cur.close()
        conn.close()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500