from fastapi import status


def test_search_projects(client, session, sample_project):
    # 创建测试数据
    session.add(sample_project)
    session.commit()

    # 确保URL路径正确
    response = client.get("/blog/projects/search", params={"keyword": "Test"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_create_project_with_collaborations(client, session, sample_skill):
    # 创建测试技能
    session.add(sample_skill)
    session.commit()

    response = client.post(
        "/blog/projects/create",
        json={
            "project_title": "New Project",
            "project_creator_id": 1,
            "project_description": "Project with collaborations",
            "project_background_img_url": "https://example.com/image.jpg",
            "is_draft": 0,
            "collaboration_list": [{"skill_id": sample_skill.skill_id, "headcount": 2}]
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "project_id" in response.json()


def test_get_full_personal_info(client, session, sample_person):
    # 创建测试用户
    session.add(sample_person)
    session.commit()

    response = client.get(f"/blog/user/{sample_person.user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_name"] == "John Doe"