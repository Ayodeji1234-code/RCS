import streamlit as st
from authentication import signup, login , reset_password
from users.teacher import Teacher
import time

st.set_page_config(page_title="School Management System", layout="centered")

def main():
    """
    Main entry point of the app.
    
    - Displays the app title.
    - Checks if a user is logged in via session state.
    - If logged in: loads the dashboard.
    - If not logged in: shows sidebar menu with Home, Sign Up, Login.
    """
    st.title("School Management System")
   

    # ✅ Keep user logged in across reruns
    if "user" in st.session_state and st.session_state["user"]:
        dashboard(st.session_state["user"])   # jump straight to dashboard
    else:
        if "page" not in st.session_state:
            st.session_state["page"] = "Home"

        # --- Handle pages ---
        if st.session_state["page"] == "Home":
            st.subheader("🏫 Welcome To Rubies Code School")
            st.subheader("Learning to code...")
            st.write("Please **Sign Up** if you're new, or **Login** if you already have an account.")

            # 👉 Signup button
            if st.button("Sign Up"):
                st.session_state["page"] = "Sign Up"
                st.rerun()

            # 👉 Login button
            if st.button("Login"):
                st.session_state["page"] = "Login"
                st.rerun()

        elif st.session_state["page"] == "Sign Up":
            signup()

            if st.button("Back"):
                st.session_state["page"] = "Home"
                st.rerun()

        elif st.session_state["page"] == "Login":
            user = login()

            if st.button("Forgot Password?"):
                st.session_state["page"] = "Forgot Password"
                reset_password()
                st.rerun()

            if st.button("Back"):
                st.session_state["page"] = "Home"
                st.rerun()

            if user:
                st.session_state["user"] = user
                st.rerun()  # reload so dashboard shows immediately

        elif st.session_state["page"] == "Forgot Password":
            reset_password()

            if st.button("Back to Login"):
                st.session_state["page"] = "Login"
                st.rerun()
                
def dashboard(user):
    """
    Dashboard for logged-in users.
    
    - Displays a sidebar menu with actions from `user.get_actions()`.
    - Handles special cases:
        * Profile → show user info
        * Logout → clear session + rerun app
    
    Args:
        user (User): The logged-in user object with attributes `name`, `role`, 
                     and methods `get_actions()` and `action(choice)`.
    """
    
    
    st.sidebar.subheader("Dashboard Menu")
    options = user.get_actions()
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "Profile":
        user.view_profile()
    elif choice == "Logout":
        with st.spinner("🚪 Logging you out..."):
            time.sleep(1.5)  # Short delay for realism
        st.success("👋 You have been logged out. See you soon!")
        time.sleep(1.2)
        st.session_state["user"] = None
        st.rerun()

    else:
        user.action(choice)

if __name__ == "__main__":
    main()
