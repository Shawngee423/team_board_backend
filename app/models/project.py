from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class ProjectInfo(SQLModel, table=True):
    __tablename__ = 'tb_project_info'
    project_id: Optional[int] = Field(default=None, primary_key=True)
    project_title: Optional[str] = Field(default=None, max_length=255, nullable=True)
    project_creator_id: Optional[int] = Field(default=None, max_length=255, nullable=True)
    project_create_time: Optional[datetime] = Field(default=None, nullable=True)
    project_description: Optional[str] = Field(default=None, max_length=65535, nullable=True)
    project_background_img_url: Optional[str] = Field(default=None, max_length=255, nullable=True)
    is_draft: int = Field(default=0, description="true: will not shown in list; false: will be shown in list")

class ProjectComment(SQLModel, table=True):
    __tablename__ = 'tb_project_comment'
    comment_id: Optional[int] = Field(default=None, primary_key=True)
    project_id: Optional[int] = Field(default=None, nullable=True)
    user_id: Optional[int] = Field(default=None, max_length=255, nullable=True)
    comment_time: Optional[datetime] = Field(default=None, nullable=True)
    comment_message: Optional[str] = Field(default=None, max_length=65535, nullable=True)
    re_comment_id: Optional[int] = Field(default=None, max_length=255, nullable=True)