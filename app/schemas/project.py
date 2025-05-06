from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.skill import SkillRead


class ProjectBase(BaseModel):
    project_title: Optional[str] = None
    project_description: Optional[str] = None
    project_background_img_url: Optional[str] = None
    is_draft: int = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    project_id: int
    project_creator_id: Optional[int] = None
    project_create_time: Optional[datetime] = None

class ProjectWithSkills(ProjectRead):
    required_skills: list[SkillRead] = []

class CommentBase(BaseModel):
    comment_message: Optional[str] = None
    re_comment_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    comment_id: int
    project_id: Optional[int] = None
    user_id: Optional[int] = None
    comment_time: Optional[datetime] = None