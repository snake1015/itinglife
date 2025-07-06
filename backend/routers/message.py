from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Message
from schemas import MessageOut
from typing import List

router = APIRouter()

@router.post('', response_model=MessageOut)
def create_message(content: str, user_id: int = None, db: Session = Depends(get_db)):
    message = Message(content=content, user_id=user_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get('', response_model=List[MessageOut])
def list_messages(db: Session = Depends(get_db)):
    return db.query(Message).order_by(Message.created_at.desc()).all()

@router.delete('/{message_id}')
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail='留言不存在')
    db.delete(message)
    db.commit()
    return {"success": True} 