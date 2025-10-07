import json , time
import os
import streamlit as st
import pandas as pd

USER_FILE = "users.json"

# --- Helpers ---
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --- Manage Users (Admin only) ---
def manage_users():
    st.subheader("👥 Manage Users")

    users = load_users()

    if not users:
        st.info("No users found.")
        return

    st.write("### 📋 Users List")

    # List each user with a delete button
    for username, details in users.items():
        col1, col2, col3 = st.columns([3, 3, 1])  # layout: name, role, delete btn
        with col1:
            st.write(f"{details.get('name','')} {username}")
        with col2:
            st.write(details.get("role", "N/A"))
        with col3:
            if st.button("🗑 Delete", key=f"del_{username}"):
                del users[username]
                save_users(users)
                st.success(f"✅ Deleted user: {username}")
                time.sleep(1.5)
                st.rerun()