from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 确保数据目录存在
DATA_DIR = "/app/data"
os.makedirs(DATA_DIR, exist_ok=True)

# 数据库文件路径
DATABASE_FILE = os.path.join(DATA_DIR, "app.db")

# 数据库URL
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_FILE}")

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

def init_db():
    """初始化数据库，创建所有表"""
    # 延迟导入以避免循环导入
    from models import User, Category, Article, Comment, Message, Banner
    Base.metadata.create_all(bind=engine)

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 