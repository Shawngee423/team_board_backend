from typing import List

from sqlmodel import Session, select, delete
from app.models.user import User, UserSkillLink, UserCreate, UserUpdate


def get_user(db: Session, user_id: int):
    return db.get(User, user_id)


def get_user_by_keycloak_id(db: Session, keycloak_id: str):
    return db.exec(select(User).where(User.keycloak_id == keycloak_id)).first()


def create_user(db: Session, user_data: UserCreate):
    user = User(**user_data.dict(exclude={"skill_ids"}))
    db.add(user)
    db.commit()
    db.refresh(user)

    if user_data.skill_ids:
        add_skills_to_user(db, user.id, user_data.skill_ids)

    return user


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = db.get(User, user_id)
    if not user:
        return None

    update_data = user_data.dict(exclude_unset=True)
    skill_ids = update_data.pop("skill_ids", None)

    for key, value in update_data.items():
        setattr(user, key, value)

    if skill_ids is not None:
        # 清除旧技能
        db.exec(delete(UserSkillLink).where(UserSkillLink.user_id == user_id))
        add_skills_to_user(db, user_id, skill_ids)

    db.commit()
    db.refresh(user)
    return user


def add_skills_to_user(db: Session, user_id: int, skill_ids: List[int]):
    for skill_id in skill_ids:
        link = UserSkillLink(user_id=user_id, skill_id=skill_id)
        db.add(link)
    db.commit()


def get_user_skills(db: Session, user_id: int):
    user = db.get(User, user_id)
    return user.skills if user else []