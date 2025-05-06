from typing import List, Optional

from pydantic import BaseModel


class ProjectCollaborationCreate(BaseModel):
    skill_id: int
    headcount: int

class ProjectCreateRequest(BaseModel):
    project_title: str
    project_creator_id: int
    project_description: Optional[str] = None
    project_background_img_url: Optional[str] = None
    is_draft: int = 0
    collaboration_list: List[ProjectCollaborationCreate] = []