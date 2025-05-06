from sqlmodel import Session, select, or_
from typing import List, Optional

from app.models.project import ProjectInfo


def search_projects(
        session: Session,
        keyword: Optional[str] = None,
        creator_id: Optional[int] = None,
        is_draft: Optional[int] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None
) -> List[ProjectInfo]:

    query = select(ProjectInfo)

    # 关键词搜索
    if keyword:
        query = query.where(
            or_(
                ProjectInfo.project_title.ilike(f"%{keyword}%"),
                ProjectInfo.project_description.ilike(f"%{keyword}%")
            )
        )

    # 创建者筛选
    if creator_id is not None:
        query = query.where(ProjectInfo.project_creator_id == creator_id)

    # 草稿状态筛选
    if is_draft is not None:
        query = query.where(ProjectInfo.is_draft == is_draft)

    # 处理分页（仅在参数提供时应用）
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    result = session.exec(query).all()

    return result