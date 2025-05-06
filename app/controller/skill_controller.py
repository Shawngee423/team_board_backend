from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_session
from app.models.skill import SkillInfo
from app.schemas.skill import SkillCreate, SkillRead, SkillUpdate
from app.services.skill_service import get_skills, get_skill, update_skill, create_skill, delete_skill

skill_router = APIRouter()

@skill_router.post("/", response_model=SkillRead)
def create_skill_router(skill: SkillCreate, session: Session = Depends(get_session)):
    db_skill = SkillInfo(**skill.model_dump())
    return create_skill(session, db_skill)

@skill_router.get("/", response_model=List[SkillRead])
def read_skills_router(skip: Optional[int] = None, limit: Optional[int] = None, session: Session = Depends(get_session)):
    return get_skills(session, skip=skip, limit=limit)

@skill_router.get("/{skill_id}", response_model=SkillRead)
def read_skill_router(skill_id: int, session: Session = Depends(get_session)):
    skill = get_skill(session, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@skill_router.put("/{skill_id}", response_model=SkillRead)
def update_skill_router(skill_id: int, skill: SkillUpdate, session: Session = Depends(get_session)):
    db_skill = update_skill(session, skill_id, skill.dict(exclude_unset=True))
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return db_skill

@skill_router.delete("/{skill_id}")
def delete_skill_router(skill_id: int, session: Session = Depends(get_session)):
    success = delete_skill(session, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"ok": True}