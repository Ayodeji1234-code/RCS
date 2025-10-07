import sys , time
sys.path.append(r'C:\Users\user\Documents\python')
from users.user import User
from operations.attendance import view_my_attendance
from operations.schedule import view_student_timetable
from operations.pairing import assigned_teacher
from operations.assessment import view_my_assessments
import streamlit as st

class Student(User):
    def __init__(self, name, username, stage):
        super().__init__(username, name, role='Student')
        self.stage = stage

    def get_actions(self):
        """Return list of actions available to Student"""
        return [
            "Profile",
            "View Time Table",
            "View My Attendance",
            "View My Assessment",
            "Logout"
        ]

    def action(self, choice):
        with st.spinner(f"Loading {choice}..."):
            time.sleep(0.8)
        if choice == "Profile":
            self.view_profile()
        elif choice == "View Time Table":
            view_student_timetable(self.name)
        elif choice == "View My Attendance":
            view_my_attendance(self.name)
        elif choice == "View My Assessment":
            view_my_assessments(self.name)

    def view_profile(self):
        """Show student dashboard info"""
        with st.spinner("Loading profile..."):
            time.sleep(1)
        st.markdown(f"""
        Welcome, **{self.username}**!

        - 📚 Stage: **{self.stage}**
        - 🏫 Role: **{self.role}**

        Use the dashboard on the left to:  
        - Check your timetable and assigned teacher 🗓️  
        - Track your attendance 📋  
        - Review your assessments 📝  
        """)

       