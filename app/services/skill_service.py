from sqlmodel import Session, select
from typing import List, Optional
from app.models.skill import SkillInfo

def create_skill(session: Session, skill: SkillInfo):
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill

def get_skill(session: Session, skill_id: int) -> Optional[SkillInfo]:
    return session.get(SkillInfo, skill_id)

def get_skills(session: Session, skip: int = 0, limit: int = 100) -> List[SkillInfo]:
    statement = select(SkillInfo).offset(skip).limit(limit)
    return session.exec(statement).all()

def update_skill(session: Session, skill_id: int, skill_data: dict) -> Optional[SkillInfo]:
    skill = session.get(SkillInfo, skill_id)
    if skill:
        for key, value in skill_data.items():
            setattr(skill, key, value)
        session.add(skill)
        session.commit()
        session.refresh(skill)
    return skill

def delete_skill(session: Session, skill_id: int) -> bool:
    skill = session.get(SkillInfo, skill_id)
    if skill:
        session.delete(skill)
        session.commit()
        return True
    return False