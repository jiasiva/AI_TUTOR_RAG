import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document  # Use langchain_core, not langchain.schema
import os

# Load your CSV
df = pd.read_csv("data/Chemistry_11th_Cleaned.csv")

# Convert each row into a LangChain Document
docs = []
for _, row in df.iterrows():
    text = f"""
Topic: {row['Topic']}
Explanation: {row['Explanation']}
Question: {row['Question']}
Answer: {row['Answer']}
Difficulty: {row['Difficulty']}
Student Level: {row['StudentLevel']}
Question Type: {row['QuestionType']}
Complexity: {row['QuestionComplexity']}
Estimated Time: {row['EstimatedTime']}
Grade: {row['grade']}
"""

    doc = Document(
        page_content=text,
        metadata={
            "topic": row['Topic'],
            "subject": row['subject'],
            "grade": row['grade']
        }
    )
    docs.append(doc)

# Set up the embedding model (make sure you have internet or it's downloaded)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS vectorstore
db = FAISS.from_documents(docs, embedding_model)

# Save vectorstore locally
if not os.path.exists("vectorstore"):
    os.makedirs("vectorstore")

db.save_local("vectorstore/ncert_chem_11")
print("Vectorstore saved at vectorstore/ncert_chem_11")
