from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    chat_history: str = ""

class ChatResponse(BaseModel):
    response: str