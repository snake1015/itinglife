from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Message

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/')
def create_message(content: str, user_id: int = None, db: Session = Depends(get_db)):
    message = Message(content=content, user_id=user_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get('/')
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