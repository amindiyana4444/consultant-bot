from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Student schemas
class StudentBase(BaseModel):
    telegram_id: int
    name: str
    field: str
    target_year: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# StudyLog schemas
class StudyLogBase(BaseModel):
    subject: str
    hours: float

class StudyLogCreate(StudyLogBase):
    student_id: int

class StudyLog(StudyLogBase):
    id: int
    student_id: int
    date: datetime

    class Config:
        from_attributes = True

# Schedule schemas
class ScheduleBase(BaseModel):
    day_of_week: int
    subject: str
    hours: float
    description: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    student_id: int

class Schedule(ScheduleBase):
    id: int
    student_id: int

    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    student_id: int
    sender: str

class Message(MessageBase):
    id: int
    student_id: int
    sender: str
    created_at: datetime

    class Config:
        from_attributes = True
