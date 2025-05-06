from sqlmodel import Session, select

from sqlmodel import Session, select

from app.models.person import PersonEducationExperience, PersonJobExperience
from app.models.person_skill_link import PersonSkillLink
from app.services.person_service import (
    create_person, get_person, get_persons, update_person, delete_person,
    add_education_experience, get_education_experiences,
    add_job_experience, get_job_experiences,
    add_skill_to_person, get_person_skills
)
from app.services.skill_service import create_skill


def test_create_person(session: Session, sample_person):
    created_person = create_person(session, sample_person)
    assert created_person.user_id is not None
    assert created_person.user_name == "John Doe"

def test_get_person(session: Session, sample_person):
    created_person = create_person(session, sample_person)
    retrieved_person = get_person(session, created_person.user_id)
    assert retrieved_person.user_name == "John Doe"

def test_get_persons(session: Session, sample_person):
    create_person(session, sample_person)
    persons = get_persons(session)
    assert len(persons) == 1
    assert persons[0].user_name == "John Doe"

def test_update_person(session: Session, sample_person):
    created_person = create_person(session, sample_person)
    updated_person = update_person(session, created_person.user_id, {"user_name": "Jane Doe"})
    assert updated_person.user_name == "Jane Doe"

def test_delete_person(session: Session, sample_person):
    created_person = create_person(session, sample_person)
    result = delete_person(session, created_person.user_id)
    assert result is True
    assert get_person(session, created_person.user_id) is None


def test_add_education_experience(session: Session, sample_person, sample_education):
    # 先创建用户
    person = create_person(session, sample_person)

    # 设置教育经历的用户ID
    sample_education.user_id = person.user_id

    # 添加教育经历
    education = add_education_experience(session, sample_education)

    # 验证
    assert education.user_id is not None
    assert education.user_id == person.user_id

    # 从数据库查询验证
    stored_edu = session.exec(
        select(PersonEducationExperience)
        .where(PersonEducationExperience.user_id == education.user_id)
    ).first()
    assert stored_edu is not None
    assert stored_edu.major == "Computer Science"

def test_get_education_experiences(session: Session, sample_person, sample_education):
    created_person = create_person(session, sample_person)
    sample_education.user_id = created_person.user_id
    add_education_experience(session, sample_education)
    educations = get_education_experiences(session, created_person.user_id)
    assert len(educations) == 1
    assert educations[0].major == "Computer Science"


def test_add_job_experience(session: Session, sample_person, sample_job):
    # 先创建用户
    person = create_person(session, sample_person)

    # 设置工作经历的用户ID
    sample_job.user_id = person.user_id

    # 添加工作经历
    job = add_job_experience(session, sample_job)

    # 验证
    assert job.user_id is not None
    assert job.user_id == person.user_id

    # 从数据库查询验证
    stored_job = session.exec(
        select(PersonJobExperience)
        .where(PersonJobExperience.user_id == job.user_id)
    ).first()
    assert stored_job is not None
    assert stored_job.company == "Tech Corp"

def test_get_job_experiences(session: Session, sample_person, sample_job):
    created_person = create_person(session, sample_person)
    sample_job.user_id = created_person.user_id
    add_job_experience(session, sample_job)
    jobs = get_job_experiences(session, created_person.user_id)
    assert len(jobs) == 1
    assert jobs[0].company == "Tech Corp"

def test_add_skill_to_person(session: Session, sample_person, sample_skill):
    created_person = create_person(session, sample_person)
    created_skill = create_skill(session, sample_skill)
    person_skill = PersonSkillLink(user_id=created_person.user_id, skill_id=created_skill.skill_id, level=3)
    result = add_skill_to_person(session, person_skill)
    assert result.user_id == created_person.user_id

def test_get_person_skills(session: Session, sample_person, sample_skill):
    created_person = create_person(session, sample_person)
    created_skill = create_skill(session, sample_skill)
    person_skill = PersonSkillLink(user_id=created_person.user_id, skill_id=created_skill.skill_id, level=3)
    add_skill_to_person(session, person_skill)
    skills = get_person_skills(session, created_person.user_id)
    assert len(skills) == 1
    assert skills[0].skill_name == "Python"