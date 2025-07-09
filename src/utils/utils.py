import google.generativeai as genai

# Set your Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your actual key

# Gemini model to use
MODEL_NAME = "models/gemini-1.5-flash"

def generate_quiz_from_topic(ragl, topic, num_questions=5):
    """
    Generates multiple-choice quiz questions on a given topic using Gemini.

    Args:
        ragl: RAGL system instance (not used in this simple version, but kept for compatibility).
        topic (str): Topic to generate quiz on.
        num_questions (int): Number of questions to generate.

    Returns:
        str: Generated quiz content as plain text or markdown.
    """
    prompt = f"""
    You are an intelligent quiz generator. Generate {num_questions} multiple choice questions on the topic "{topic}".
    For each question, include:
    - The question text
    - Four options labeled A to D
    - Indicate the correct answer clearly at the end

    Format:
    Q1. ...
    A. ...
    B. ...
    C. ...
    D. ...
    Answer: B
    """

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text.strip()
