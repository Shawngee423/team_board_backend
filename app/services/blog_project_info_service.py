from sqlmodel import select, Session
from typing import Optional

from app.models.person import PersonalInfo
from app.models.project import ProjectInfo, ProjectComment
from app.models.project_skill_link import ProjectSkillLink
from app.models.skill import SkillInfo
from app.schemas.blog_project_info import ProjectInfoResponse


def get_project_full_info(project_id: int, session: Session) -> Optional[ProjectInfoResponse]:
    """业务逻辑集中处理"""
    # 1. 获取基础数据
    project = session.get(ProjectInfo, project_id)
    if not project:
        return None

    # 2. 获取关联数据
    collaborations = _get_collaborations(session, project_id)
    comments = _get_comments_with_replies(session, project_id)
    creator_name = _get_creator_name(session, project.project_creator_id)

    # 3. 构建响应
    return ProjectInfoResponse(
        project_id=project.project_id,
        project_title=project.project_title,
        project_creator_name=creator_name,
        project_create_time=project.project_create_time,
        project_description=project.project_description,
        project_background_img_url=project.project_background_img_url,
        collaboration_list=collaborations,
        comment_list=comments
    )


def _get_collaborations(session: Session, project_id: int):
    """处理协作技能查询"""
    # results = session.exec(
    #     select(ProjectSkillLink, SkillInfo.skill_name)
    #     .select_from(ProjectSkillLink)
    #     .join(SkillInfo, ProjectSkillLink.skill_id == SkillInfo.skill_id)
    #     .where(ProjectSkillLink.project_id == project_id)
    # ).all()
    results = session.exec(
        select(ProjectSkillLink, SkillInfo.skill_name)
        .join(SkillInfo, ProjectSkillLink.skill_id == SkillInfo.skill_id)
        .where(ProjectSkillLink.project_id == project_id)
    ).all()

    return [
        {
            "skill_id": link.skill_id,
            "skill_name": skill_name,
            "headcount": link.headcount,
            "applied_number": link.applied_number
        }
        for link, skill_name in results
    ]


def _get_comments_with_replies(session: Session, project_id: int):
    """处理评论树构建"""
    comments = session.exec(
        select(ProjectComment)
        .where(ProjectComment.project_id == project_id)
        .order_by(ProjectComment.comment_time)
    ).all()

    return _build_comment_tree(session, comments)


def _build_comment_tree(session: Session, comments: list):
    """递归构建评论树"""
    comment_dict = {}
    root_comments = []

    for comment in comments:
        comment_data = {
            "comment_id": comment.comment_id,
            "user_id": comment.user_id,
            "user_name": _get_creator_name(session, comment.user_id),
            "comment_time": comment.comment_time,
            "comment_message": comment.comment_message,
            "re_list": []
        }
        comment_dict[comment.comment_id] = comment_data

        if comment.re_comment_id is None or comment.re_comment_id == 0:
            root_comments.append(comment_data)
        else:
            parent = comment_dict.get(comment.re_comment_id)
            if parent:
                parent["re_list"].append(comment_data)

    return root_comments


def _get_creator_name(session: Session, creator_id: int) -> str:
    """获取创建者名称"""
    creator = session.get(PersonalInfo, creator_id)
    return creator.user_name if creator else "Unknown"