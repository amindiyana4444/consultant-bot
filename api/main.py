from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import students, study, schedule, messages

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="مشاور کنکور API",
    description="API برای سیستم مدیریت مشاوره کنکور",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router, prefix="/students", tags=["دانش‌آموزان"])
app.include_router(study.router, prefix="/study", tags=["ساعات مطالعه"])
app.include_router(schedule.router, prefix="/schedule", tags=["برنامه مطالعه"])
app.include_router(messages.router, prefix="/messages", tags=["پیام‌ها"])

@app.get("/")
def root():
    return {"message": "به API مشاور کنکور خوش آمدید"}

@app.get("/health")
def health():
    return {"status": "ok"}
