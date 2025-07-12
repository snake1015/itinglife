from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 数据库配置优化
def get_database_url():
    """获取数据库URL，支持多种环境"""
    # 优先使用环境变量
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    
    # 本地开发环境
    if os.path.exists("data"):
        # 如果data目录存在，使用data目录
        DATA_DIR = "data"
        os.makedirs(DATA_DIR, exist_ok=True)
        DATABASE_FILE = os.path.join(DATA_DIR, "app.db")
        return f"sqlite:///{DATABASE_FILE}"
    
    # Docker环境
    if os.path.exists("/app"):
        DATA_DIR = "/app/data"
        os.makedirs(DATA_DIR, exist_ok=True)
        DATABASE_FILE = os.path.join(DATA_DIR, "app.db")
        return f"sqlite:///{DATABASE_FILE}"
    
    # 默认使用当前目录
    return "sqlite:///./app.db"

# 数据库URL
DATABASE_URL = get_database_url()

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