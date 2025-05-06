from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ProjectCollaborationResponse(BaseModel):
    skill_id: int
    skill_name: str
    headcount: int
    applied_number: int

class ProjectCommentResponse(BaseModel):
    comment_id: int
    user_id: int
    user_name: str
    comment_time: datetime
    comment_message: str
    re_list: List["ProjectCommentResponse"] = []


class ProjectInfoResponse(BaseModel):
    project_id: int
    project_title: str
    project_creator_name: str
    project_create_time: datetime
    project_description: Optional[str] = None
    project_background_img_url: Optional[str] = None
    collaboration_list: List[ProjectCollaborationResponse] = []
    comment_list: List[ProjectCommentResponse] = []