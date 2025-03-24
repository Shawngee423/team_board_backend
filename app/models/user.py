from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import SQLModel, Field

from app.models.skill import Skill


class UserBase(SQLModel):
    keycloak_id: str = Field(index=True, unique=True, description="Keycloak 用户唯一标识")
    username: str = Field(index=True, min_length=3, max_length=50)
    email: str = Field(index=True, regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    full_name: Optional[str] = Field(default=None, max_length=100)
    bio: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # # 用户技能关系
    # skills: List[Skill] = Relationship(
    #     back_populates="users",
    #     link_model=UserSkillLink  # 需要定义关联表
    # )
    #
    # # 用户创建的项目
    # projects_created: List[Project] = Relationship(back_populates="creator")
    #
    # # 用户参与的项目
    # projects_joined: List[Project] = Relationship(
    #     back_populates="members",
    #     link_model=ProjectMemberLink  # 需要定义关联表
    # )


class UserCreate(UserBase):
    skill_ids: List[int] = []


class UserUpdate(SQLModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    skill_ids: Optional[List[int]] = None


class UserRead(UserBase):
    id: int
    skills: List[Skill] = []
    projects_created_count: int = 0
    projects_joined_count: int = 0


# 用户技能关联表
class UserSkillLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        primary_key=True
    )
    skill_id: Optional[int] = Field(
        default=None,
        foreign_key="skill.id",
        primary_key=True
    )
    proficiency_level: int = Field(default=1, ge=1, le=5)