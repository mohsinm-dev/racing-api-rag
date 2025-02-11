# app/api/endpoints/chat.py
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi import APIRouter,Depends
from app.services.query_handler import process_query
from app.pydantic_models.chat import ChatRequest,ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse, summary="Chat endpoint to process user query")
def chat_endpoint(chat_request: ChatRequest, db: Session = Depends(get_db)):
    context = process_query(chat_request.query, chat_request.chat_history, db)
    return ChatResponse(response=context)
