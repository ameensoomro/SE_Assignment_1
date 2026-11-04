
from flask import Flask, request, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import secrets
import os

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), "employees.db")

# Demo users: one Administrator and one Employee
USERS = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "role": "Administrator"
    },
    "employee": {
        "password": generate_password_hash("emp123"),
        "role": "Employee"
    }
}

# Temporary login sessions
TOKENS = {}


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM employees"
    ).fetchone()[0]

    if count == 0:
        conn.execute("""
            INSERT INTO employees (name, department, email)
            VALUES (?, ?, ?)
        """, ("Ali Ahmed", "IT", "ali@example.com"))

        conn.execute("""
            INSERT INTO employees (name, department, email)
            VALUES (?, ?, ?)
        """, ("Sara Khan", "HR", "sara@example.com"))

    conn.commit()
    conn.close()


# Authentication and authorization decorator
def require_auth(admin_only=False):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get("Authorization", "")

            if not auth_header.startswith("Bearer "):
                return jsonify({
                    "error": "Authentication required"
                }), 401

            token = auth_header.split(" ", 1)[1]
            user = TOKENS.get(token)

            if not user:
                return jsonify({
                    "error": "Invalid or expired token"
                }), 401

            if admin_only and user["role"] != "Administrator":
                return jsonify({
                    "error": "Administrator access required"
                }), 403

            return function(*args, **kwargs)

        return wrapper
    return decorator


# Login endpoint
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    user = USERS.get(username)

    if not user or not check_password_hash(
        user["password"], password or ""
    ):
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    token = secrets.token_urlsafe(32)

    TOKENS[token] = {
        "username": username,
        "role": user["role"]
    }

    return jsonify({
        "message": "Login successful",
        "username": username,
        "role": user["role"],
        "token": token
    }), 200


# View employees: Employee and Administrator
@app.route("/employees", methods=["GET"])
@require_auth()
def get_employees():

    conn = get_db()
    employees = conn.execute(
        "SELECT * FROM employees"
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in employees]), 200


# Add employee: Administrator only
@app.route("/employees", methods=["POST"])
@require_auth(admin_only=True)
def add_employee():

    data = request.get_json(silent=True) or {}

    name = data.get("name")
    department = data.get("department")
    email = data.get("email")

    if not all(isinstance(value, str) and value.strip()
               for value in (name, department, email)):
        return jsonify({
            "error": "Name, department and email are required"
        }), 400

    conn = get_db()

    try:
        cursor = conn.execute("""
            INSERT INTO employees (name, department, email)
            VALUES (?, ?, ?)
        """, (name.strip(), department.strip(), email.strip()))

        conn.commit()

        return jsonify({
            "message": "Employee added successfully",
            "employee_id": cursor.lastrowid
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email already exists"
        }), 409

    finally:
        conn.close()


# Update employee: Administrator only
@app.route("/employees/<int:employee_id>", methods=["PUT"])
@require_auth(admin_only=True)
def update_employee(employee_id):

    data = request.get_json(silent=True) or {}

    name = data.get("name")
    department = data.get("department")
    email = data.get("email")

    if not all(isinstance(value, str) and value.strip()
               for value in (name, department, email)):
        return jsonify({
            "error": "Name, department and email are required"
        }), 400

    conn = get_db()

    try:
        cursor = conn.execute("""
            UPDATE employees
            SET name = ?, department = ?, email = ?
            WHERE id = ?
        """, (name.strip(), department.strip(),
              email.strip(), employee_id))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Employee not found"
            }), 404

        return jsonify({
            "message": "Employee updated successfully"
        }), 200

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email already exists"
        }), 409

    finally:
        conn.close()


# Delete employee: Administrator only
@app.route("/employees/<int:employee_id>", methods=["DELETE"])
@require_auth(admin_only=True)
def delete_employee(employee_id):

    conn = get_db()

    cursor = conn.execute(
        "DELETE FROM employees WHERE id = ?",
        (employee_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({
            "error": "Employee not found"
        }), 404

    return jsonify({
        "message": "Employee deleted successfully"
    }), 200


if __name__ == "__main__":
    initialize_database()
    app.run(port=5002, debug=True)