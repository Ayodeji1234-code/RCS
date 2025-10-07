import streamlit as st
import json
import os,time

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def system_report():
    st.subheader("📊 System Report")

    users = load_users()
    if not users:
        st.info("⚠️ No users found in the system yet.")
        return
    
    with st.spinner("Generating system report..."):
        time.sleep(1.2) 

    st.divider()
    # --- Teachers ---
    teachers = [name for name, info in users.items() if info.get("role", "").lower() == "teacher"]
    st.write(f"👩‍🏫 **Teachers:** {len(teachers)}")
    with st.expander("View Teachers"):
        for i, teacher in enumerate(teachers, start=1):
            st.write(f"{i}. {teacher}")

    st.divider()        

    # --- Students by Stage ---
    stages = {}
    for name, info in users.items():
        if info.get("role", "").lower() == "student":
            stage = info.get("stage", "Unassigned")
            stages.setdefault(stage, []).append(name)

    st.write("🎓 **Students by Stage:**")
    for stage, students in stages.items():
        st.write(f"- **{stage}**: {len(students)} student(s)")
        with st.expander(f"View {stage} Students"):
            for i, student in enumerate(students, start=1):
                st.write(f"{i}. {student}")
                
    st.divider()

    # --- Admins ---
    admins = [name for name, info in users.items() if info.get("role", "").lower() == "admin"]
    st.write(f"🛠️ **Admins:** {len(admins)}")
    with st.expander("View Admins"):
        for i, admin in enumerate(admins, start=1):
            st.write(f"{i}. {admin}")
