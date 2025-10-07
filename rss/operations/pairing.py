import streamlit as st
import json
import os , time

USER_FILE = "users.json"

def init_user_file():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)

def load_users():
    init_user_file()
    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}  # fallback if file is empty/corrupt

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def assign_teacher():
    st.subheader("👩‍🏫 Assign Teacher to Student")

    users = load_users()

    # Get all teachers (FULL NAME)
    teachers = [fullname for fullname, info in users.items() if info.get("role", "").lower() == "teacher"]

    # Get only students with no assigned teacher
    students = [
        fullname for fullname, info in users.items()
        if info.get("role", "").lower() == "student" and not info.get("teacher")
    ]

    if not students:
        st.info("⚠️ All students have already been assigned to teachers.")
        return
    if not teachers:
        st.info("⚠️ No teachers available to assign.")
        return

    # Select teacher (FULL NAME)
    teacher_name = st.selectbox("Select Teacher", teachers)

    # Select multiple students (only unassigned ones will show)
    selected_students = st.multiselect("Select Students", students)

    if st.button("Assign"):
        if not selected_students:
            st.warning("⚠️ Please select at least one student.")
            return
        with st.spinner("Assigning students to teacher..."):
            time.sleep(1.2)

            for student_name in selected_students:
                # ✅ Save teacher's FULL NAME to student record
                users[student_name]["teacher"] = teacher_name  

            save_users(users)  # ✅ Save once outside loop
        st.success(f"✅ Assigned {len(selected_students)} student(s) to {teacher_name}")
        time.sleep(0.7)

def assigned_students(teacher_name):
    st.subheader("👩‍🏫 My Students")

    with st.spinner("Assigned students..."):
        time.sleep(1.5)
        users = load_users()

    # Find all students assigned to this teacher (full name match)
    my_students = [
        {"name": fullname, "stage": info.get("stage", "N/A")}
        for fullname, info in users.items()
        if info.get("role", "").lower() == "student" and info.get("teacher") == teacher_name
    ]

    if not my_students:
        time.sleep(0.5)
        st.info("📌 You have no students assigned yet.")
        return

    # Display students with numbering and stage
    st.write("### 📋 Assigned Students:")
    time.sleep(0.5)
    for i, student in enumerate(my_students, start=1):
        st.write(f"{i}. **{student['name']}** — Stage: {student['stage']}")


def assigned_teacher(student_name):
    """
    Display the teacher assigned to the student.
    """
    if not os.path.exists(USER_FILE):
        st.info("No users found.")
        return

    with st.spinner("My teacher..."):
        time.sleep(0.8)
        with open(USER_FILE, "r") as f:
            users = json.load(f)

    student_record = users.get(student_name)
    if not student_record:
        st.warning("Your record was not found.")
        return

    teacher_name = student_record.get("teacher")
    time.sleep(0.3)
    if not teacher_name:
        st.info("No teacher assigned yet.")
    else:
        st.success(f"Your assigned teacher is: **{teacher_name}**")
