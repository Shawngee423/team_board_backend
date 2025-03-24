from typing import Optional

from sqlmodel import Session, select, delete
from app.models.project import Project, ProjectMemberLink, ProjectSkillLink, ProjectCreate, ProjectUpdate


def create_project(db: Session, project_data: ProjectCreate, creator_id: int):
    # 创建基础项目
    project = Project(**project_data.dict(exclude={"member_ids", "required_skill_ids"}))
    project.creator_id = creator_id

    db.add(project)
    db.commit()
    db.refresh(project)

    # 添加项目成员（包括创建者）
    member_ids = set(project_data.member_ids)
    member_ids.add(creator_id)  # 自动添加创建者为成员

    # 处理成员关联
    for user_id in member_ids:
        role = "owner" if user_id == creator_id else "member"
        db.add(ProjectMemberLink(
            project_id=project.id,
            user_id=user_id,
            role=role
        ))

    # 处理技能关联
    for skill_id in project_data.required_skill_ids:
        db.add(ProjectSkillLink(
            project_id=project.id,
            skill_id=skill_id
        ))

    db.commit()
    return project


def get_project(db: Session, project_id: int):
    return db.get(Project, project_id)


def get_projects(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        creator_id: Optional[int] = None
):
    query = select(Project)

    if status:
        query = query.where(Project.status == status)

    if creator_id:
        query = query.where(Project.creator_id == creator_id)

    return db.exec(query.offset(skip).limit(limit)).all()


def update_project(db: Session, project_id: int, project_data: ProjectUpdate):
    project = db.get(Project, project_id)
    if not project:
        return None

    # 更新基础字段
    update_data = project_data.dict(exclude_unset=True, exclude={"member_ids", "required_skill_ids"})
    for key, value in update_data.items():
        setattr(project, key, value)

    # 更新成员
    if project_data.member_ids is not None:
        # 删除旧成员（保留创建者）
        db.exec(delete(ProjectMemberLink).where(
            (ProjectMemberLink.project_id == project_id) &
            (ProjectMemberLink.role != "owner")
        ))

        # 添加新成员
        for user_id in project_data.member_ids:
            if user_id != project.creator_id:  # 防止覆盖创建者
                db.add(ProjectMemberLink(
                    project_id=project_id,
                    user_id=user_id,
                    role="member"
                ))

    # 更新技能要求
    if project_data.required_skill_ids is not None:
        db.exec(delete(ProjectSkillLink).where(
            ProjectSkillLink.project_id == project_id
        ))

        for skill_id in project_data.required_skill_ids:
            db.add(ProjectSkillLink(
                project_id=project_id,
                skill_id=skill_id
            ))

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int):
    project = db.get(Project, project_id)
    if not project:
        return False

    # 删除关联关系
    db.exec(delete(ProjectMemberLink).where(
        ProjectMemberLink.project_id == project_id
    ))
    db.exec(delete(ProjectSkillLink).where(
        ProjectSkillLink.project_id == project_id
    ))

    db.delete(project)
    db.commit()
    return True


def get_project_members(db: Session, project_id: int):
    project = db.get(Project, project_id)
    return project.members if project else []


def get_user_projects(db: Session, user_id: int):
    return db.exec(select(Project).join(ProjectMemberLink).where(
        ProjectMemberLink.user_id == user_id
    )).all()