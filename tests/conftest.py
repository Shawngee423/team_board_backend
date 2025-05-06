import os
import sys
from pathlib import Path

from sqlalchemy import StaticPool

from app.db.database import get_session
from app.models.person import PersonalInfo, PersonEducationExperience, PersonJobExperience
from app.models.project import ProjectInfo, ProjectComment
from app.models.skill import SkillInfo

# 设置测试环境变量
os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["HOST"] = "localhost"
os.environ["PORT"] = "0"  # 测试时通常不需要实际端口

# 确保正确导入路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 现在可以安全导入app
from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.app import app

# 覆盖任何其他需要修改的配置
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:",
                           connect_args={"check_same_thread": False},  # 添加此参数
                           poolclass=StaticPool
                           )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def sample_person():
    return PersonalInfo(
        user_name="John Doe",
        job_title="Software Engineer",
        city="New York",
        country="USA",
        phone_number="1234567890",
        website="https://example.com",
        profile_url="https://example.com/profile"
    )

@pytest.fixture
def sample_education():
    return PersonEducationExperience(
        user_id=1,
        major="Computer Science",
        school="MIT",
        start_time=datetime(2015, 9, 1),
        end_time=datetime(2019, 6, 1),
        experience_description="Bachelor's degree"
    )

@pytest.fixture
def sample_job():
    return PersonJobExperience(
        user_id=1,
        job_title="Software Developer",
        company="Tech Corp",
        start_time=datetime(2019, 7, 1),
        end_time=datetime(2021, 12, 31),
        experience_description="Developed web applications"
    )

@pytest.fixture
def sample_skill():
    return SkillInfo(skill_name="Python")

@pytest.fixture
def sample_project():
    return ProjectInfo(
        project_title="Test Project",
        project_creator_id=1,
        project_description="A test project",
        project_background_img_url="https://example.com/image.jpg",
        is_draft=0
    )

@pytest.fixture
def sample_comment():
    return ProjectComment(
        project_id=1,
        user_id=1,
        comment_message="Test comment",
        re_comment_id=None
    )

