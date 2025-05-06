from typing import Optional
from sqlmodel import Field, SQLModel

class ProjectSkillLink(SQLModel, table=True):
    __tablename__ = 'tb_project_collaboration'
    project_id: Optional[int] = Field(default=None, primary_key=True)
    skill_id: Optional[int] = Field(default=None, primary_key=True)
    headcount: Optional[int] = Field(default=None, nullable=True)
    applied_number: Optional[int] = Field(default=None, nullable=True)