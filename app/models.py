from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    mode: str  # "rag" или "sql"

class ChatResponse(BaseModel):
    answer: str

class UploadResponse(BaseModel):
    message: str
    chunks_added: int