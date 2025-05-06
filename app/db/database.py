from sqlmodel import create_engine, Session

# # 请替换为您的MySQL连接字符串
# DATABASE_URL = "mysql+pymysql://root:UJMik,78@localhost/team_board?charset=utf8mb4"
#
# engine = create_engine(DATABASE_URL)
#
# def get_session():
#     with Session(engine) as session:
#         yield session

from sqlmodel import create_engine, Session
from sqlalchemy.engine import Engine
from typing import Generator
from app.config.config import settings  # 导入全局配置

# 单例引擎实例
_engine: Engine = None

def get_engine() -> Engine:
    """获取数据库引擎（单例模式）"""
    global _engine
    if _engine is None:
        _engine = create_engine(
            str(settings.database_url),
            pool_pre_ping=True,  # 连接前检查连接是否有效
            pool_recycle=3600,    # 1小时后回收连接
            pool_size=10,         # 连接池大小
            max_overflow=20,      # 最大溢出连接数
            echo=settings.debug   # 调试模式下显示SQL
        )
    return _engine

def get_session() -> Generator[Session, None, None]:
    """获取数据库会话（依赖注入用）"""
    with Session(get_engine()) as session:
        yield session