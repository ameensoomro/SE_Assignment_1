
import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/students"

st.set_page_config(page_title="Student Management", page_icon="🎓")
st.title("Student Management System")

# Display all students
def load_students():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    st.error("Unable to load students.")
    return []

students = load_students()

st.subheader("All Students")

if students:
    st.dataframe(students, use_container_width=True)
else:
    st.info("No students found.")

st.divider()

# Add student
st.subheader("Add New Student")

with st.form("add_student"):
    name = st.text_input("Student Name")
    department = st.text_input("Department")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Add Student")

    if submitted:
        response = requests.post(API_URL, json={
            "name": name,
            "department": department,
            "email": email
        })

        if response.status_code == 201:
            st.success("Student added successfully!")
            st.rerun()
        else:
            st.error(response.json().get("error", "Unable to add student."))

st.divider()

# Update student
st.subheader("Update Student")

if students:
    student_ids = [s["id"] for s in students]
    selected_id = st.selectbox("Select Student ID", student_ids)

    selected = next(s for s in students if s["id"] == selected_id)

    with st.form("update_student"):
        new_name = st.text_input("Name", value=selected["name"])
        new_department = st.text_input(
            "Department", value=selected["department"]
        )
        new_email = st.text_input("Email", value=selected["email"])

        updated = st.form_submit_button("Update Student")

        if updated:
            response = requests.put(
                f"{API_URL}/{selected_id}",
                json={
                    "name": new_name,
                    "department": new_department,
                    "email": new_email
                }
            )

            if response.status_code == 200:
                st.success("Student updated successfully!")
                st.rerun()
            else:
                st.error(response.json().get("error", "Unable to update."))

    st.divider()

    # Delete student
    st.subheader("Delete Student")

    if st.button("Delete Selected Student"):
        response = requests.delete(f"{API_URL}/{selected_id}")

        if response.status_code == 200:
            st.success("Student deleted successfully!")
            st.rerun()
        else:
            st.error(response.json().get("error", "Unable to delete."))

# Refresh records
if st.button("Refresh Records"):
    st.rerun()