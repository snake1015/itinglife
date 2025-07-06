from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# User schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True

# Category schemas
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# Article schemas
class ArticleBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    is_featured: bool = False
    tags: Optional[str] = None

class ArticleCreate(ArticleBase):
    category_id: int

class ArticleOut(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category_id: int
    author_id: Optional[int] = None

    class Config:
        orm_mode = True

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    article_id: int

class CommentOut(CommentBase):
    id: int
    created_at: datetime
    article_id: int
    user_id: int

    class Config:
        orm_mode = True

# Message schemas
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True

# Banner schemas
class BannerBase(BaseModel):
    img: str
    link: str

class BannerCreate(BannerBase):
    pass

class BannerOut(BannerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 