import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
from src.utils.state import init_ragl_system
from dotenv import load_dotenv

# --------------------------------------------------------------------
# 🔐 Load Gemini API Key
# --------------------------------------------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "models/gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# --------------------------------------------------------------------
# ⚙️ Initialize RAGL System in Session State
# --------------------------------------------------------------------
init_ragl_system()
st.title("👨‍🏫 Teacher Dashboard")
ragl_system = st.session_state.ragl_system  # ✅ Correct way to retrieve the object

# --------------------------------------------------------------------
# 1. 📤 Upload NCERT Chapter to Knowledge Base
# --------------------------------------------------------------------
st.subheader("📘 Upload NCERT Chapter")
uploaded_file = st.file_uploader("Upload a CSV or Text file", type=["csv", "txt"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    metadata = {
        "filename": uploaded_file.name,
        "upload_timestamp": datetime.now().isoformat(),
        "source": "teacher_upload"
    }

    # ✅ Add document using method from RAGLSystem
    ragl_system.add_documents([content], [metadata])
    st.success(f"✅ Uploaded {uploaded_file.name} and added to the knowledge base.")

# --------------------------------------------------------------------
# 2. ❓ Question Bank Generator (Based on PYQs)
# --------------------------------------------------------------------
st.subheader("❓ Generate Question Bank from PYQs")
subject = st.text_input("Subject (e.g., Biology Class 12)")
chapters = st.text_area("Relevant Chapters (comma-separated)")
num_questions = st.slider("Number of Questions", 5, 20, 10)

if st.button("Generate Question Bank"):
    if subject and chapters:
        prompt = f"""
        Based on previous year question trends, generate {num_questions} exam-style questions.
        Subject: {subject}
        Chapters: {chapters}
        Include a mix of short and long questions. Format clearly.
        """
        try:
            response = model.generate_content(prompt)
            st.success("📘 Question Bank Generated")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Failed to generate questions: {e}")
    else:
        st.warning("Please fill in subject and chapters.")

# --------------------------------------------------------------------
# 3. 📋 AI-Powered Lesson Plan Generator
# --------------------------------------------------------------------
st.subheader("📋 Lesson Plan Generator")
lesson_topic = st.text_input("Lesson Topic")
objectives = st.text_area("Learning Objectives (comma-separated)")
duration = st.selectbox("Select Duration", ["30 mins", "45 mins", "1 hour"])
activities = st.text_area("Activities (e.g., quiz, discussion, diagram)")

if st.button("Generate Lesson Plan"):
    if lesson_topic and objectives and activities:
        prompt = f"""
        Create a structured lesson plan.

        Topic: {lesson_topic}
        Duration: {duration}
        Learning Objectives: {objectives}
        Activities: {activities}

        Return the output in a readable markdown format.
        """
        try:
            response = model.generate_content(prompt)
            st.success("📘 Lesson Plan Generated")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Failed to generate lesson plan: {e}")
    else:
        st.warning("Please fill in all fields.")
