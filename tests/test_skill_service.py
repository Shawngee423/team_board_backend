from sqlmodel import Session

from app.services.skill_service import (
    create_skill, get_skill, get_skills, update_skill, delete_skill
)


def test_create_skill(session: Session, sample_skill):
    skill = create_skill(session, sample_skill)
    assert skill.skill_id is not None
    assert skill.skill_name == "Python"

def test_get_skill(session: Session, sample_skill):
    created_skill = create_skill(session, sample_skill)
    retrieved_skill = get_skill(session, created_skill.skill_id)
    assert retrieved_skill.skill_name == "Python"

def test_get_skills(session: Session, sample_skill):
    create_skill(session, sample_skill)
    skills = get_skills(session)
    assert len(skills) == 1
    assert skills[0].skill_name == "Python"

def test_update_skill(session: Session, sample_skill):
    created_skill = create_skill(session, sample_skill)
    updated_skill = update_skill(session, created_skill.skill_id, {"skill_name": "JavaScript"})
    assert updated_skill.skill_name == "JavaScript"

def test_delete_skill(session: Session, sample_skill):
    created_skill = create_skill(session, sample_skill)
    result = delete_skill(session, created_skill.skill_id)
    assert result is True
    assert get_skill(session, created_skill.skill_id) is None