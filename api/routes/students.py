from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Student, StudyLog
from schemas import StudentCreate, Student as StudentSchema
from sqlalchemy import func

router = APIRouter()

@router.get("/", response_model=List[StudentSchema])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.post("/", response_model=StudentSchema)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/{student_id}", response_model=StudentSchema)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="دانش‌آموز یافت نشد")
    return student

@router.get("/{student_id}/stats")
def get_student_stats(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="دانش‌آموز یافت نشد")

    total_hours = db.query(func.sum(StudyLog.hours)).filter(
        StudyLog.student_id == student_id
    ).scalar() or 0

    today = func.date(StudyLog.date)
    today_hours = db.query(func.sum(StudyLog.hours)).filter(
        StudyLog.student_id == student_id,
        today == func.current_date()
    ).scalar() or 0

    return {
        "student": student,
        "total_hours": total_hours,
        "today_hours": today_hours
    }
