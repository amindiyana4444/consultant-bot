from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import StudyLog
from schemas import StudyLogCreate, StudyLog as StudyLogSchema

router = APIRouter()

@router.get("/{student_id}", response_model=List[StudyLogSchema])
def get_study_logs(student_id: int, db: Session = Depends(get_db)):
    return db.query(StudyLog).filter(
        StudyLog.student_id == student_id
    ).order_by(StudyLog.date.desc()).limit(30).all()

@router.post("/", response_model=StudyLogSchema)
def create_study_log(log: StudyLogCreate, db: Session = Depends(get_db)):
    db_log = StudyLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
