import json
import os
import streamlit as st
from users.student import Student
from users.teacher import Teacher
from users.admin import Admin
from ciper import caesar_encrypt,caesar_decrypt
import time

SHIFT = 3
# File to store users
USER_FILE = "users.json"

# Initialize file if not exists
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

def reset_users():
    with open(USER_FILE, "w") as f:
        json.dump({}, f)
    print("✅ User file reset to empty.")        


def signup():
    """Streamlit-based signup form"""
    st.subheader("📝 Create Account")

    users = load_users()

    if "signed_up" not in st.session_state:
        st.session_state["signed_up"] = False

    if not st.session_state["signed_up"]:  
        # --- Sign Up Form ---
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["Student", "Teacher", "Admin"])

            # Stage selection only if student
            stage = None
            if role == "Student":
                age = st.number_input("Enter your age", min_value=5, max_value=18, step=1)

                # Auto-assign stage based on age bracket
                if 5 <= age <= 7:
                    stage = "Adventurer"
                elif 8 <= age <= 12:
                    stage = "Creator"
                elif 12 <= age <= 19:
                    stage = "Innovator"
                else:
                    stage = "Unassigned"

                st.info(f"🎯 Based on your age, your stage is: **{stage}**")

            submitted = st.form_submit_button("Sign Up")

        # --- Process Signup ---
        if submitted:
            full_name = name.strip().title()

            if full_name in users:  # ✅ Full name must be unique
                st.error("⚠️ Full name already exists. Try another one.")
                time.sleep(1)
            elif not full_name or not password:
                st.error("⚠️ Full name and password cannot be empty.")
                time.sleep(1)
            else:
                with st.spinner("🔐 Creating your account..."):
                    encrypted_pw = caesar_encrypt(password, SHIFT)
                    users[full_name] = {
                        "username": username,
                        "password": encrypted_pw,
                        "role": role
                    }

                    if role == "Student":
                        users[full_name]["stage"] = stage

                    save_users(users)
                    time.sleep(1.5)  # Small delay for realism

                st.session_state["signed_up"] = True
                st.success("✅ Account created successfully! Redirecting...")
                time.sleep(1.2)
                st.rerun()

    else:
        # --- After Successful Signup ---
        st.success("✅ Account created successfully!")
        time.sleep(1)
        if st.button("➡️ Go to Login"):
            st.session_state["page"] = "Login"
            st.session_state["signed_up"] = False
            st.rerun()



def login():
    """Streamlit-based login form"""
    st.subheader("🔑 Login")

    users = load_users()

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        found = False  # ✅ Start with False

        for full_name, details in users.items():
            if details["username"] == username:
                found = True  # ✅ username exists
                if caesar_decrypt(details["password"], SHIFT) == password:
                    role = details["role"]

                    st.success("✅ Login successful! Redirecting to your dashboard...")
                    with st.spinner("Loading your profile..."):
                        time.sleep(1.5)

                    if role == "Student":
                        return Student(full_name, details["username"], details["stage"])
                    elif role == "Teacher":
                        return Teacher(details["username"])
                    elif role == "Admin":
                        return Admin(full_name, details["username"])
                    else:
                        st.error("Unknown role")
                        return None
                else:
                    st.error("Incorrect password")
                    time.sleep(1)
                    return None

        if not found:  # ✅ only show after loop finishes
            st.error("Username not found")
            time.sleep(1)

    return None

def reset_password():
    """Streamlit-based password reset"""
    st.subheader("🔑 Reset Password")

    users = load_users()

    with st.form("reset_form"):
        username = st.text_input("Enter your username")
        name = st.text_input("Enter your full name (for verification)")
        new_password = st.text_input("Enter new password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        submitted = st.form_submit_button("Reset Password")

    if submitted:
        # 🔍 Find user by username + name
        matched_user = None
        for full_name, details in users.items():
            if (
                details["username"] == username
                and full_name.lower() == name.strip().title().lower()
            ):
                matched_user = full_name
                break

        if not matched_user:
            st.error("❌ Username and full name do not match our records.")
            time.sleep(1)
            return
        if not new_password:
            st.error("⚠️ Password cannot be empty.")
            time.sleep(1)
            return
        if new_password != confirm_password:
            st.error("⚠️ Passwords do not match.")
            time.sleep(1)
            return

        # ✅ Encrypt and update password
        encrypted_pw = caesar_encrypt(new_password, SHIFT)
        users[matched_user]["password"] = encrypted_pw
        save_users(users)

        st.success("✅ Password has been reset successfully! Please login with your new password.")
        time.sleep(1.2)
