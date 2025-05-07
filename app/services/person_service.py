from sqlmodel import Session, select
from typing import List, Optional
from app.models.person import (
    PersonalInfo,
    PersonEducationExperience,
    PersonJobExperience
)
from app.models.person_skill_link import PersonSkillLink
from app.models.skill import SkillInfo

def create_person(session: Session, person: PersonalInfo):
    session.add(person)
    session.commit()
    session.refresh(person)
    return person

def get_person(session: Session, user_id: int) -> Optional[PersonalInfo]:
    return session.get(PersonalInfo, user_id)

def get_persons(session: Session, skip: int = 0, limit: int = 100) -> List[PersonalInfo]:
    statement = select(PersonalInfo).offset(skip).limit(limit)
    return session.exec(statement).all()

def update_person(session: Session, user_id: int, person_data: dict) -> Optional[PersonalInfo]:
    person = session.get(PersonalInfo, user_id)
    if person:
        for key, value in person_data.items():
            setattr(person, key, value)
        session.add(person)
        session.commit()
        session.refresh(person)
    return person

def delete_person(session: Session, user_id: int) -> bool:
    person = session.get(PersonalInfo, user_id)
    if person:
        session.delete(person)
        session.commit()
        return True
    return False

def add_education_experience(session: Session, education: PersonEducationExperience):
    session.add(education)
    session.commit()
    session.refresh(education)
    return education

def get_education_experiences(session: Session, user_id: int) -> List[PersonEducationExperience]:
    statement = select(PersonEducationExperience).where(PersonEducationExperience.user_id == user_id)
    return session.exec(statement).all()

def add_job_experience(session: Session, job: PersonJobExperience):
    session.add(job)
    session.commit()
    session.refresh(job)
    return job

def get_job_experiences(session: Session, user_id: int) -> List[PersonJobExperience]:
    statement = select(PersonJobExperience).where(PersonJobExperience.user_id == user_id)
    return session.exec(statement).all()

def add_skill_to_person(session: Session, user_id: int, skill_id: int, level: int):
    # 先查询是否已存在关联
    existing_link = session.exec(
        select(PersonSkillLink)
        .where(PersonSkillLink.user_id == user_id)
        .where(PersonSkillLink.skill_id == skill_id)
    ).first()

    if existing_link:
        # 存在则更新等级
        existing_link.level = level
    else:
        # 不存在则新增
        new_link = PersonSkillLink(
            user_id=user_id,
            skill_id=skill_id,
            level=level
        )
        session.add(new_link)

    session.commit()
    now_link = session.exec(
        select(PersonSkillLink)
        .where(PersonSkillLink.user_id == user_id)
        .where(PersonSkillLink.skill_id == skill_id)
    ).first()
    return now_link

def get_person_skills(session: Session, user_id: int) -> List[SkillInfo]:
    statement = select(SkillInfo).join(PersonSkillLink, SkillInfo.skill_id == PersonSkillLink.skill_id).where(PersonSkillLink.user_id == user_id)
    return session.exec(statement).all()