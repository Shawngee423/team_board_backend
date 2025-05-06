from typing import Optional
from sqlmodel import Field, SQLModel

class PersonSkillLink(SQLModel, table=True):
    __tablename__ = 'tb_person_skill_link'
    user_id: Optional[int] = Field(default=None, primary_key=True)
    skill_id: Optional[int] = Field(default=None, primary_key=True)
    level: Optional[int] = Field(default=None, nullable=True)