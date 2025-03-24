from typing import Optional

from sqlmodel import Session, select
from app.models.skill import Skill, SkillCreate, SkillUpdate


def get_skill(db: Session, skill_id: int):
    return db.get(Skill, skill_id)


def get_skill_by_name(db: Session, name: str):
    return db.exec(select(Skill).where(Skill.name == name)).first()


def get_skills(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        active_only: bool = True
):
    query = select(Skill)

    if category:
        query = query.where(Skill.category == category)

    if active_only:
        query = query.where(Skill.is_active == True)

    return db.exec(query.offset(skip).limit(limit)).all()


def create_skill(db: Session, skill_data: SkillCreate):
    # 检查名称是否已存在
    if get_skill_by_name(db, skill_data.name):
        return None

    skill = Skill(**skill_data.dict())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def update_skill(db: Session, skill_id: int, skill_data: SkillUpdate):
    skill = db.get(Skill, skill_id)
    if not skill:
        return None

    update_data = skill_data.dict(exclude_unset=True)

    # 防止更新名称
    if "name" in update_data:
        del update_data["name"]

    for key, value in update_data.items():
        setattr(skill, key, value)

    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, skill_id: int):
    skill = db.get(Skill, skill_id)
    if not skill:
        return False

    db.delete(skill)
    db.commit()
    return True


def get_skill_stats(db: Session, skill_id: int):
    skill = db.get(Skill, skill_id)
    if not skill:
        return None

    return {
        "user_count": len(skill.users),
        "project_count": len(skill.projects)
    }