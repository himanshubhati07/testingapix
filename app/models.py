# SQLAlchemy models for salary management system
import os
from datetime import datetime, date
from enum import Enum
from dotenv import load_dotenv
from sqlalchemy import String, DateTime, Date, Integer, Boolean, ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)

from app.database import Base


class EmployeeStatus(str, Enum):
    active = "Active"
    inactive = "Inactive"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        UniqueConstraint("email", name="uq_employee_email"),
        UniqueConstraint("phone_number", name="uq_employee_phone"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(30), nullable=False)
    department: Mapped[str] = mapped_column(String(100))
    designation: Mapped[str] = mapped_column(String(100))
    date_of_joining: Mapped[date] = mapped_column(Date)
    status: Mapped[EmployeeStatus] = mapped_column(String(20), default=EmployeeStatus.active)
    gross_salary: Mapped[float] = mapped_column(Numeric(12, 2), default=50000.0)
    pf_eligible: Mapped[bool] = mapped_column(Boolean, default=True)
    esi_eligible: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    salaries: Mapped[list["SalaryRecord"]] = relationship("SalaryRecord", back_populates="employee")


class SalaryConfig(Base):
    __tablename__ = "salary_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pf_employee_rate: Mapped[float] = mapped_column(Numeric(6, 4), default=0.12)
    pf_employer_rate: Mapped[float] = mapped_column(Numeric(6, 4), default=0.12)
    esi_employee_rate: Mapped[float] = mapped_column(Numeric(6, 4), default=0.0075)
    esi_employer_rate: Mapped[float] = mapped_column(Numeric(6, 4), default=0.0325)
    esi_threshold: Mapped[float] = mapped_column(Numeric(12, 2), default=21000.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SalaryRecord(Base):
    __tablename__ = "salary_records"
    __table_args__ = (
        UniqueConstraint("employee_id", "salary_month", name="uq_salary_employee_month"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    salary_month: Mapped[date] = mapped_column(Date, nullable=False)
    gross_salary: Mapped[float] = mapped_column(Numeric(12, 2))
    pf_employee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    pf_employer: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    esi_employee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    esi_employer: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    other_deductions: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    net_salary: Mapped[float] = mapped_column(Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    employee: Mapped[Employee] = relationship("Employee", back_populates="salaries")
