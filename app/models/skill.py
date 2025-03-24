from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class SkillBase(SQLModel):
    name: str = Field(index=True, unique=True, min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
    category: str = Field(default="general", min_length=2, max_length=20)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Skill(SkillBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # # 与用户的关联
    # users: List[User] = Relationship(
    #     back_populates="skills",
    #     link_model=UserSkillLink
    # )
    #
    # # 与项目的关联
    # projects: List[Project] = Relationship(
    #     back_populates="required_skills",
    #     link_model=ProjectSkillLink  # 需要定义关联表
    # )


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SQLModel):
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class SkillRead(SkillBase):
    id: int
    user_count: int = 0
    project_count: int = 0


