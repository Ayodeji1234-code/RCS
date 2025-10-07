import streamlit as st
import json,os,time
import pandas as pd
from operations.pairing import assigned_teacher

USER_FILE = "users.json"
TIMETABLE_FILE = "timetable.json"

# --- helpers ---
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def load_timetable():
    if not os.path.exists(TIMETABLE_FILE):
        return {}
    with open(TIMETABLE_FILE, "r") as f:
        return json.load(f)

def save_timetable(timetable):
    with open(TIMETABLE_FILE, "w") as f:
        json.dump(timetable, f, indent=4)


def add_timetable_entry():
    st.subheader("🗓️ Create Schedule")

    users = load_users()

    # --- Persistent session storage ---
    if "student_name" not in st.session_state:
        st.session_state.student_name = ""
    if "teacher_name" not in st.session_state:
        st.session_state.teacher_name = ""

    # --- Input form ---
    with st.form("schedule_form", clear_on_submit=False):
        # Student input
        student_name = st.text_input(
            "Enter student name:",
            value=st.session_state.student_name,
            key="student_input"
        )

        # Auto-fill teacher name if assigned
        if student_name and student_name in users and "teacher" in users[student_name]:
            assigned_teacher = users[student_name]["teacher"]
            st.session_state.teacher_name = assigned_teacher
        else:
            assigned_teacher = ""

        teacher_name = st.text_input(
            "Assigned Teacher",
            value=st.session_state.teacher_name or assigned_teacher,
            disabled=True,
            key="teacher_input"
        )

        day = st.selectbox(
            "Select Day",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday","Sunday"],
            key="day_input"
        )

        # Define valid hourly time slots
        time_options = [
            "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
            "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM",
            "9:00 PM", "10:00 PM", "11:00 PM", "12:00 AM"
        ]

        col1, col2 = st.columns(2)
        with col1:
            start_time = st.selectbox("Start Time", time_options, key="start_time")
        with col2:
            end_time = st.selectbox("End Time", time_options, key="end_time")

        submitted = st.form_submit_button("Save Schedule")

    # --- When form is submitted ---
    if submitted:
        if not student_name:
            st.error("⚠️ Please enter a student name.")
            return
        if not assigned_teacher:
            st.error("⚠️ This student does not have an assigned teacher.")
            return
        if not day or not start_time or not end_time:
            st.error("⚠️ Please complete all fields before saving.")
            return

        # Validate time order (optional)
        start_index = time_options.index(start_time)
        end_index = time_options.index(end_time)
        if end_index <= start_index:
            st.error("⚠️ End time must be later than start time.")
            return

        # Combine time slot
        time_slot = f"{start_time} - {end_time}"
        with st.spinner("💾 Saving schedule..."):
            time.sleep(1.5)

            # Load or initialize timetable
            if os.path.exists(TIMETABLE_FILE):
                with open(TIMETABLE_FILE, "r") as f:
                    timetable = json.load(f)
            else:
                timetable = {"students": {}, "teachers": {}}

            # Save schedule for both student and teacher
            timetable["students"].setdefault(student_name, []).append({
                "day": day,
                "time": time_slot,
                "teacher": assigned_teacher
            })
            timetable["teachers"].setdefault(assigned_teacher, []).append({
                "day": day,
                "time": time_slot,
                "student": student_name
            })

            # Write back to file
            with open(TIMETABLE_FILE, "w") as f:
                json.dump(timetable, f, indent=4)

        st.success(f"✅ Added {student_name} with {assigned_teacher} on {day} ({time_slot})")
        time.sleep(1.2)

        # Clear fields after success
        st.session_state.student_name = ""
        st.session_state.teacher_name = ""
        st.rerun()

def view_student_timetable(student_name):
    assigned_teacher(student_name)
    with st.spinner("Fetching your timetable..."):
        time.sleep(1) 
        if not os.path.exists(TIMETABLE_FILE):
            st.warning("⚠️ No timetable file found yet.")
            return

        with open(TIMETABLE_FILE, "r") as f:
            timetable = json.load(f)

    student_records = timetable.get("students", {}).get(student_name, [])

    if not student_records:
        st.warning(f"⚠️ No timetable found for {student_name}")
        return

    rows = [
        {"Day": record.get("day", "N/A"),
         "Time": record.get("time", "N/A")}
        for record in student_records
    ]

    df = pd.DataFrame(rows)
    df.index = df.index + 1
    st.subheader(f"📅 Timetable for {student_name}")
    time.sleep(0.3)
    st.dataframe(df, use_container_width=True)


def view_teacher_schedule(teacher_name):
    with st.spinner("Loading your schedule..."):
        time.sleep(1)
        if not os.path.exists(TIMETABLE_FILE):
            st.warning("⚠️ No timetable file found yet.")
            return

        with open(TIMETABLE_FILE, "r") as f:
            timetable = json.load(f)

    teacher_records = timetable.get("teachers", {}).get(teacher_name, [])
    if not teacher_records:
        st.warning(f"📂 No timetable found for {teacher_name}")
        return

    # --- Sort by weekday order ---
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    teacher_records.sort(
        key=lambda x: day_order.index(x.get("day", "Monday")) if x.get("day") in day_order else 7
    )

    # --- Group by day ---
    grouped = {}
    for slot in teacher_records:
        day = slot.get("day", "Unknown")
        grouped.setdefault(day, []).append(slot)

    st.subheader(f"📅 Schedule for {teacher_name}")
    time.sleep(0.4)

    # --- Build table rows without repeating day names ---
    rows = []
    for day, slots in grouped.items():
        for i, slot in enumerate(slots):
            rows.append({
                "Day": day if i == 0 else "",  # ✅ show day only once
                "Time": slot.get("time", ""),
                "Student": slot.get("student", "")
            })

    df = pd.DataFrame(rows)
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True)

def view_all_schedules():
    """Admin views all schedules (students + teachers)."""
    with st.spinner("Compiling all schedules..."):
        time.sleep(1.2)
        if not os.path.exists(TIMETABLE_FILE):
            st.info("No schedules found yet.")
            return

        with open(TIMETABLE_FILE, "r") as f:
            timetable = json.load(f)

    rows = []
    index = 1
    for student, schedules in timetable.get("students", {}).items():
        first_row = True
        for sched in schedules:
            rows.append({
                "Index": index if first_row else "",
                "Student": student if first_row else "",
                "Day": sched["day"],
                "Time": sched["time"],
                "Teacher": sched["teacher"]
            })
            first_row = False
        index += 1

    # Convert to DataFrame
    df = pd.DataFrame(rows)
    if "Index" in df.columns:
        df.set_index("Index", inplace=True)

    st.subheader("📅 All Schedules")
    time.sleep(0.3)
    st.dataframe(df, use_container_width=True)
