from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PersonBase(BaseModel):
    user_name: Optional[str] = None
    job_title: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None
    profile_url: Optional[str] = None

class PersonCreate(PersonBase):
    pass

class PersonUpdate(PersonBase):
    pass

class PersonRead(PersonBase):
    user_id: int

class EducationExperienceBase(BaseModel):
    school: Optional[str] = None
    major: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    experience_description: Optional[str] = None

class EducationExperienceCreate(EducationExperienceBase):
    pass

class EducationExperienceRead(EducationExperienceBase):
    user_id: int
    school: str
    major: str

class JobExperienceBase(BaseModel):
    company: Optional[str] = None
    job_title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    experience_description: Optional[str] = None
    full_time: Optional[int] = None

class JobExperienceCreate(JobExperienceBase):
    pass

class JobExperienceRead(JobExperienceBase):
    user_id: int
    company: str
    job_title: str