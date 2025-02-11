# app/api/endpoints/session.py
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.session import ChatSession
from fastapi import APIRouter, HTTPException, Depends
from app.pydantic_models.session import ChatSessionCreate,ChatSessionUpdate

router = APIRouter()


@router.post("/create-session", summary="Create a new chat session")
def create_chat_session(session_data: ChatSessionCreate, db: Session = Depends(get_db)):
    existing = db.query(ChatSession).filter(ChatSession.session_id == session_data.session_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Session already exists")
    new_session = ChatSession(
        session_id=session_data.session_id,
        user_id=session_data.user_id,
        chat_history=session_data.chat_history,
        last_updated=datetime.utcnow()
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/{session_id}", summary="Get a chat session by session_id")
def get_chat_session(session_id: str, db: Session = Depends(get_db)):
    session_obj = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_obj

@router.put("/{session_id}", summary="Update chat session history")
def update_chat_session(session_id: str, update: ChatSessionUpdate, db: Session = Depends(get_db)):
    session_obj = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    session_obj.chat_history = update.chat_history
    session_obj.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(session_obj)
    return session_obj

@router.delete("/{session_id}", summary="Delete a chat session")
def delete_chat_session(session_id: str, db: Session = Depends(get_db)):
    session_obj = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session_obj)
    db.commit()
    return {"detail": "Session deleted"}
