from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Category

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/')
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post('/')
def create_category(name: str, description: str = '', db: Session = Depends(get_db)):
    category = Category(name=name, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get('/{category_id}')
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail='分类不存在')
    return category 