from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Message
from schemas import MessageCreate, Message as MessageSchema

router = APIRouter()

@router.get("/{student_id}", response_model=List[MessageSchema])
def get_messages(student_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(
        Message.student_id == student_id
    ).order_by(Message.created_at.desc()).limit(50).all()

@router.post("/", response_model=MessageSchema)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
