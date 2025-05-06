from datetime import datetime

from sqlmodel import Session, select
from typing import List, Optional
from app.models.project import ProjectInfo, ProjectComment
from app.models.project_skill_link import ProjectSkillLink
from app.models.skill import SkillInfo
from app.schemas.skill import SkillRead


def create_project(session: Session, project: ProjectInfo):
    project.project_create_time = datetime.utcnow()
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

def get_project(session: Session, project_id: int) -> Optional[ProjectInfo]:
    return session.get(ProjectInfo, project_id)

def get_projects(session: Session, skip: Optional[int] = None, limit: Optional[int] = None) -> List[ProjectInfo]:
    query = select(ProjectInfo).where(ProjectInfo.is_draft == 0)

    if skip is not None and limit is not None:
        query = query.offset(skip).limit(limit)

    return session.exec(query).all()

def update_project(session: Session, project_id: int, project_data: dict) -> Optional[ProjectInfo]:
    project = session.get(ProjectInfo, project_id)
    if project:
        for key, value in project_data.items():
            setattr(project, key, value)
        session.add(project)
        session.commit()
        session.refresh(project)
    return project

def delete_project(session: Session, project_id: int) -> bool:
    project = session.get(ProjectInfo, project_id)
    if project:
        session.delete(project)
        session.commit()
        return True
    return False

def add_comment(session: Session, comment: ProjectComment):
    comment.comment_time = datetime.utcnow()
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

def get_comments(session: Session, project_id: int, skip: Optional[int] = None, limit: Optional[int] = None) -> List[ProjectComment]:
    query = select(ProjectComment).where(ProjectComment.project_id == project_id)

    if skip is not None and limit is not None:
        query = query.offset(skip).limit(limit)

    return session.exec(query).all()

def add_skill_to_project(session: Session, project_skill: ProjectSkillLink):
    session.add(project_skill)
    session.commit()
    session.refresh(project_skill)
    return project_skill

def get_project_skills(session: Session, project_id: int) -> List[SkillRead]:
    # statement = select(SkillInfo).join(ProjectSkillLink, SkillInfo.skill_id == ProjectSkillLink.skill_id).where(ProjectSkillLink.project_id == project_id)
    # return session.exec(statement).all()
    skills = session.exec(
        select(SkillInfo)
        .join(ProjectSkillLink, SkillInfo.skill_id == ProjectSkillLink.skill_id)
        .where(ProjectSkillLink.project_id == project_id)
    ).all()

    return [
        SkillRead(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name
        )
        for skill in skills
    ]