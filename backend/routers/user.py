from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserOut, UserCreate, UserLogin
from typing import List

router = APIRouter()

@router.get('', response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post('/register')
def register(user_data: UserCreate = Body(...), db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == user_data.username) | (User.email == user_data.email)).first():
        raise HTTPException(status_code=400, detail='用户已存在')
    user = User(username=user_data.username, email=user_data.email, password=user_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email}

@router.post('/login')
def login(user_data: UserLogin = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username, User.password == user_data.password).first()
    if not user:
        raise HTTPException(status_code=401, detail='用户名或密码错误')
    return {"id": user.id, "username": user.username, "email": user.email}

@router.get('/{user_id}', response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='用户不存在')
    return user 