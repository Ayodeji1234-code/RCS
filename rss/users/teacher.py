import streamlit as st
from users.user import User
from operations.assessment import record_assessment, view_assessments
from operations.attendance import view_attendance, record_attendance
from operations.schedule import view_teacher_schedule
from operations.pairing import assigned_students, load_users   # ✅ make sure this points to your user utils
import json
import os,time

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)


def get_fullname_from_username(username):
    """Return the FULL NAME of a teacher given their username."""
    users = load_users()
    for fullname, info in users.items():
        if info.get("username") == username and info.get("role", "").lower() == "teacher":
            return fullname
    return username  # fallback if not found


class Teacher(User):
    def __init__(self, username):
        fullname = get_fullname_from_username(username)
        super().__init__(username, fullname, role="Teacher")

    def get_actions(self):
        return [
            "Profile",
            "View Schedule",
            "My Students",
            "Record Assessment",
            "View Assessment",
            "Record Attendance",
            "View Attendance",
            "Logout"
        ]

    def action(self, choice):
        with st.spinner(f"Loading {choice}..."):
            time.sleep(0.8)
        if choice == "Profile":
            self.view_profile()
        elif choice == "View Schedule":
            view_teacher_schedule(self.name)   # full name 
        elif choice == "My Students":    
            assigned_students(self.name)       # full name
            st.session_state["students_viewed"] = True
        elif choice == "Record Assessment":
            record_assessment(self.name)
        elif choice == "View Assessment":
            view_assessments()
        elif choice == "Record Attendance":
            record_attendance(self.name)       #  matches student["teacher"]
        elif choice == "View Attendance":
            view_attendance()

    def view_profile(self):
            with st.spinner("Loading profile..."):
                time.sleep(1)
            st.markdown(f"""
           Welcome, {self.username}

            Use the dashboard on the left to:
            - 🗓️ Record or view attendance  
            - 📝 Track student progress  
            - 📅 View your class schedules
            - 📝  Record or view assessment              
            """)

            users = load_users()
            assigned_students = [s for s, info in users.items() if info.get("teacher") == self.name]

            # Only show 'new student' message if they haven't viewed it yet
            if assigned_students and not st.session_state.get("students_viewed", False):
                st.success("✅ You have new student(s) assigned.")
            else:
                st.info(" You have no new students yet.")