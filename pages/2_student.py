
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load subject-specific vectorstores
bio_vectorstore = Chroma(persist_directory="vectorstore/ncert_bio_11", embedding_function=embedding_model)
chem_vectorstore = Chroma(persist_directory="vectorstore/ncert_chem_11", embedding_function=embedding_model)
phy_vectorstore = Chroma(persist_directory="vectorstore/ncert_phy_11", embedding_function=embedding_model)


# Load Gemini API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "models/gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)  # ✅ Add this line



# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(page_title="AI Learning Assistant", layout="wide")
st.title("📚 AI Learning Assistant")
st.write(f"Welcome, **{st.session_state.get('user', 'Student')}**")

# ------------------------------
# Tabs
# ------------------------------
tabs = st.tabs(["📘 Smart Notes", "🧪 Quiz + Question Bank", "📄 Answer Review"])

# ------------------------------
# 📘 Smart Notes Tab
# ------------------------------
with tabs[0]:
    st.subheader("📘 Generate Study Notes and Quiz")

    topic = st.text_input("Enter a topic you want to learn about")
    note_level = st.selectbox("Choose your level of understanding", ["Beginner", "Intermediate", "Advanced"])
    st.session_state.note_level = note_level  # Store for use in quiz

    if topic and st.button("🧠 Generate Notes"):
        with st.spinner("Generating notes..."):
            prompt_notes = f"""
Write {note_level.lower()}-level NCERT Class 11 Biology notes for the topic: "{topic}".

- Use simple language and clear explanations suited to a {note_level.lower()} student.
- Avoid MCQs or questions.
- Use bullet points or short paragraphs.
"""
            model = genai.GenerativeModel(MODEL_NAME)
            response_notes = model.generate_content(prompt_notes)
            notes = response_notes.text.strip()
            st.session_state.generated_notes = notes
            st.markdown(f"### 📝 {note_level} Level Study Notes")
            st.markdown(notes)

    if "generated_notes" in st.session_state:
        if st.checkbox("❓ Generate Quiz for this topic"):
            num_questions = st.slider("Select number of MCQs", 1, 10, 5)

            if st.button("📝 Generate Quiz"):
                with st.spinner("Creating questions..."):
                    level_instruction = {
                        "Beginner": "Basic recall questions with simple options",
                        "Intermediate": "Application-based questions with moderate difficulty",
                        "Advanced": "Conceptual, reasoning-based questions for deep understanding"
                    }

                    prompt_mcq = f"""
Generate {num_questions} NCERT Class 11 Biology MCQs on the topic: "{topic}".
Student level: {note_level}
Instructions: {level_instruction[note_level]}

Each question must follow this format:
Q1. <question text>
     A. Option A
     B. Option B
     C. Option C
     D. Option D
Answer: <Correct Option Letter>

Return only the questions in the above format.
"""
                    response_mcq = model.generate_content(prompt_mcq)
                    quiz = response_mcq.text.strip()
                    st.session_state.generated_questions = quiz
                    st.markdown("### 🧪 Quiz Based on Notes Level")
                    st.markdown(quiz)

# ------------------------------
# 🧪 Quiz + Question Bank Tab
# ------------------------------
with tabs[1]:
    st.subheader("🧪 Upload Your Own Questions")
    custom_q_topic = st.text_input("Topic for your questions")
    user_questions = st.text_area("Paste your questions and answers here", height=200)

    if user_questions and st.button("🤖 Review My Q&A"):
        with st.spinner("Reviewing your content..."):
            prompt_custom = f"""
You are an expert NCERT teacher. Review the following questions and answers from a student on the topic: "{custom_q_topic}".
{user_questions}

Give detailed feedback and corrections for each question.
Also provide suggested NCERT page number if a concept is unclear or incorrect.
"""
            model = genai.GenerativeModel(MODEL_NAME)
            review_response = model.generate_content(prompt_custom)
            st.markdown("### 🧾 Feedback on Submitted Q&A")
            st.markdown(review_response.text.strip())

# ------------------------------
# 📄 Answer Review Tab
# ------------------------------
with tabs[2]:
    st.subheader("📄 Review Your Written Answer")
    review_mode = st.radio("Choose input method:", ["✍️ Write manually", "📤 Upload answer sheet"])
    user_answer_text = ""

    if review_mode == "✍️ Write manually":
        user_answer_text = st.text_area("Write or paste your answer here", height=200)
    else:
        uploaded_file = st.file_uploader("Upload your answer sheet (PDF or TXT)", type=["pdf", "txt"])
        if uploaded_file is not None:
            if uploaded_file.type == "text/plain":
                user_answer_text = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/pdf":
                from PyPDF2 import PdfReader
                reader = PdfReader(uploaded_file)
                user_answer_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    if user_answer_text.strip() and st.button("🧠 Get Feedback on Answer"):
        with st.spinner("Analyzing your answer..."):
            feedback_prompt = f"""
You are a supportive and experienced NCERT biology teacher reviewing a student's written answer:

{user_answer_text}

Give feedback in a natural, teacher-like tone, just as you would while writing comments on a student's answer sheet.

- First, comment on the overall understanding and accuracy of the student's answer.
- Point out any scientific or conceptual mistakes, gently correcting them.
- Offer constructive suggestions on how the student can improve the structure, explanation, and use of scientific terms.
- If the answer is missing key concepts or explanations, highlight what they missed and why it's important.
- Mention which specific NCERT textbook topic and **page number** the student should refer to for a better understanding.
- Finally, estimate a fair **score out of 10**, and include 1-2 motivating lines encouraging them to improve.

Keep your tone warm, respectful, and motivating—like a teacher who wants the student to grow and succeed.
"""
            model = genai.GenerativeModel(MODEL_NAME)
            feedback_response = model.generate_content(feedback_prompt)
            feedback = feedback_response.text.strip()
            st.markdown("### 🧾 AI Feedback")
            st.markdown(feedback)
    elif not user_answer_text:
        st.info("Write or upload your answer above to receive feedback.")


