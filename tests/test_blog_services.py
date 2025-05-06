from datetime import datetime

from sqlmodel import Session, select

from app.models.person_skill_link import PersonSkillLink
from app.models.project import ProjectComment
from app.models.project_skill_link import ProjectSkillLink
from app.schemas.blog_project_create import ProjectCreateRequest, ProjectCollaborationCreate
from app.services.blog_person_info_service import get_full_personal_info
from app.services.blog_project_create_service import create_project_with_collaborations
from app.services.blog_project_info_service import get_project_full_info
from app.services.blog_project_search_service import search_projects
from app.services.person_service import create_person, add_education_experience, add_job_experience, add_skill_to_person
from app.services.project_service import create_project
from app.services.skill_service import create_skill


def test_get_full_personal_info(session: Session, sample_person, sample_education, sample_job, sample_skill):
    # 创建测试数据
    person = create_person(session, sample_person)

    # 添加教育经历
    sample_education.user_id = person.user_id
    add_education_experience(session, sample_education)

    # 添加工作经历
    sample_job.user_id = person.user_id
    add_job_experience(session, sample_job)

    # 添加技能
    skill = create_skill(session, sample_skill)
    person_skill = PersonSkillLink(user_id=person.user_id, skill_id=skill.skill_id, level=3)
    add_skill_to_person(session, person_skill)

    # 测试获取完整个人信息
    result = get_full_personal_info(session, person.user_id)
    assert result is not None
    assert result.user_name == "John Doe"
    assert len(result.skills) == 1
    assert len(result.job_experiences) == 1
    assert len(result.education_experiences) == 1


def test_create_project_with_collaborations(session: Session, sample_person, sample_skill):
    # 创建测试数据
    person = create_person(session, sample_person)
    skill = create_skill(session, sample_skill)

    project_data = ProjectCreateRequest(
        project_title="New Project",
        project_creator_id=person.user_id,
        project_description="Project with collaborations",
        project_background_img_url="https://example.com/image.jpg",
        is_draft=0,
        collaboration_list=[
            ProjectCollaborationCreate(skill_id=skill.skill_id, headcount=2)
        ]
    )

    # 测试创建项目
    project = create_project_with_collaborations(session, project_data)
    assert project is not None
    assert project.project_id is not None

    # 验证协作关系是否创建
    collaborations = session.exec(
        select(ProjectSkillLink)
        .where(ProjectSkillLink.project_id == project.project_id)
    ).all()
    assert len(collaborations) == 1


def test_get_project_full_info(session: Session, sample_person, sample_project, sample_comment, sample_skill):
    # 创建用户
    person = create_person(session, sample_person)
    session.commit()

    # 创建项目并设置创建者
    project = create_project(session, sample_project)
    project.project_creator_id = person.user_id
    session.add(project)
    session.commit()

    # 添加技能
    skill = create_skill(session, sample_skill)
    session.commit()

    # 添加项目技能关联
    project_skill = ProjectSkillLink(
        project_id=project.project_id,
        skill_id=skill.skill_id,
        headcount=2,
        applied_number=0
    )
    session.add(project_skill)
    session.commit()

    # 添加评论
    comment = ProjectComment(
        project_id=project.project_id,
        user_id=person.user_id,
        comment_message="Test comment",
        comment_time=datetime.utcnow(),
        re_comment_id=None
    )
    session.add(comment)
    session.commit()

    # 获取完整项目信息
    result = get_project_full_info(project.project_id, session)

    # 验证
    assert result is not None
    assert result.project_title == "Test Project"
    assert result.project_creator_name == person.user_name

    # 验证协作技能 - 使用对象属性访问方式
    assert len(result.collaboration_list) == 1
    collaboration = result.collaboration_list[0]
    assert collaboration.skill_name == "Python"
    assert collaboration.headcount == 2
    assert collaboration.applied_number == 0

    # 验证评论 - 同样使用对象属性访问
    assert len(result.comment_list) == 1
    comment = result.comment_list[0]
    assert comment.comment_message == "Test comment"
    assert comment.user_name == person.user_name

def test_search_projects(session: Session, sample_project):
    # 创建测试项目
    create_project(session, sample_project)

    # 测试关键词搜索
    results = search_projects(session, keyword="Test")
    assert len(results) == 1

    # 测试创建者筛选
    results = search_projects(session, creator_id=1)
    assert len(results) == 1

    # 测试草稿状态筛选
    results = search_projects(session, is_draft=0)
    assert len(results) == 1

    # 测试分页
    results = search_projects(session, skip=0, limit=1)
    assert len(results) == 1