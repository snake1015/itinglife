from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Category
from schemas import CategoryOut, CategoryCreate
from typing import List

router = APIRouter()

@router.get('', response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post('', response_model=CategoryOut)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(name=category_data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get('/{category_id}', response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail='分类不存在')
    return category 