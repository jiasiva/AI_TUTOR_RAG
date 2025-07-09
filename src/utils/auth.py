
import streamlit as st

# Sample user database (username: {password, role})
USER_DB = {
    "teacher1": {"password": "teach123", "role": "Teacher"},
    "student1": {"password": "stud123", "role": "Student"},
    "student2": {"password": "pass456", "role": "Student"},
}

def login_user():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        st.title("🔐 Login to NCERT Adaptive RAGL Chatbot")

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                user_data = USER_DB.get(username)
                if user_data and user_data["password"] == password:
                    st.success("Login successful!")
                    st.session_state.user = {"username": username, "role": user_data["role"]}
                else:
                    st.error("Invalid username or password")

        st.stop()  # Stop further rendering until user logs in

    return st.session_state.user
