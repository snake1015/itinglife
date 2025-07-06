from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Article, Category, User
from schemas import ArticleOut, ArticleCreate

router = APIRouter()

@router.post('', response_model=ArticleOut)
def create_article(article_data: ArticleCreate, db: Session = Depends(get_db)):
    article = Article(
        title=article_data.title,
        content=article_data.content,
        summary=article_data.summary or '',
        category_id=article_data.category_id,
        tags=article_data.tags or '',
        is_featured=article_data.is_featured
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@router.get('', response_model=List[ArticleOut])
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
def update_article(article_id: int, article_data: ArticleCreate, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail='文章不存在')
    
    article.title = article_data.title
    article.content = article_data.content
    article.summary = article_data.summary or ''
    article.category_id = article_data.category_id
    article.tags = article_data.tags or ''
    article.is_featured = article_data.is_featured
    
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