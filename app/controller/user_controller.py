from fastapi import APIRouter, Depends, HTTPException, status
from setuptools.package_index import user_agent
from sqlmodel import Session
from app.auth.dependency import get_current_user
from app.database import get_db
from app.models.user import UserRead, UserUpdate, User
from app.services.user_service import (
    get_user,
    update_user,
    get_user_skills
)

user_router = APIRouter()

@user_router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return current_user

@user_router.patch("/me", response_model=UserRead)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = update_user(db, current_user.id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@user_router.get("/me/skills")
async def get_my_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_skills(db, current_user.id)

@user_router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)  # 需要登录
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user