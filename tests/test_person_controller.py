from fastapi import status
from sqlmodel import select

from app.models.person_skill_link import PersonSkillLink


def test_create_person(client, sample_person):
    response = client.post("/persons/", json={
        "user_name": sample_person.user_name,
        "job_title": sample_person.job_title,
        "city": sample_person.city
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_name"] == "John Doe"


def test_get_person(client, session, sample_person):
    session.add(sample_person)
    session.commit()

    response = client.get(f"/persons/{sample_person.user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_name"] == "John Doe"


def test_add_education_experience(client, session, sample_person, sample_education):
    session.add(sample_person)
    session.commit()

    response = client.post(
        f"/persons/{sample_person.user_id}/education",
        json={
            "major": sample_education.major,
            "school": sample_education.school,
            "start_time": sample_education.start_time.isoformat(),
            "end_time": sample_education.end_time.isoformat()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["major"] == "Computer Science"


def test_add_skill_to_person(client, session, sample_person, sample_skill):
    session.add_all([sample_person, sample_skill])
    session.commit()

    response = client.post(
        f"/persons/{sample_person.user_id}/skills/{sample_skill.skill_id}",
        params={"level": 3}
    )
    assert response.status_code == status.HTTP_200_OK

    # Verify link was created
    link = session.exec(
        select(PersonSkillLink)
        .where(PersonSkillLink.user_id == sample_person.user_id)
        .where(PersonSkillLink.skill_id == sample_skill.skill_id)
    ).first()
    assert link is not None