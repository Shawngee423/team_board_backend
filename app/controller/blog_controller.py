from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from app.db.database import get_session
from app.models.project import ProjectInfo

from app.schemas.blog_person_info import PersonalInfoFullResponse
from app.schemas.blog_project_create import ProjectCreateRequest
from app.schemas.blog_project_info import ProjectInfoResponse
from app.services.blog_person_info_service import get_full_personal_info
from app.services.blog_project_create_service import create_project_with_collaborations
from app.services.blog_project_info_service import get_project_full_info
from app.services.blog_project_search_service import search_projects

blog_router = APIRouter()

@blog_router.get("/projects/search", response_model=List[ProjectInfo])
def search_projects_router(
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    creator_id: Optional[int] = Query(None, description="创建者ID"),
    is_draft: Optional[int] = Query(None, description="草稿状态(0/1)"),
    skip: Optional[int] = Query(None, description="分页偏移量"),
    limit: Optional[int] = Query(None, description="每页数量"),
    session: Session = Depends(get_session)
):

    return search_projects(
        session=session,
        keyword=keyword,
        creator_id=creator_id,
        is_draft=is_draft,
        skip=skip,
        limit=limit
    )

@blog_router.post("/projects/create", status_code=status.HTTP_201_CREATED)
def create_project_skill_transaction(
    project_data: ProjectCreateRequest,
    session: Session = Depends(get_session)
):
    try:
        project = create_project_with_collaborations(session, project_data)
        return {
            "project_id": project.project_id,
            "message": "Project created successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}"
        )
@blog_router.get("/user/{user_id}", response_model=PersonalInfoFullResponse)
def get_full_personal_info_router(
    user_id: int,
    session: Session = Depends(get_session)
):
    full_info = get_full_personal_info(session, user_id)
    if not full_info:
        raise HTTPException(status_code=404, detail="User not found")
    return full_info


@blog_router.get("/projects/{project_id}", response_model=ProjectInfoResponse)
def get_project_full_info_router(
    project_id: int,
    session: Session = Depends(get_session)
):
    result = get_project_full_info(project_id,session)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return result




