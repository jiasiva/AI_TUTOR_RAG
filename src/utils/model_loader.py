import os
import sys
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Add the parent directory to path to resolve imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.config import GEMINI_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS

def load_llm():
    """Load and configure the Gemini LLM."""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key not found. Please set it in your .env file.")

    return GoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GEMINI_API_KEY,
        temperature=TEMPERATURE,
        max_output_tokens=MAX_TOKENS,
    )

def create_rag_chain(retriever):
    """Create a RAG chain with the provided retriever."""
    llm = load_llm()

    template = """
    You are an adaptive AI assistant powered by a retrieval-augmented generation system.
    You have access to a knowledge base that is continuously updated with new information.

    When answering, use the following context information as your main source of knowledge,
    but also apply your general knowledge and reasoning abilities.

    Context information:
    {context}

    User question: {question}

    Instructions:
    - Provide a comprehensive and accurate answer using the context and your knowledge.
    - If the context doesn't provide enough information, acknowledge the limitations.
    - If the user provides new information that isn't in the context, consider it as valuable input.

    Answer:
    """

    prompt = PromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_context(query):
        docs = retriever(query)
        return format_docs(docs)

    def rag_chain(query):
        context = get_context(query)

        if not context.strip():
            response = llm.invoke(query)
            return response if isinstance(response, str) else response.text

        formatted_prompt = prompt.format(context=context, question=query)
        response = llm.invoke(formatted_prompt)
        return response if isinstance(response, str) else response.text

    return rag_chain
    