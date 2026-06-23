# Pydantic schemas for API requests and responses
import os
from datetime import date, datetime
from typing import Optional, List
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, Field, ConfigDict

load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    is_active: bool


class EmployeeBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    department: str
    designation: str
    date_of_joining: date
    status: str = "Active"
    pf_eligible: bool = True
    esi_eligible: bool = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    date_of_joining: Optional[date] = None
    status: Optional[str] = None
    pf_eligible: Optional[bool] = None
    esi_eligible: Optional[bool] = None


class EmployeeOut(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    gross_salary: float
    created_at: datetime


class SalaryConfigOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pf_employee_rate: float
    pf_employer_rate: float
    esi_employee_rate: float
    esi_employer_rate: float
    esi_threshold: float


class SalaryGenerateRequest(BaseModel):
    employee_id: int
    salary_month: date
    other_deductions: float = 0


class SalaryUpdateRequest(BaseModel):
    other_deductions: Optional[float] = None


class SalaryRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    salary_month: date
    gross_salary: float
    pf_employee: float
    pf_employer: float
    esi_employee: float
    esi_employer: float
    other_deductions: float
    net_salary: float
    created_at: datetime


class SalarySlipOut(BaseModel):
    employee: EmployeeOut
    salary: SalaryRecordOut


class SalaryReportOut(BaseModel):
    total_salary_paid: float
    total_pf_deducted: float
    total_esi_deducted: float


class MonthlyPayrollSummaryOut(BaseModel):
    month: str
    total_employees: int
    total_salary_paid: float
    total_pf_deducted: float
    total_esi_deducted: float


class EmployeeSalaryReportOut(BaseModel):
    employee_id: int
    employee_name: str
    total_paid: float
    total_pf: float
    total_esi: float
    records: List[SalaryRecordOut]
