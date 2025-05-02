from fastapi import FastAPI
from backend.routers import face_recognition
from backend import models, database

# Tạo bảng nếu chưa có
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Face Recognition Attendance System",
    description="API for face recognition and attendance tracking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Gắn router
app.include_router(face_recognition.router, prefix="/face_recognition", tags=["Face Recognition"])
