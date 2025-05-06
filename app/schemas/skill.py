from typing import Optional
from pydantic import BaseModel

class SkillBase(BaseModel):
    skill_name: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(SkillBase):
    pass

class SkillRead(SkillBase):
    skill_id: int