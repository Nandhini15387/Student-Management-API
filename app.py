from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Student Management API"
    })


# GET - View all students
@app.route("/api/students", methods=["GET"])
def get_students():

    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students]), 200


# GET - View student by ID
@app.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):

    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student)), 200


# POST - Add a new student
@app.route("/api/students", methods=["POST"])
def add_student():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not all(isinstance(value, str) and value.strip()
               for value in [name, email, course]):
        return jsonify({
            "error": "Name, email and course are required"
        }), 400

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
            (name.strip(), email.strip(), course.strip())
        )

        conn.commit()

        return jsonify({
            "message": "Student added successfully",
            "id": cursor.lastrowid
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

    finally:
        conn.close()


# PUT - Update student details
@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not all(isinstance(value, str) and value.strip()
               for value in [name, email, course]):
        return jsonify({
            "error": "Name, email and course are required"
        }), 400

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """UPDATE students
               SET name = ?, email = ?, course = ?
               WHERE id = ?""",
            (name.strip(), email.strip(), course.strip(), id)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({
            "message": "Student updated successfully"
        }), 200

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

    finally:
        conn.close()


# DELETE - Remove a student
@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "message": "Student deleted successfully"
    }), 200


# Start application
create_table()

if __name__ == "__main__":
    app.run(debug=True)