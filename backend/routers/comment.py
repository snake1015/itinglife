from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Comment
from schemas import CommentOut, CommentCreate
from typing import List

router = APIRouter()

@router.post('', response_model=CommentOut)
def create_comment(comment_data: CommentCreate, db: Session = Depends(get_db)):
    comment = Comment(content=comment_data.content, article_id=comment_data.article_id, user_id=getattr(comment_data, 'user_id', None))
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get('', response_model=List[CommentOut])
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