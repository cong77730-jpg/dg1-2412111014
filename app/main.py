import os
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'students.json')
MSSV_ENV = os.getenv('MSSV', '2412111014')

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html', students=read_data())

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "student": MSSV_ENV}), 200

@app.route('/api/students', methods=['GET'])
def get_students():
    students = read_data()
    lop = request.args.get('lop')
    if lop:
        students = [s for s in students if s.get('lop') == lop]
    return jsonify(students), 200

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    students = read_data()
    student = next((s for s in students if s.get('id') == student_id), None)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Not Found"}), 404

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    required_fields = ['mssv', 'ho_ten', 'lop', 'diem']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        diem = float(data['diem'])
        if diem < 0 or diem > 10:
            return jsonify({"error": "Diem must be between 0 and 10"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid diem format"}), 400

    students = read_data()
    new_id = max([s['id'] for s in students], default=0) + 1
    new_student = {
        "id": new_id,
        "mssv": str(data['mssv']),
        "ho_ten": str(data['ho_ten']),
        "lop": str(data['lop']),
        "diem": diem
    }
    students.append(new_student)
    write_data(students)
    return jsonify(new_student), 201

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
