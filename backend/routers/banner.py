from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Banner
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/')
def list_banners(db: Session = Depends(get_db)) -> List[Banner]:
    return db.query(Banner).order_by(Banner.created_at.desc()).all()

@router.post('/')
def create_banner(img: str, link: str = '', db: Session = Depends(get_db)):
    banner = Banner(img=img, link=link)
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return banner

@router.put('/{banner_id}')
def update_banner(banner_id: int, img: str = None, link: str = None, db: Session = Depends(get_db)):
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail='轮播图不存在')
    if img is not None:
        banner.img = img
    if link is not None:
        banner.link = link
    db.commit()
    db.refresh(banner)
    return banner

@router.delete('/{banner_id}')
def delete_banner(banner_id: int, db: Session = Depends(get_db)):
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail='轮播图不存在')
    db.delete(banner)
    db.commit()
    return {"success": True} 