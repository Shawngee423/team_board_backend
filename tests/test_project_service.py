from sqlmodel import Session

from app.models.project_skill_link import ProjectSkillLink
from app.services.project_service import (
    create_project, get_project, get_projects, update_project, delete_project,
    add_comment, get_comments,
    add_skill_to_project, get_project_skills
)
from app.services.skill_service import create_skill


def test_create_project(session: Session, sample_project):
    project = create_project(session, sample_project)
    assert project.project_id is not None
    assert project.project_create_time is not None

def test_get_project(session: Session, sample_project):
    created_project = create_project(session, sample_project)
    retrieved_project = get_project(session, created_project.project_id)
    assert retrieved_project.project_title == "Test Project"

def test_get_projects(session: Session, sample_project):
    create_project(session, sample_project)
    projects = get_projects(session)
    assert len(projects) == 1
    assert projects[0].project_title == "Test Project"

def test_update_project(session: Session, sample_project):
    created_project = create_project(session, sample_project)
    updated_project = update_project(session, created_project.project_id, {"project_title": "Updated Project"})
    assert updated_project.project_title == "Updated Project"

def test_delete_project(session: Session, sample_project):
    created_project = create_project(session, sample_project)
    result = delete_project(session, created_project.project_id)
    assert result is True
    assert get_project(session, created_project.project_id) is None

def test_add_comment(session: Session, sample_project, sample_comment):
    created_project = create_project(session, sample_project)
    sample_comment.project_id = created_project.project_id
    comment = add_comment(session, sample_comment)
    assert comment.comment_id is not None
    assert comment.comment_time is not None

def test_get_comments(session: Session, sample_project, sample_comment):
    created_project = create_project(session, sample_project)
    sample_comment.project_id = created_project.project_id
    add_comment(session, sample_comment)
    comments = get_comments(session, created_project.project_id)
    assert len(comments) == 1
    assert comments[0].comment_message == "Test comment"

def test_add_skill_to_project(session: Session, sample_project, sample_skill):
    created_project = create_project(session, sample_project)
    created_skill = create_skill(session, sample_skill)
    project_skill = ProjectSkillLink(project_id=created_project.project_id, skill_id=created_skill.skill_id, headcount=2)
    result = add_skill_to_project(session, project_skill)
    assert result.project_id == created_project.project_id

def test_get_project_skills(session: Session, sample_project, sample_skill):
    created_project = create_project(session, sample_project)
    created_skill = create_skill(session, sample_skill)
    project_skill = ProjectSkillLink(project_id=created_project.project_id, skill_id=created_skill.skill_id, headcount=2)
    add_skill_to_project(session, project_skill)
    skills = get_project_skills(session, created_project.project_id)
    assert len(skills) == 1
    assert skills[0].skill_name == "Python"