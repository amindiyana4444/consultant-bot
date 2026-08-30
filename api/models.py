from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    field = Column(String)  # رشته: ریاضی، تجربی، انسانی
    target_year = Column(Integer)  # سال کنکور هدف
    created_at = Column(DateTime, default=datetime.now)

    study_logs = relationship("StudyLog", back_populates="student")
    schedules = relationship("Schedule", back_populates="student")

class StudyLog(Base):
    __tablename__ = "study_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)  # نام درس
    hours = Column(Float)  # ساعت مطالعه
    date = Column(DateTime, default=datetime.now)

    student = relationship("Student", back_populates="study_logs")

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    day_of_week = Column(Integer)  # 0=شنبه، 6=جمعه
    subject = Column(String)
    hours = Column(Float)
    description = Column(Text, nullable=True)

    student = relationship("Student", back_populates="schedules")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    sender = Column(String)  # "student" or "consultant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
