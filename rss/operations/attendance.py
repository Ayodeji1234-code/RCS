import json
import os , time
from datetime import date
import streamlit as st
import pandas as pd

ATTENDANCE_FILE = "attendance.json"
USER_FILE = "users.json"


# --- Helpers ---
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)


def init_attendance_file():
    """Ensure the attendance file exists."""
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w") as f:
            json.dump({}, f)  # start with empty JSON

def load_attendance():
    init_attendance_file()
    with open(ATTENDANCE_FILE, "r") as f:
        return json.load(f)


def save_attendance(attendance):
    with open(ATTENDANCE_FILE, "w") as f:
        json.dump(attendance, f, indent=4)


# --- Record Attendance (Teacher Only) ---
def record_attendance(teacher_name):
    """
    Record attendance for students assigned to a teacher by full name.

    Args:
        teacher_name (str): Teacher's full name stored in students' "teacher" field
    """
    st.subheader("📌 Record Attendance")
    time.sleep(0.5) 
    users = load_users()  # Load all users

    # Find students assigned to this teacher (strict full-name match)
    students = [
        student_name
        for student_name, info in users.items()
        if info.get("role", "").lower() == "student"
        and info.get("teacher") == teacher_name
    ]

    if not students:
        st.info("⚠️ No students assigned to you yet.")
        return

    today = str(date.today())
    attendance = load_attendance()  # Load existing attendance

    # --- Bulk attendance form ---
    with st.form("attendance_form"):
        status_dict = {}
        for student in students:
            status = st.radio(
                f"{student}",
                ["Present", "Absent"],
                horizontal=True,
                key=f"{student}_{today}"
            )
            status_dict[student] = status

        submitted = st.form_submit_button("✅ Save Attendance")

        if submitted:
            for student, status in status_dict.items():
                if student not in attendance:
                    attendance[student] = {}
                attendance[student][today] = status

            save_attendance(attendance)
            st.success("🎉 Attendance saved successfully!")
            time.sleep(1.5)


def view_attendance():
    st.subheader("📂 All Attendance Records")
    with st.spinner("Loading all attendance..."):
        time.sleep(1.5)
        attendance = load_attendance()
    
    if not attendance:
        st.info("No attendance records yet.")
        return

    rows = []
    for student, records in attendance.items():
        for day, status in records.items():
            rows.append({"Student": student, "Date": day, "Status": status})

    df = pd.DataFrame(rows)
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True)



def view_my_attendance(student_fullname):
    st.subheader(f"📂 Attendance for {student_fullname}")
    with st.spinner("My attendance..."):
        time.sleep(1.5)
        attendance = load_attendance()

    # ✅ Lookup by full name
    records = attendance.get(student_fullname, {})
    if not records:
        st.info("⚠️ No attendance recorded for you yet.")
        return

    # Display neatly
    df = pd.DataFrame(list(records.items()), columns=["Date", "Status"])
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True)


def attendance_summary():
    st.subheader("📊 Attendance Summary")
    with st.spinner("Loading all attendance..."):
        time.sleep(1.5)
        with open(ATTENDANCE_FILE, "r") as f:
            attendance = json.load(f)

    if not attendance:
        st.info("No attendance records found.")
        return

    summary_rows = []
    for student, records in attendance.items():
        total_days = len(records)
        present_days = sum(1 for s in records.values() if s == "Present")
        absent_days = total_days - present_days
        percentage = (present_days / total_days) * 100 if total_days > 0 else 0
        status = "⚠️ Needs Intervention" if percentage < 75 else "✅ On Track"

        summary_rows.append({
            "Student": student,
            "Total Days": total_days,
            "Present": present_days,
            "Absent": absent_days,
            "Attendance Rate (%)": f"{percentage:.2f}",
            "Status": status
        })

    df_summary = pd.DataFrame(summary_rows)
    df_summary.index = df_summary.index + 1  # Start index at 1
    st.dataframe(df_summary, use_container_width=True)
