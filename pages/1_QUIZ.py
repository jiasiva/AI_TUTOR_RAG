import streamlit as st
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-1.5-flash"

st.set_page_config(page_title="LLM Quiz Generator", page_icon="🧪")
st.title("🧪 Gemini-Powered Quiz Generator")
st.markdown("Upload a text or PDF file, and automatically generate multiple-choice quiz questions using Gemini.")

# --- Helper to extract text from PDF or TXT ---

def extract_text(file):
    if file.type == "application/pdf":
        text = ""
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        return text
    else:
        return file.read().decode("utf-8")

# --- Gemini: Generate Quiz ---
def generate_quiz_gemini(content, num_questions=5):
    prompt = f"""
You are a quiz generator. Based on the content below, generate {num_questions} multiple-choice questions. 
Each question must have 4 options (A, B, C, D) and indicate the correct answer.

Content:
\"\"\"
{content}
\"\"\"

Format:
Q1: <Question>
A. Option A
B. Option B
C. Option C
D. Option D
Answer: B

Only return the quiz in this format.
"""
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip()

# --- UI: Upload File ---
uploaded_file = st.file_uploader("📄 Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    st.success("✅ File uploaded successfully.")
    if st.button("🚀 Generate Quiz"):
        with st.spinner("Generating quiz using Gemini..."):
            text = extract_text(uploaded_file)
            if len(text.strip()) < 100:
                st.warning("The uploaded file has insufficient content.")
            else:
                quiz = generate_quiz_gemini(text)
                st.subheader("📝 Generated Quiz")
                st.markdown(f"```text\n{quiz}\n```")
else:
    st.info("Please upload a `.pdf` or `.txt` file to begin.")

# --- Footer ---
st.markdown("---")
st.markdown("<center>🧠 Powered by Google Gemini & Adaptive RAGL</center>", unsafe_allow_html=True)
