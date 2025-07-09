import streamlit as st

# -----------------------------
# Initialize Session State
# -----------------------------
def init_ragl_system():
    if "ragl_system" not in st.session_state:
        st.session_state.ragl_system = {
            "user": None,
            "topic": None,
            "quiz": [],
            "score": 0
        }

    # Optional: Set default user
    if "user" not in st.session_state:
        st.session_state["user"] = "Student"

    # Initialize chat/quiz state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = []
