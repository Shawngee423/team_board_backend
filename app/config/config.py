import os

from pydantic import Field, AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field("Team Board Backend Project", env="tb_backend")

    host: str = Field("localhost", env="HOST")

    port: int = Field(8000, env="PORT")

    debug: bool = Field(False, env="DEBUG")

    database_url: AnyUrl = Field("sqlite:///./test.db", env="DATABASE_URL")

    database_pool_size: int = Field(
        10,
        env="DATABASE_POOL_SIZE",
        description="数据库连接池大小"
    )

    database_max_overflow: int = Field(
        20,
        env="DATABASE_MAX_OVERFLOW",
        description="数据库最大溢出连接数"
    )

    database_pool_recycle: int = Field(
        3600,
        env="DATABASE_POOL_RECYCLE",
        description="连接回收时间（秒）"
    )
    # 日志配置
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"  # 忽略额外字段


if os.getenv("APP_ENV") == "test":
    settings = Settings(database_url="sqlite:///:memory:")
else:
    settings = Settings()
