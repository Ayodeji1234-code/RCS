import sys,time
sys.path.append(r'C:\Users\user\Documents\python')
from users.user import User
from operations.assessment import assessment_summary
from operations.attendance import attendance_summary
from operations.manage_users import manage_users
from operations.schedule import add_timetable_entry,view_all_schedules
from operations.pairing import assign_teacher
from operations.system_report import system_report
import streamlit as st

class Admin(User):
    def __init__(self, name, username):
        super().__init__(username, name, role="Admin")

    def get_actions(self):
        """Return list of actions available to Admin"""
        return [
            "Profile",
            "Manage Users",
            "Pair Teacher-Students",
            "Create Schedules",
            "View All Schedules",
            "Assessment Summary",
            "Attendance Summary",
            "System Report",
            "Logout"
        ]

    def action(self, choice):
        with st.spinner(f"Loading {choice}..."):
            time.sleep(0.8)  

        if choice == "Manage Users":
            manage_users()
        elif choice == "Pair Teacher-Students":
            assign_teacher()
        elif choice == "Create Schedules":
            add_timetable_entry()
        elif choice == "View All Schedules":
            view_all_schedules()    
        elif choice == "Assessment Summary":
            assessment_summary()
        elif choice == "Attendance Summary":
            attendance_summary()
        elif choice == "System Report":
            system_report()

    def view_profile(self):
        """Display a welcome profile for the Admin"""
        with st.spinner("Loading profile..."):
            time.sleep(1)

        st.markdown(f"""
        ### 🧩 Welcome, **{self.username}!**
        You are logged in as **Administrator**.

        As an Admin, use the dashboard on the left to:
        - 👥 Manage users (create, edit, delete)
        - 📘 Assign teachers to students
        - 🗓️ Create and view schedules
        - 📊 Monitor assessments and attendance
        - 🧾 View system-wide reports
        """)        
