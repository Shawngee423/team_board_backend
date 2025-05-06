from fastapi import status

from app.models.skill import SkillInfo


def test_create_skill(client, sample_skill):
    response = client.post("/skills/", json={
        "skill_name": sample_skill.skill_name
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["skill_name"] == "Python"


def test_update_skill(client, session, sample_skill):
    session.add(sample_skill)
    session.commit()

    response = client.put(
        f"/skills/{sample_skill.skill_id}",
        json={"skill_name": "Python 3"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["skill_name"] == "Python 3"


def test_delete_skill(client, session, sample_skill):
    session.add(sample_skill)
    session.commit()

    response = client.delete(f"/skills/{sample_skill.skill_id}")
    assert response.status_code == status.HTTP_200_OK

    # Verify deletion
    deleted_skill = session.get(SkillInfo, sample_skill.skill_id)
    assert deleted_skill is None