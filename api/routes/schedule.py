from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Schedule
from schemas import ScheduleCreate, Schedule as ScheduleSchema

router = APIRouter()

@router.get("/{student_id}", response_model=List[ScheduleSchema])
def get_schedule(student_id: int, db: Session = Depends(get_db)):
    return db.query(Schedule).filter(
        Schedule.student_id == student_id
    ).all()

@router.post("/", response_model=ScheduleSchema)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = Schedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if schedule:
        db.delete(schedule)
        db.commit()
    return {"message": "برنامه حذف شد"}
