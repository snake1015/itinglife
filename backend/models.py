from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    email = Column(String(128), unique=True)
    password = Column(String(128))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    comments = relationship('Comment', back_populates='user')
    messages = relationship('Message', back_populates='user')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), unique=True, index=True)
    articles = relationship('Article', back_populates='category')

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128))
    content = Column(Text)
    summary = Column(String(256))
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='articles')
    comments = relationship('Comment', back_populates='article')
    tags = Column(String(128))  # 逗号分隔
    author_id = Column(Integer, ForeignKey('users.id'))

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    article_id = Column(Integer, ForeignKey('articles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    article = relationship('Article', back_populates='comments')
    user = relationship('User', back_populates='comments')

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='messages')

class Banner(Base):
    __tablename__ = 'banners'
    id = Column(Integer, primary_key=True, index=True)
    img = Column(String(256))
    link = Column(String(256))
    created_at = Column(DateTime, default=datetime.utcnow) 