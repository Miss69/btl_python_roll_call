from sqlalchemy.ext.declarative import declarative_base
from .employee import Employee
from .timekeeping import Timekeeping

Base = declarative_base()

__all__ = ['Base', 'Employee', 'Timekeeping'] 