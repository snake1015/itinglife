from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Comment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/')
def create_comment(content: str, article_id: int, user_id: int, db: Session = Depends(get_db)):
    comment = Comment(content=content, article_id=article_id, user_id=user_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get('/')
def list_comments(article_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Comment)
    if article_id:
        query = query.filter(Comment.article_id == article_id)
    return query.order_by(Comment.created_at.desc()).all()

@router.delete('/{comment_id}')
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail='评论不存在')
    db.delete(comment)
    db.commit()
    return {"success": True} 