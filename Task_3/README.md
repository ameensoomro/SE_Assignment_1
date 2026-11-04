# Task 3: Authentication and Authorization in Flask API

## Project Description
This project demonstrates authentication and role-based authorization using a Flask REST API. It provides an employee management system with two user roles: Employee and Administrator.

## Technologies Used
- Python
- Flask
- SQLite
- Werkzeug Security

## User Credentials

| Role | Username | Password |
|---|---|---|
| Administrator | admin | admin123 |
| Employee | employee | emp123 |

*These credentials are for coursework demonstration only.*

## API Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /login | User login | Public |
| GET | /employees | View employees | Employee and Administrator |
| POST | /employees | Add employee | Administrator |
| PUT | /employees/{id} | Update employee | Administrator |
| DELETE | /employees/{id} | Delete employee | Administrator |

## Authentication
Users must log in using valid credentials. The API generates a token that must be sent in the Authorization header:

`Authorization: Bearer YOUR_TOKEN`

## Authorization
- Employee: Can only view employee records.
- Administrator: Can view, add, update, and delete employee records.
- Unauthenticated users: Cannot access protected endpoints.
- Unauthorized roles: Receive HTTP 403 Forbidden.

## Testing
The following tests were performed:
1. Successful Administrator login.
2. Successful Employee login.
3. Employee viewing employee records.
4. Employee denied permission to add employees.
5. Administrator adding an employee.
6. Administrator updating an employee.
7. Administrator deleting an employee.
8. Unauthenticated access rejected with HTTP 401.
9. Invalid login rejected with HTTP 401.

## How to Run

Install dependencies:

`pip install -r requirements.txt`

Run the application:

`python Task_3/app.py`

The server runs at:

`http://127.0.0.1:5002`