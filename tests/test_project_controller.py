from fastapi import status

from app.models.project_skill_link import ProjectSkillLink


def test_create_project(client, sample_project):
    response = client.post(
        "/projects/create",
        params={"project_creator_id": sample_project.project_creator_id},  # 作为查询参数
        json={
            "project_title": sample_project.project_title,
            "project_description": sample_project.project_description,
            "project_background_img_url": sample_project.project_background_img_url,
            "is_draft": sample_project.is_draft
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "project_id" in data
    assert data["project_title"] == "Test Project"


def test_get_project_with_skills(client, session, sample_project, sample_skill):
    # 先创建项目和技能
    session.add(sample_project)
    session.add(sample_skill)
    session.commit()

    # 创建关联
    project_skill = ProjectSkillLink(
        project_id=sample_project.project_id,
        skill_id=sample_skill.skill_id,
        headcount=2,
        applied_number=0
    )
    session.add(project_skill)
    session.commit()

    # 查询项目
    response = client.get(f"/projects/{sample_project.project_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["project_id"] == sample_project.project_id
    assert len(data["required_skills"]) == 1
    assert data["required_skills"][0]["skill_id"] == sample_skill.skill_id