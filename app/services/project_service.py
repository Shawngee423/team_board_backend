from sqlmodel import Session, select
from typing import List, Optional
from app.models.project import ProjectInfo, ProjectComment
from app.models.project_skill_link import ProjectSkillLink
from app.models.skill import SkillInfo

def create_project(session: Session, project: ProjectInfo):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

def get_project(session: Session, project_id: int) -> Optional[ProjectInfo]:
    return session.get(ProjectInfo, project_id)

def get_projects(session: Session, skip: int = 0, limit: int = 100) -> List[ProjectInfo]:
    statement = select(ProjectInfo).where(ProjectInfo.is_draft == 0).offset(skip).limit(limit)
    return session.exec(statement).all()

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
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

def get_comments(session: Session, project_id: int, skip: int = 0, limit: int = 100) -> List[ProjectComment]:
    statement = select(ProjectComment).where(ProjectComment.project_id == project_id).offset(skip).limit(limit)
    return session.exec(statement).all()

def add_skill_to_project(session: Session, project_skill: ProjectSkillLink):
    session.add(project_skill)
    session.commit()
    session.refresh(project_skill)
    return project_skill

def get_project_skills(session: Session, project_id: int) -> List[SkillInfo]:
    statement = select(SkillInfo).join(ProjectSkillLink).where(ProjectSkillLink.project_id == project_id)
    return session.exec(statement).all()