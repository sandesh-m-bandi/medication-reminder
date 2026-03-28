from flask import Blueprint, request, jsonify
from config import get_db_connection 
from datetime import date, timedelta

medicines_bp = Blueprint('medicines', __name__)


# ---------------------------
# Fetch all medicines (FIXED)
# ---------------------------
@medicines_bp.route('/all', methods=['GET'])
def get_all_medicines():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM medicines;")
    
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    medicines = []
    for row in rows:
        med = dict(zip(columns, row))

        # Convert datetime/timedelta to string
        for key, value in med.items():
            if hasattr(value, 'isoformat'):
                med[key] = value.isoformat()
            elif str(type(value)) == "<class 'datetime.timedelta'>":
                total_seconds = int(value.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                med[key] = f"{hours:02}:{minutes:02}:{seconds:02}"

        medicines.append(med)

    cur.close()
    conn.close()

    return jsonify(medicines)


# ---------------------------
# Add new medicine (NO CHANGE)
# ---------------------------
@medicines_bp.route('/add', methods=['POST'])
def add_medicine():
    data = request.get_json()

    name = data.get('name')
    dosage = data.get('dosage')
    frequency = data.get('frequency')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    time1 = data.get('time1')
    time2 = data.get('time2')
    time3 = data.get('time3')

    today = data.get('today') or str(date.today())

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO medicines 
            (name, dosage, frequency, time1, time2, time3, start_date, end_date, today)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, dosage, frequency, time1, time2, time3, start_date, end_date, today))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'message': 'Medicine added successfully!',
            'today': today
        }), 201

    except Exception as e:
        print("Error adding medicine:", e)
        return jsonify({
            'message': 'Failed to add medicine',
            'error': str(e)
        }), 500


# ---------------------------
# Update existing medicine (FIXED)
# ---------------------------
@medicines_bp.route('/update/<int:med_id>', methods=['PUT'])
def update_medicine(med_id):
    from datetime import date, timedelta, datetime

    data = request.get_json()
    name = data.get('name')
    dosage = data.get('dosage')
    frequency = data.get('frequency')
    time1 = data.get('time1')
    time2 = data.get('time2')
    time3 = data.get('time3')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    today = data.get('today')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM medicines WHERE id = %s", (med_id,))
        row = cur.fetchone()

        if not row:
            cur.close()
            conn.close()
            return jsonify({'message': 'Medicine not found!'}), 404

        # Convert row → dict
        columns = [desc[0] for desc in cur.description]
        existing = dict(zip(columns, row))

        # Move to next day
        if data.get("move_to_next_day") == True:
            today = (date.fromisoformat(existing["today"]) + timedelta(days=1)).isoformat()

        # Move to next time
        elif data.get("move_to_next_time") == True:
            current_time = datetime.now().strftime("%H:%M")

            if existing["time2"] and current_time >= str(existing["time1"])[:5] and current_time < str(existing["time2"])[:5]:
                print("Moving to next reminder: time2")
            elif existing["time3"] and current_time >= str(existing["time2"])[:5]:
                print("Moving to next reminder: time3")
            else:
                today = (date.fromisoformat(existing["today"]) + timedelta(days=1)).isoformat()

        cur.execute("""
            UPDATE medicines
            SET name=%s, dosage=%s, frequency=%s, time1=%s, time2=%s, time3=%s,
                start_date=%s, end_date=%s, today=%s
            WHERE id=%s
        """, (name, dosage, frequency, time1, time2, time3,
              start_date, end_date, today or existing["today"], med_id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'message': 'Medicine updated successfully!',
            'today': today or existing["today"]
        })

    except Exception as e:
        print("Error while updating medicine:", e)
        return jsonify({
            'message': 'Failed to update medicine',
            'error': str(e)
        }), 500


# ---------------------------
# Delete medicine (NO CHANGE)
# ---------------------------
@medicines_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_medicine(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM medicines WHERE id = %s", (id,))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Medicine deleted successfully!'})
