from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_db
from app.models.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.models.user import User
from app.services.project_service import (
    create_project,
    get_project,
    get_projects,
    update_project,
    delete_project,
    get_user_projects
)
from app.auth.dependency import get_current_user, verify_project_owner

project_router = APIRouter()

@project_router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_new_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_project(db, project_data, current_user.id)

@project_router.get("/", response_model=List[ProjectRead])
def read_projects(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_projects(db, skip, limit, status)

@project_router.get("/me", response_model=List[ProjectRead])
def read_my_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_projects(db, current_user.id)

@project_router.get("/{project_id}", response_model=ProjectRead)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@project_router.patch("/{project_id}", response_model=ProjectRead)
def update_existing_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    _=Depends(verify_project_owner)  # 权限验证
):
    updated_project = update_project(db, project_id, project_data)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@project_router.delete("/{project_id}")
def remove_project(
    project_id: int,
    db: Session = Depends(get_db),
    _=Depends(verify_project_owner)  # 权限验证
):
    if not delete_project(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted"}