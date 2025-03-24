from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.config.config import settings

# 带连接池的 MySQL 引擎配置
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,  # 使用连接池
    pool_size=20,         # 保持的连接数
    max_overflow=10,      # 允许超过pool_size的连接数
    pool_recycle=3600,    # 连接回收时间（秒）
    pool_pre_ping=True,   # 执行前检查连接有效性
    echo=False            # 生产环境建议关闭
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    初始化数据库（创建表结构）
    注意：生产环境建议使用迁移工具（如 Alembic）
    """
    SQLModel.metadata.create_all(engine)