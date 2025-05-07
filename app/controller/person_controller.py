from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.database import get_session
from app.models.person import (
    PersonalInfo,
    PersonEducationExperience,
    PersonJobExperience
)
from app.models.person_skill_link import PersonSkillLink
from app.schemas.person import (
    PersonCreate, PersonRead, PersonUpdate,
    EducationExperienceCreate, EducationExperienceRead,
    JobExperienceCreate, JobExperienceRead
)
from app.services.person_service import create_person, get_persons, get_person, update_person, delete_person, \
    add_education_experience, get_education_experiences, add_job_experience, get_job_experiences, add_skill_to_person

person_router = APIRouter()


@person_router.post("/", response_model=PersonRead)
def create_person_router(person: PersonCreate, session: Session = Depends(get_session)):
    db_person = PersonalInfo(**person.dict())
    return create_person(session, db_person)

@person_router.get("/", response_model=List[PersonRead])
def read_persons_router(skip: Optional[int] = None, limit: Optional[int] = None, session: Session = Depends(get_session)):
    return get_persons(session, skip=skip, limit=limit)

@person_router.get("/{user_id}", response_model=PersonRead)
def read_person_router(user_id: int, session: Session = Depends(get_session)):
    person = get_person(session, user_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@person_router.put("/{user_id}", response_model=PersonRead)
def update_person_router(user_id: int, person: PersonUpdate, session: Session = Depends(get_session)):
    db_person = update_person(session, user_id, person.dict(exclude_unset=True))
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@person_router.delete("/{user_id}")
def delete_person_router(user_id: int, session: Session = Depends(get_session)):
    success = delete_person(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"ok": True}

@person_router.post("/{user_id}/education", response_model=EducationExperienceRead)
def create_education_experience_router(
    user_id: int,
    education: EducationExperienceCreate,
    session: Session = Depends(get_session)
):
    db_education = PersonEducationExperience(user_id=user_id, **education.dict())
    return add_education_experience(session, db_education)

@person_router.get("/{user_id}/education", response_model=List[EducationExperienceRead])
def read_education_experiences_router(user_id: int, session: Session = Depends(get_session)):
    return get_education_experiences(session, user_id)

@person_router.post("/{user_id}/jobs", response_model=JobExperienceRead)
def create_job_experience_router(
    user_id: int,
    job: JobExperienceCreate,
    session: Session = Depends(get_session)
):
    db_job = PersonJobExperience(user_id=user_id, **job.dict())
    return add_job_experience(session, db_job)

@person_router.get("/{user_id}/jobs", response_model=List[JobExperienceRead])
def read_job_experiences_router(user_id: int, session: Session = Depends(get_session)):
    return get_job_experiences(session, user_id)

@person_router.post("/{user_id}/skills/{skill_id}")
def add_skill_to_person_router(
    user_id: int,
    skill_id: int,
    level: int,
    session: Session = Depends(get_session)
):
    return add_skill_to_person(session, user_id, skill_id, level)