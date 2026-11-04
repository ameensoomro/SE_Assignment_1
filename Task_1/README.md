# Task 1: Database-Driven Flask API with Streamlit Interface

## Overview
A Student Management System developed using Flask, SQLite, and Streamlit.

## Technologies Used
- Python
- Flask
- SQLite
- Streamlit
- Requests

## Database
The students table contains:
- ID
- Name
- Department
- Email

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /students | Get all students |
| GET | /students/<id> | Get student by ID |
| POST | /students | Add student |
| PUT | /students/<id> | Update student |
| DELETE | /students/<id> | Delete student |

## How to Run

Install dependencies:

pip install -r requirements.txt

Run Flask:

python Task_1/app.py

Run Streamlit in another terminal:

python -m streamlit run Task_1/streamlit_app.py

## Features
- View all students
- Add new students
- Update student records
- Delete students
- Refresh records automatically after successful operations
- SQLite database storage