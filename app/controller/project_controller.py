from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional

from app.db.database import get_session
from app.models.project import ProjectInfo, ProjectComment
from app.models.project_skill_link import ProjectSkillLink
from app.schemas.project import (
    ProjectCreate, ProjectRead, ProjectUpdate, ProjectWithSkills,
    CommentCreate, CommentRead
)
from app.services.project_service import get_projects, get_project, get_project_skills, add_comment, get_comments, \
    add_skill_to_project, delete_project, update_project, create_project

project_router = APIRouter()


@project_router.post("/create", response_model=ProjectRead)
def create_project_router(project: ProjectCreate, project_creator_id: int = Query(1, description="创建者用户ID"), session: Session = Depends(get_session)):
    db_project = ProjectInfo(project_creator_id=project_creator_id, **project.dict())
    return create_project(session, db_project)


@project_router.get("/", response_model=List[ProjectRead])
def read_projects_router(skip: Optional[int] = None, limit: Optional[int] = None,
                         session: Session = Depends(get_session)):
    return get_projects(session, skip=skip, limit=limit)


@project_router.get("/{project_id}", response_model=ProjectWithSkills)
def read_project_router(project_id: int, session: Session = Depends(get_session)):
    project = get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    skills = get_project_skills(session, project_id)
    return ProjectWithSkills(**project.dict(), required_skills=skills)


@project_router.put("/{project_id}", response_model=ProjectRead)
def update_project_router(project_id: int, project: ProjectUpdate, session: Session = Depends(get_session)):
    db_project = update_project(session, project_id, project.dict(exclude_unset=True))
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@project_router.delete("/{project_id}")
def delete_project_router(project_id: int, session: Session = Depends(get_session)):
    success = delete_project(session, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"ok": True}


@project_router.post("/{project_id}/comments", response_model=CommentRead)
def create_comment_router(project_id: int, user_id: int, comment: CommentCreate,
                          session: Session = Depends(get_session)):
    db_comment = ProjectComment(project_id=project_id, user_id=user_id, **comment.dict())
    return add_comment(session, db_comment)


@project_router.get("/{project_id}/comments", response_model=List[CommentRead])
def read_comments_router(project_id: int, skip: Optional[int] = None, limit: Optional[int] = None,
                         session: Session = Depends(get_session)):
    return get_comments(session, project_id, skip=skip, limit=limit)


@project_router.post("/{project_id}/skills/{skill_id}")
def add_skill_to_project_router(
        project_id: int,
        skill_id: int,
        headcount: int,
        session: Session = Depends(get_session)
):
    project_skill = ProjectSkillLink(
        project_id=project_id,
        skill_id=skill_id,
        headcount=headcount,
        applied_number=0
    )
    return add_skill_to_project(session, project_skill)
