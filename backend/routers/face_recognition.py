from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend import models, database
from backend.schemas.timekeeping import TimekeepingResponse, TimekeepingCreate, TimekeepingCheckout
from backend.database import get_db
from backend.models import Employee, Timekeeping
from datetime import datetime

router = APIRouter()

# Dependency để lấy session DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/check-in", response_model=TimekeepingResponse)
def check_in(employee_id: int, db: Session = Depends(get_db)):
    # Kiểm tra nhân viên có tồn tại không
    employee = db.query(Employee).filter(Employee.id_employee == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Tạo bản ghi check-in mới
    timekeeping = Timekeeping(
        id_employee=employee_id,
        check_in=datetime.now(),
        date=datetime.now().date(),
        status="Present"
    )
    db.add(timekeeping)
    db.commit()
    db.refresh(timekeeping)
    
    return timekeeping

@router.post("/check-out", response_model=TimekeepingResponse)
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
    db.refresh(timekeeping)
    
    return timekeeping
