import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load Gemini API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-1.5-flash"

# ------------------------------
# Generate MCQ Quiz from Topic
# ------------------------------
def generate_quiz_from_topic(topic, num_questions=5):
    prompt = f"""
Generate {num_questions} multiple-choice questions (MCQs) from the topic: "{topic}".
Each question should have 4 options (A, B, C, D), with the correct answer clearly marked.

Example format:
Q1. What is the powerhouse of the cell?
A. Nucleus
B. Mitochondria
C. Chloroplast
D. Ribosome
Answer: B

Only return quiz in the above format.
"""
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip()

# ------------------------------
# Evaluate Quiz (optional stub)
# ------------------------------
def evaluate_quiz(user_answers, correct_answers):
    score = 0
    for u, c in zip(user_answers, correct_answers):
        if u.strip().upper() == c.strip().upper():
            score += 1
    return score, len(correct_answers)
