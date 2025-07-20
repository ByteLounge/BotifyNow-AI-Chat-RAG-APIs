import openai
import os
from app.services.qdrant_service import search_document

# ✅ Set API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Normal GPT Chat
def chat_with_gpt(user_input: str):
    """
    Simple chatbot response without RAG.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # ✅ Updated to a universally available model
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ✅ RAG Chat (Uses context from Qdrant search)
def rag_chat(query: str, document_id: str):
    """
    Retrieves context from Qdrant, then sends query + context to OpenAI for a better answer.
    """
    try:
        # 🔍 Fetch related document context
        context = search_document(query, document_id)

        if not context:
            return "❌ No relevant document context found."

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # ✅ Updated to avoid `gpt-3.5-turbo` restrictions
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert assistant. Use this document context to answer the user:\n\n{context}"
                },
                {"role": "user", "content": query}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"
