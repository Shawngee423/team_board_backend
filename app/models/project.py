from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from app.models.user import User
from app.models.skill import Skill


class ProjectBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    status: str = Field(default="open", regex="^(open|closed|in_progress|completed)$")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    creator_id: int = Field(foreign_key="user.id")

    # # 关系定义
    # creator: User = Relationship(back_populates="projects_created")
    # members: List[User] = Relationship(
    #     back_populates="projects_joined",
    #     link_model="ProjectMemberLink"
    # )
    # required_skills: List[Skill] = Relationship(
    #     back_populates="projects",
    #     link_model="ProjectSkillLink"
    # )


class ProjectCreate(ProjectBase):
    member_ids: List[int] = []
    required_skill_ids: List[int] = []


class ProjectUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    member_ids: Optional[List[int]] = None
    required_skill_ids: Optional[List[int]] = None


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    creator: User
    members: List[User] = []
    required_skills: List[Skill] = []


# 项目成员关联表
class ProjectMemberLink(SQLModel, table=True):
    project_id: Optional[int] = Field(
        default=None,
        foreign_key="project.id",
        primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        primary_key=True
    )
    join_date: datetime = Field(default_factory=datetime.utcnow)
    role: str = Field(default="member", regex="^(owner|manager|member)$")


# 项目技能关联表
class ProjectSkillLink(SQLModel, table=True):
    project_id: Optional[int] = Field(
        default=None,
        foreign_key="project.id",
        primary_key=True
    )
    skill_id: Optional[int] = Field(
        default=None,
        foreign_key="skill.id",
        primary_key=True
    )
    required_level: int = Field(default=1, ge=1, le=5)
