from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    host: str = "testhost"
    database_url: str = "sqlite:///:memory:"
    # 其他测试专用的配置项...

test_settings = TestSettings()