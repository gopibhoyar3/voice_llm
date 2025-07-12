from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_message: str
    rag_context: str = ""