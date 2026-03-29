from flask import Blueprint, request, jsonify
from config import get_db_connection
from datetime import timedelta

doctors_bp = Blueprint('doctors_bp', __name__)

# ----------------------------
# ✅ Add Doctor
# ----------------------------
@doctors_bp.route('/add', methods=['POST'])
def add_doctor():
    try:
        data = request.get_json()

        name = data.get('name')
        specialization = data.get('specialization')
        hospital_name = data.get('hospital_name')
        contact_no = data.get('contact_no')
        available_from = data.get('available_from')
        available_to = data.get('available_to')

        if not name or not specialization:
            return jsonify({"error": "Name and specialization are required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO doctors (name, specialization, hospital_name, contact_no, available_from, available_to)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, specialization, hospital_name, contact_no, available_from, available_to))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Doctor added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# ✅ Get All Doctors
# ----------------------------
@doctors_bp.route('/all', methods=['GET'])
def get_all_doctors():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM doctors ORDER BY name;")

        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        doctors = []

        for row in rows:
            doc = dict(zip(columns, row))

            # Convert datetime / timedelta
            for key, value in doc.items():
                if isinstance(value, timedelta):
                    total_seconds = int(value.total_seconds())
                    doc[key] = str(timedelta(seconds=total_seconds))
                elif hasattr(value, "isoformat"):
                    doc[key] = value.isoformat()

            doctors.append(doc)

        cur.close()
        conn.close()

        return jsonify(doctors)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# ✅ Get Doctor by ID
# ----------------------------
@doctors_bp.route('/<int:id>', methods=['GET'])
def get_doctor(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM doctors WHERE id = %s;", (id,))
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "Doctor not found"}), 404

        columns = [desc[0] for desc in cur.description]
        doctor = dict(zip(columns, row))

        cur.close()
        conn.close()

        return jsonify(doctor)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# ✅ Update Doctor
# ----------------------------
@doctors_bp.route('/update/<int:id>', methods=['PUT'])
def update_doctor(id):
    try:
        data = request.get_json()
        fields = []
        values = []

        for key in ['name', 'specialization', 'hospital_name', 'contact_no', 'available_from', 'available_to']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])

        if not fields:
            return jsonify({"error": "No fields to update"}), 400

        values.append(id)

        conn = get_db_connection()
        cur = conn.cursor()

        query = f"UPDATE doctors SET {', '.join(fields)} WHERE id = %s;"
        cur.execute(query, values)

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Doctor updated successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# ✅ Delete Doctor
# ----------------------------
@doctors_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM doctors WHERE id = %s;", (id,))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Doctor deleted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500