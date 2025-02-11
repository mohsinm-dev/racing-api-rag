from pydantic import BaseModel

class ChatSessionCreate(BaseModel):
    session_id: str
    user_id: str
    chat_history: str = ""

class ChatSessionUpdate(BaseModel):
    chat_history: str