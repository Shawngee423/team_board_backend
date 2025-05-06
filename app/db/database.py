from sqlmodel import create_engine, Session

# 请替换为您的MySQL连接字符串
DATABASE_URL = "mysql+pymysql://root:UJMik,78@localhost/team_board?charset=utf8mb4"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session