from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "UJMik,78"
    MYSQL_DB: str = "keycloak_teamboard"
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "TeamBoard"
    KEYCLOAK_CLIENT_ID: str = "TeamBoard_Backend"
    KEYCLOAK_CLIENT_SECRET: str = "qh0pEjNBHykG7xHDMz2mxXWq9zpNBU5E"

    class Config:
        env_file = ".env"

    # def __init__(self, **values):
    #     super().__init__(**values)
    #     # 动态生成数据库 URL
    #     self.DATABASE_URL = f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}?charset=utf8mb4"

settings = Settings()