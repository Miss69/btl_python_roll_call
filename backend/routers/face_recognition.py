from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import os
from typing import List
from sqlalchemy.orm import Session
from backend import models, database
from backend.schemas.timekeeping import TimekeepingResponse, TimekeepingCreate, TimekeepingCheckout
from backend.services.face_service import FaceService
from backend.database import get_db
from backend.models import Employee, Timekeeping
from datetime import datetime

router = APIRouter()
face_service = FaceService()

# Dependency để lấy session DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
async def register_face(
    employee_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Kiểm tra nhân viên tồn tại
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Đọc dữ liệu ảnh
    image_data = await image.read()
    
    # Đăng ký khuôn mặt
    success = await face_service.register_face(employee_id, image_data)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to register face")
    
    return {"message": "Face registered successfully"}

@router.post("/check-in")
def check_in(employee_id: int, db: Session = Depends(get_db)):
    # Kiểm tra nhân viên có tồn tại không
    employee = db.query(Employee).filter(Employee.id_employee == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Tạo bản ghi check-in mới
    timekeeping = Timekeeping(
        id_employee=employee_id,
        check_in=datetime.now(),
        status="Present"
    )
    db.add(timekeeping)
    db.commit()
    db.refresh(timekeeping)
    
    return {"message": "Check-in successful", "timekeeping_id": timekeeping.id_timekeeping}

@router.post("/check-out")
def check_out(employee_id: int, db: Session = Depends(get_db)):
    # Kiểm tra nhân viên có tồn tại không
    employee = db.query(Employee).filter(Employee.id_employee == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Tìm bản ghi check-in gần nhất chưa có check-out
    timekeeping = db.query(Timekeeping).filter(
        Timekeeping.id_employee == employee_id,
        Timekeeping.check_out == None
    ).order_by(Timekeeping.check_in.desc()).first()
    
    if not timekeeping:
        raise HTTPException(status_code=400, detail="No active check-in found")
    
    # Cập nhật thời gian check-out
    timekeeping.check_out = datetime.now()
    db.commit()
    
    return {"message": "Check-out successful"}
