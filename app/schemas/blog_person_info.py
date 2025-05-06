from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class SkillInfoResponse(BaseModel):
    skill_id: int
    skill_name: str
    level: int

class JobExperienceResponse(BaseModel):
    job_title: str
    company: str
    start_time: datetime
    end_time: Optional[datetime] = None
    experience_description: Optional[str] = None

class EducationExperienceResponse(BaseModel):
    major: str
    school: str
    start_time: datetime
    end_time: Optional[datetime] = None
    experience_description: Optional[str] = None

class PersonalInfoFullResponse(BaseModel):
    user_id: int
    user_name: Optional[str] = None
    job_title: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None
    profile_url: Optional[str] = None
    skills: List[SkillInfoResponse] = []
    job_experiences: List[JobExperienceResponse] = []
    education_experiences: List[EducationExperienceResponse] = []

