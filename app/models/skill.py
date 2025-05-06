from typing import Optional
from sqlmodel import Field, SQLModel

class SkillInfo(SQLModel, table=True):
    __tablename__ = 'tb_skill_info'
    skill_id: Optional[int] = Field(default=None, primary_key=True)
    skill_name: Optional[str] = Field(default=None, max_length=255, nullable=True)