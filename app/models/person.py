from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class PersonalInfo(SQLModel, table=True):
    __tablename__ = 'tb_personal_info'
    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: Optional[str] = Field(default=None, max_length=255, nullable=True)
    job_title: Optional[str] = Field(default=None, max_length=255, nullable=True)
    city: Optional[str] = Field(default=None, max_length=255, nullable=True)
    country: Optional[str] = Field(default=None, max_length=255, nullable=True)
    phone_number: Optional[str] = Field(default=None, max_length=255, nullable=True)
    website: Optional[str] = Field(default=None, max_length=255, nullable=True)
    profile_url: Optional[str] = Field(default=None, max_length=255, nullable=True)

class PersonEducationExperience(SQLModel, table=True):
    __tablename__ = 'tb_person_education_experience'
    user_id: Optional[int] = Field(default=None, primary_key=True)
    school: Optional[str] = Field(default=None, max_length=255, primary_key=True, description="school")
    start_time: Optional[datetime] = Field(default=None, nullable=True)
    end_time: Optional[datetime] = Field(default=None, nullable=True)
    experience_description: Optional[str] = Field(default=None, max_length=65535, nullable=True)
    major: Optional[str] = Field(default=None, max_length=255, primary_key=True, description="major")

class PersonJobExperience(SQLModel, table=True):
    __tablename__ = 'tb_person_job_experience'
    user_id: Optional[int] = Field(default=None, primary_key=True)
    company: Optional[str] = Field(default=None, max_length=255, primary_key=True, description="company")
    start_time: Optional[datetime] = Field(default=None, nullable=True)
    end_time: Optional[datetime] = Field(default=None, nullable=True)
    experience_description: Optional[str] = Field(default=None, max_length=65535, nullable=True)
    job_title: Optional[str] = Field(default=None, max_length=255, primary_key=True, description="job")
    full_time: Optional[int] = Field(default=None, nullable=True, description="true:full time; false:half time")