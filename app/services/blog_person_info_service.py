from typing import Optional

from sqlmodel import select, Session

from app.models.person import PersonalInfo, PersonJobExperience, PersonEducationExperience
from app.models.person_skill_link import PersonSkillLink
from app.models.skill import SkillInfo
from app.schemas.blog_person_info import PersonalInfoFullResponse, SkillInfoResponse, JobExperienceResponse, EducationExperienceResponse


def get_full_personal_info(session: Session, user_id: int) -> Optional[PersonalInfoFullResponse]:
    # 获取用户基本信息
    personal_info = session.get(PersonalInfo, user_id)
    if not personal_info:
        return None

    # 获取技能列表（带level）
    skill_query = (
        select(SkillInfo, PersonSkillLink.level)
        .join(PersonSkillLink, SkillInfo.skill_id == PersonSkillLink.skill_id)
        .where(PersonSkillLink.user_id == user_id)
    )
    skill_results = session.exec(skill_query).all()

    # 转换技能数据
    skills = [
        SkillInfoResponse(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            level=level
        )
        for skill, level in skill_results
    ]

    # 获取工作经历
    job_experiences = [
        JobExperienceResponse(
            job_title=job.job_title,
            company=job.company,
            start_time=job.start_time,
            end_time=job.end_time,
            experience_description=job.experience_description
        )
        for job in session.exec(
            select(PersonJobExperience)
            .where(PersonJobExperience.user_id == user_id)
        ).all()
    ]

    # 获取教育经历
    education_experiences = [
        EducationExperienceResponse(
            major=edu.major,
            school=edu.school,
            start_time=edu.start_time,
            end_time=edu.end_time,
            experience_description=edu.experience_description
        )
        for edu in session.exec(
            select(PersonEducationExperience)
            .where(PersonEducationExperience.user_id == user_id)
        ).all()
    ]

    return PersonalInfoFullResponse(
        user_id=personal_info.user_id,
        user_name=personal_info.user_name,
        job_title=personal_info.job_title,
        city=personal_info.city,
        country=personal_info.country,
        phone_number=personal_info.phone_number,
        website=personal_info.website,
        profile_url=personal_info.profile_url,
        skills=skills,
        job_experiences=job_experiences,
        education_experiences=education_experiences
    )
