from sqlalchemy import Column, Integer, String, Date
from frontend.utils.database import Base
from sqlalchemy.orm import relationship

class Employee(Base):
    __tablename__ = "employee"

    id_employee = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    date_of_birth = Column(Date)
    phonenumber = Column(String(20))
    email = Column(String(100))
    address = Column(String(200))
    department = Column(String(100))
    gender = Column(String(10))
    position = Column(String(100))
    status = Column(String(20))
    cccd = Column(String(20))

    # Relationship với bảng timekeeping
    timekeepings = relationship("Timekeeping", back_populates="employee") 