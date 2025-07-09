
# 🎓 Adaptive Retrieval-Augmented Generation Learning (RAGL) System

**AI_TUTOR_RAG** is a multimodal, AI-powered educational assistant designed for personalized learning. It combines document-based retrieval, large language model generation, and role-based dashboards for students and teachers. The system supports real-time quiz generation, chatbot Q&A, lesson planning, and answer paper review.

📺 **Demo**: [Watch on YouTube](#) *(Add your demo link)*

---

## 📘 Project Overview

The Adaptive RAGL System enhances student learning using Retrieval-Augmented Generation (RAG) architecture. It supports document uploads in multiple formats, uses semantic search to fetch relevant content, and generates responses using local or cloud-based LLMs like Zephyr and Gemini.

It features:
- A **Student Dashboard** for quiz taking, chatbot learning, and answer review
- A **Teacher Dashboard** for uploading materials, generating quizzes, and planning lessons

---

## 🔑 Key Features

### 🧑‍🎓 Student Dashboard
- 🤖 Ask questions through a chatbot trained on uploaded documents
- 📝 Take auto-generated quizzes based on uploaded syllabus
- 📤 Upload answer papers (TXT/PDF) for review
- 📊 Track learning sessions and performance data

### 👩‍🏫 Teacher Dashboard
- 📚 Upload classroom materials (PDF, DOCX, PPTX, etc.)
- 📝 Generate quizzes by topic
- 📄 Generate lesson plans automatically
- 📈 View and track quiz data

### 🗃️ Multi-Format Document Support
Supports uploading and processing:
- PDF, DOC, DOCX, TXT, CSV
- PPT, PPTX, XLS, XLSX
- HTML, JSON, XML, Markdown (MD)

### 🧠 Learning Capabilities
- Adaptive document chunking and retrieval
- FAISS/Chroma vector database search
- Feedback-based learning event logging
- Metadata tracking for content source and sessions

---

## ⚙️ Technical Architecture

| Layer       | Tools Used |
|-------------|-------------|
| Backend     | Python 3.12, FAISS, Chroma, LangChain, PyPDF2, python-docx, pandas, python-pptx |
| Frontend    | Streamlit, Custom CSS |
| LLM Engine  | Zephyr via Ollama (default), Gemini via API (optional) |
| Storage     | CSV logs, FAISS indexes, Chroma SQLite DBs |

### 🧱 Core Components

- **Vector DB**: FAISS/Chroma for semantic document retrieval
- **RAG Engine**: Combines retrieved chunks with prompts for LLM generation
- **Document Processor**: Uses format-specific loaders and chunking logic
- **LLMs**: 
  - Offline: `Zephyr` (via Ollama)
  - Online (optional): `Gemini` (via API key)
- **Dashboards**: Role-based features for teachers and students

---

## 🛠️ Setup Instructions

### 📋 Prerequisites
- Python 3.12+
- Git
- Ollama installed
- *(Optional)* Google Gemini API Key for online LLM access

### 🔧 Installation
git clone https://github.com/jiasiva/AI_TUTOR_RAG.git
cd AI_TUTOR_RAG
python -m venv env
env\Scripts\activate     # Windows
# OR
source env/bin/activate  # macOS/Linux

pip install -r requirements.txt


### 🔐 Environment Setup (for Gemini)

Create a `.env` file in the root directory and add:

GEMINI_API_KEY=your_gemini_api_key_here



### ▶️ Run the Application

 # Start LLM if using Ollama
ollama run zephyr

# Then start the app
streamlit run app.py
then open your browser and visit: http://localhost:8501

### 📚 How to Use

**👩‍🏫 For Teachers**
1.Upload documents related to topics (PDFs, PPTs, DOCX, etc.)
2.Use the dashboard to generate quizzes
3.Export/share quiz questions
4.Use the lesson plan generator for daily planning

**🧑‍🎓 For Students**
1.Ask subject-related questions in the chatbot
2.Participate in quizzes
3.Upload answer sheets for review (PDF/TXT)

### 🔮 Future Enhancements:
 
🗣️ Voice-based input and speech response
🧾 OCR for scanned answer paper analysis
📊 Visual dashboards for student progress
🌐 Multilingual support (e.g., Tamil, Hindi)
🧠 Personalized learning path suggestions
⚡ Caching and faster document processing
