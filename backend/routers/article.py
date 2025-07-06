from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Article, Category, User
from schemas import ArticleOut

router = APIRouter()

@router.post('/', response_model=ArticleOut)
def create_article(title: str, content: str, summary: str = '', category_id: int = None, tags: str = '', author_id: int = None, is_featured: bool = False, db: Session = Depends(get_db)):
    article = Article(title=title, content=content, summary=summary, category_id=category_id, tags=tags, author_id=author_id, is_featured=is_featured)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@router.get('/', response_model=List[ArticleOut])
def list_articles(category_id: Optional[int] = None, tag: Optional[str] = None, is_featured: Optional[bool] = None, author_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Article)
    if category_id:
        query = query.filter(Article.category_id == category_id)
    if tag:
        query = query.filter(Article.tags.like(f'%{tag}%'))
    if is_featured is not None:
        query = query.filter(Article.is_featured == is_featured)
    if author_id:
        query = query.filter(Article.author_id == author_id)
    return query.order_by(Article.created_at.desc()).all()

@router.get('/hot', response_model=List[ArticleOut])
def hot_articles(db: Session = Depends(get_db)):
    # 简单以评论数排序，实际可按访问量等
    return db.query(Article).order_by(Article.created_at.desc()).limit(10).all()

@router.get('/{article_id}', response_model=ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail='文章不存在')
    return article

@router.put('/{article_id}', response_model=ArticleOut)
def update_article(article_id: int, title: str = None, content: str = None, summary: str = None, category_id: int = None, tags: str = None, is_featured: bool = None, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail='文章不存在')
    if title is not None:
        article.title = title
    if content is not None:
        article.content = content
    if summary is not None:
        article.summary = summary
    if category_id is not None:
        article.category_id = category_id
    if tags is not None:
        article.tags = tags
    if is_featured is not None:
        article.is_featured = is_featured
    db.commit()
    db.refresh(article)
    return article

@router.delete('/{article_id}')
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail='文章不存在')
    db.delete(article)
    db.commit()
    return {"success": True} 