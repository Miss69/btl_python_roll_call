from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from . import Base
from sqlalchemy.orm import relationship

class Timekeeping(Base):
    __tablename__ = "timekeeping"

    id_timekeeping = Column(Integer, primary_key=True, index=True)
    id_employee = Column(Integer, ForeignKey("employee.id_employee"))
    check_in = Column(DateTime)
    check_out = Column(DateTime, nullable=True)
    status = Column(String(20))

    # Relationship với bảng employee
    employee = relationship("Employee", back_populates="timekeepings")
