import json
import os , time
import streamlit as st
import pandas as pd
from operations.pairing import load_users

ASSESSMENT_FILE = "assessments.json"

# Initialize file if not exists
if not os.path.exists(ASSESSMENT_FILE):
    with open(ASSESSMENT_FILE, "w") as f:
        json.dump({}, f)


def record_assessment(teacher_name):
    st.subheader("📝 Record Assessment")
# Load users and filter students assigned to this teacher
    users = load_users()
    students = [
        fullname for fullname, info in users.items()
        if info.get("role", "").lower() == "student"
        and info.get("teacher") == teacher_name
    ]

    if not students:
        st.info("⚠️ No students assigned to you yet.")
        return

    # ✅ Select student from assigned list
    student_name = st.selectbox("Select Student", students)

    # Let teacher pick CA or Exam
    assessment_type = st.radio("Select Assessment Type", ["C.A", "Exam"])

    score = st.number_input("Enter score (%)", min_value=0, max_value=100, step=1)

    if st.button("Save Assessment"):
        with st.spinner("Saving assessment..."):
            time.sleep(1)
            with open(ASSESSMENT_FILE, "r") as f:
                assessments = json.load(f)

            if student_name not in assessments:
                assessments[student_name] = {}

            # ✅ Ensure storage is always a list
            if assessment_type not in assessments[student_name]:
                assessments[student_name][assessment_type] = []

            # If it was saved earlier as a string, convert to list
            if isinstance(assessments[student_name][assessment_type], str):
                assessments[student_name][assessment_type] = [assessments[student_name][assessment_type]]

            # ✅ Now append safely
            assessments[student_name][assessment_type].append(f"{score}%")

            with open(ASSESSMENT_FILE, "w") as f:
                json.dump(assessments, f, indent=4)

        st.success(f"✅ Recorded {student_name}'s {assessment_type}: {score}%")
        time.sleep(0.7)

def view_assessments():
    st.subheader("📂 All Assessments")
    with st.spinner("Loading assessments..."):
        time.sleep(1.5)
        # Load data
        if not os.path.exists(ASSESSMENT_FILE):
            st.info("No assessments yet.")
            return
        
        with open(ASSESSMENT_FILE, "r") as f:
            assessments = json.load(f)

    if not assessments:
        st.info("No assessments yet.")
        return

    rows = []
    index = 1  # student numbering

    for student, records in assessments.items():
        ca_scores = records.get("C.A", [])
        exam_scores = records.get("Exam", [])

        # Convert single strings to lists if necessary
        if isinstance(ca_scores, str):
            ca_scores = [ca_scores]
        if isinstance(exam_scores, str):
            exam_scores = [exam_scores]

        # Ensure lists have same length
        max_len = max(len(ca_scores), len(exam_scores))
        ca_scores += [""] * (max_len - len(ca_scores))
        exam_scores += [""] * (max_len - len(exam_scores))

        first_row = True
        for ca, exam in zip(ca_scores, exam_scores):
            try:
                final = (int(str(ca).replace("%", "")) + int(str(exam).replace("%", ""))) / 2
            except:
                final = ""
            
            rows.append({
                "#": index if first_row else "",
                "Student": student if first_row else "",
                "C.A": ca,
                "Exam": exam,
                "Final": final if final != "" else ""
            })
            first_row = False

        # Increment student index **inside the loop** for each student
        index += 1

    # Convert to DataFrame and display
    df = pd.DataFrame(rows)
    time.sleep(0.5)
    st.dataframe(df.set_index("#"), use_container_width=True)

def view_my_assessments(student_name):
    """Allow a student to view only their own assessments"""
    st.subheader(f"📘 {student_name}'s Assessments")
    with st.spinner("Fetching your assessments..."):
        time.sleep(1.5)

        try:
            with open(ASSESSMENT_FILE, "r") as f:
                assessments = json.load(f)
        except FileNotFoundError:
            st.error("⚠️ No assessments file found.")
            return

    student_records = assessments.get(student_name, {})
    if not student_records:
        st.info("⚠️ No assessments recorded for you yet.")
        return

    # Convert scores to integers
    ca_scores = [int(x.replace("%", "").strip()) for x in student_records.get("C.A", [])]
    exam_scores = [int(x.replace("%", "").strip()) for x in student_records.get("Exam", [])]

    # Build dataframe with Average column
    rows = []
    for i in range(max(len(ca_scores), len(exam_scores))):
        ca = ca_scores[i] if i < len(ca_scores) else 0
        exam = exam_scores[i] if i < len(exam_scores) else 0
        average = (ca + exam) / 2
        rows.append({"C.A": ca, "Exam": exam, "Average": round(average, 2)})

    df = pd.DataFrame(rows)
    df.index = df.index + 1
    st.dataframe(df, use_container_width=True)

    # Overall average for comment
    all_scores = ca_scores + exam_scores
    if all_scores:
        overall_avg = sum(all_scores) / len(all_scores)
        time.sleep(0.4)
        if overall_avg >= 70:
            st.success("✅ You're doing great! Keep it up!")
        else:
            st.warning("⚠️ You need to work harder.")


def assessment_summary():
    st.subheader("📊 Assessment Summary")
    with st.spinner("Generating report..."):
        time.sleep(1.5)
        if not os.path.exists(ASSESSMENT_FILE):
            st.info("No assessment records yet.")
            return

        with open(ASSESSMENT_FILE, "r") as f:
            assessments = json.load(f)

    if not assessments:
        st.info("No assessment records yet.")
        return

    rows = []
    index = 1

    for student, scores in assessments.items():
        # Ensure lists even if stored as single strings
        ca_list = scores.get("C.A", [])
        exam_list = scores.get("Exam", [])

        if isinstance(ca_list, str):
            ca_list = [ca_list]
        if isinstance(exam_list, str):
            exam_list = [exam_list]

        # Convert strings to numbers
        ca_values = []
        exam_values = []
        for ca in ca_list:
            try:
                ca_values.append(float(str(ca).replace("%", "")))
            except:
                continue
        for exam in exam_list:
            try:
                exam_values.append(float(str(exam).replace("%", "")))
            except:
                continue

        # Calculate averages
        avg_ca = round(sum(ca_values)/len(ca_values), 2) if ca_values else 0
        avg_exam = round(sum(exam_values)/len(exam_values), 2) if exam_values else 0
        final_score = round(avg_ca*0.4 + avg_exam*0.6, 2) if (ca_values or exam_values) else ""

        status = "⚠️ Needs Intervention" if final_score != "" and final_score < 40 else "✅ On Track"

        rows.append({
            "#": index,
            "Student": student,
            "Avg C.A (%)": avg_ca,
            "Avg Exam (%)": avg_exam,
            "Final Score (%)": final_score,
            "Status": status
        })

        index += 1

    df_summary = pd.DataFrame(rows)
    search_name = st.text_input("Search Student by Name:")

    if search_name:
        df_summary = df_summary[df_summary["Student"].str.contains(search_name, case=False, na=False)]
    time.sleep(1)    
    st.dataframe(df_summary.set_index("#"), use_container_width=True)
