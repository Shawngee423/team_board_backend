from sqlmodel import Session
from datetime import datetime

from app.models.project import ProjectInfo
from app.models.project_skill_link import ProjectSkillLink
from app.schemas.blog_project_create import ProjectCreateRequest


def create_project_with_collaborations(
        session: Session,
        project_data: ProjectCreateRequest
) -> ProjectInfo:
    """
    创建项目及协作关系（事务处理）
    """
    try:
        # 开始事务（SQLModel的Session默认在事务中）
        project = ProjectInfo(
            project_title=project_data.project_title,
            project_creator_id=project_data.project_creator_id,
            project_create_time=datetime.utcnow(),
            project_description=project_data.project_description,
            project_background_img_url=project_data.project_background_img_url,
            is_draft=project_data.is_draft
        )
        session.add(project)
        session.flush()  # 获取project_id但不提交事务

        # 添加协作关系
        for collaboration in project_data.collaboration_list:
            session.add(ProjectSkillLink(
                project_id=project.project_id,
                skill_id=collaboration.skill_id,
                headcount=collaboration.headcount,
                applied_number=0  # 初始化为0
            ))

        session.commit()  # 提交事务（所有操作要么全部成功，要么全部失败）
        return project

    except Exception as e:
        session.rollback()  # 发生异常时回滚
        raise  # 重新抛出异常