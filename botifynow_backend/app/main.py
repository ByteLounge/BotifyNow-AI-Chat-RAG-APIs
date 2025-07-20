from fastapi import FastAPI, File, UploadFile, HTTPException
from app.models import ChatRequest, RAGRequest
from app.services.openai_service import chat_with_gpt, rag_chat
from app.services.qdrant_service import store_document, generate_doc_id
from app.utils.pdf_extractor import extract_text_from_pdf

import os
import shutil

app = FastAPI(title="BotifyNow AI APIs")


@app.post("/chat")
async def chat_api(request: ChatRequest):
    try:
        response = chat_with_gpt(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_api(file: UploadFile = File(...)):
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(temp_file_path)
        elif file.filename.endswith(".txt"):
            with open(temp_file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            raise HTTPException(status_code=400, detail="Only PDF or TXT files allowed")

        os.remove(temp_file_path)

        # Store in Qdrant
        document_id = generate_doc_id()
        store_document(document_id, text)

        return {
            "message": "Document uploaded successfully",
            "document_id": document_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rag-chat")
async def rag_chat_api(request: RAGRequest):
    try:
        response = rag_chat(request.message, request.document_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Backend is running ✅"}
