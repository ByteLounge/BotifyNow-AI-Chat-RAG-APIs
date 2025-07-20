from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class RAGRequest(BaseModel):
    message: str
    document_id: str
