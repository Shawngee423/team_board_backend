from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_db
from app.models.skill import SkillCreate, SkillRead, SkillUpdate
from app.services.skill_service import (
    get_skill,
    get_skills,
    create_skill,
    update_skill,
    delete_skill,
    get_skill_stats
)
from app.auth.dependency import get_current_admin_user

skill_router = APIRouter()

@skill_router.get("/", response_model=List[SkillRead])
def read_skills(
    category: Optional[str] = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_skills(db, skip, limit, category, active_only)

@skill_router.get("/{skill_id}", response_model=SkillRead)
def read_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = get_skill(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@skill_router.post("/", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_new_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin_user)
):
    skill = create_skill(db, skill_data)
    if not skill:
        raise HTTPException(status_code=400, detail="Skill name already exists")
    return skill

@skill_router.patch("/{skill_id}", response_model=SkillRead)
def update_existing_skill(
    skill_id: int,
    skill_data: SkillUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin_user)
):
    skill = update_skill(db, skill_id, skill_data)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@skill_router.delete("/{skill_id}")
def remove_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin_user)
):
    success = delete_skill(db, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"message": "Skill deleted"}

@skill_router.get("/{skill_id}/stats")
def get_skill_statistics(skill_id: int, db: Session = Depends(get_db)):
    stats = get_skill_stats(db, skill_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Skill not found")
    return stats