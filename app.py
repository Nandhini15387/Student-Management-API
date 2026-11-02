from flask import Flask, request, jsonify
import psycopg
from psycopg.rows import dict_row
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


# Database connection
def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


# Create database table
def create_table():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id BIGSERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL
            )
        """)


# Initialize database when configured
if DATABASE_URL:
    create_table()


# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Student Management API"
    })


# GET - View all students
@app.route("/api/students", methods=["GET"])
def get_students():

    with get_db_connection() as conn:
        students = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

    return jsonify(students), 200


# GET - View student by ID
@app.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):

    with get_db_connection() as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE id = %s",
            (id,)
        ).fetchone()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student), 200


# POST - Add a new student
@app.route("/api/students", methods=["POST"])
def add_student():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON data is required"}), 400

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not all(
        isinstance(value, str) and value.strip()
        for value in [name, email, course]
    ):
        return jsonify({
            "error": "Name, email and course are required"
        }), 400

    try:
        with get_db_connection() as conn:
            student = conn.execute(
                """
                INSERT INTO students (name, email, course)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (name.strip(), email.strip(), course.strip())
            ).fetchone()

        return jsonify({
            "message": "Student added successfully",
            "id": student["id"]
        }), 201

    except psycopg.errors.UniqueViolation:
        return jsonify({"error": "Email already exists"}), 409


# PUT - Update student details
@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON data is required"}), 400

    name = data.get("name")
    email = data.get("email")
    course = data.get("course")

    if not all(
        isinstance(value, str) and value.strip()
        for value in [name, email, course]
    ):
        return jsonify({
            "error": "Name, email and course are required"
        }), 400

    try:
        with get_db_connection() as conn:
            result = conn.execute(
                """
                UPDATE students
                SET name = %s, email = %s, course = %s
                WHERE id = %s
                """,
                (name.strip(), email.strip(), course.strip(), id)
            )

            updated = result.rowcount

        if updated == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({
            "message": "Student updated successfully"
        }), 200

    except psycopg.errors.UniqueViolation:
        return jsonify({"error": "Email already exists"}), 409


# DELETE - Remove a student
@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    with get_db_connection() as conn:
        result = conn.execute(
            "DELETE FROM students WHERE id = %s",
            (id,)
        )

        deleted = result.rowcount

    if deleted == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "message": "Student deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)