# Salary management routes
import os
from datetime import date
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

load_dotenv('.env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2', override=True)

from app.database import get_db
from app.models import Employee, SalaryRecord, SalaryConfig, WelfareFundConfig, WelfareFundType
from app.schemas import SalaryGenerateRequest, SalaryRecordOut, SalaryUpdateRequest, SalarySlipOut

router = APIRouter(prefix="/salaries", tags=["salaries"])


def _round(value: float) -> float:
    return float(round(value, 2))


async def _get_config(db: AsyncSession) -> SalaryConfig:
    result = await db.execute(select(SalaryConfig))
    config = result.scalar_one_or_none()
    if not config:
        config = SalaryConfig()
        db.add(config)
        await db.commit()
        await db.refresh(config)
    return config


async def _get_welfare_config(db: AsyncSession) -> WelfareFundConfig:
    result = await db.execute(select(WelfareFundConfig).where(WelfareFundConfig.is_active.is_(True)))
    config = result.scalar_one_or_none()
    if not config:
        config = WelfareFundConfig(deduction_type=WelfareFundType.amount, deduction_value=0.0, is_active=True)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    return config


def _calculate_deductions(employee: Employee, config: SalaryConfig, gross: float):
    pf_employee = pf_employer = esi_employee = esi_employer = 0.0
    if employee.pf_eligible:
        pf_employee = _round(gross * float(config.pf_employee_rate))
        pf_employer = _round(gross * float(config.pf_employer_rate))
    if employee.esi_eligible and gross <= float(config.esi_threshold):
        esi_employee = _round(gross * float(config.esi_employee_rate))
        esi_employer = _round(gross * float(config.esi_employer_rate))
    return pf_employee, pf_employer, esi_employee, esi_employer


def _calculate_welfare_fund(employee: Employee, config: WelfareFundConfig, gross: float) -> float:
    if not employee.welfare_fund_eligible or not config.is_active:
        return 0.0
    value = float(config.deduction_value)
    if config.deduction_type == WelfareFundType.percentage:
        return _round(gross * value)
    return _round(value)


@router.post("/generate", response_model=SalaryRecordOut, status_code=201)
async def generate_salary(payload: SalaryGenerateRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.id == payload.employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    result = await db.execute(
        select(SalaryRecord).where(
            SalaryRecord.employee_id == payload.employee_id,
            SalaryRecord.salary_month == payload.salary_month,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Salary record already exists for this month")

    config = await _get_config(db)
    welfare_config = await _get_welfare_config(db)
    gross = float(employee.gross_salary)
    pf_employee, pf_employer, esi_employee, esi_employer = _calculate_deductions(employee, config, gross)
    welfare_fund_deduction = _calculate_welfare_fund(employee, welfare_config, gross)
    other_deductions = _round(payload.other_deductions)
    net_salary = _round(gross - pf_employee - esi_employee - welfare_fund_deduction - other_deductions)

    record = SalaryRecord(
        employee_id=employee.id,
        salary_month=payload.salary_month,
        gross_salary=gross,
        pf_employee=pf_employee,
        pf_employer=pf_employer,
        esi_employee=esi_employee,
        esi_employer=esi_employer,
        welfare_fund_deduction=welfare_fund_deduction,
        other_deductions=other_deductions,
        net_salary=net_salary,
    )
    db.add(record)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate salary record") from exc
    await db.refresh(record)
    return record


@router.get("", response_model=list[SalaryRecordOut])
async def list_salaries(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SalaryRecord).limit(limit).offset(offset))
    return result.scalars().all()


@router.get("/{salary_id}", response_model=SalaryRecordOut)
async def get_salary(salary_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SalaryRecord).where(SalaryRecord.id == salary_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Salary record not found")
    return record


@router.get("/employee/{employee_id}", response_model=list[SalaryRecordOut])
async def get_salary_by_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SalaryRecord).where(SalaryRecord.employee_id == employee_id))
    return result.scalars().all()


@router.get("/month/{year}/{month}", response_model=list[SalaryRecordOut])
async def get_salary_by_month(year: int, month: int, db: AsyncSession = Depends(get_db)):
    month_date = date(year, month, 1)
    result = await db.execute(select(SalaryRecord).where(SalaryRecord.salary_month == month_date))
    return result.scalars().all()


@router.put("/{salary_id}", response_model=SalaryRecordOut)
async def update_salary(salary_id: int, payload: SalaryUpdateRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SalaryRecord).where(SalaryRecord.id == salary_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Salary record not found")
    if payload.other_deductions is not None:
        record.other_deductions = _round(payload.other_deductions)
    record.net_salary = _round(
        float(record.gross_salary)
        - float(record.pf_employee)
        - float(record.esi_employee)
        - float(record.welfare_fund_deduction)
        - float(record.other_deductions)
    )
    await db.commit()
    await db.refresh(record)
    return record


@router.get("/{salary_id}/slip", response_model=SalarySlipOut)
async def get_salary_slip(salary_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SalaryRecord).where(SalaryRecord.id == salary_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Salary record not found")
    await db.refresh(record, attribute_names=["employee"])
    return {"employee": record.employee, "salary": record}


@router.get("/{salary_id}/download", response_class=Response)
async def download_salary_slip(salary_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SalaryRecord).where(SalaryRecord.id == salary_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Salary record not found")
    await db.refresh(record, attribute_names=["employee"])
    content = (
        f"Salary Slip for {record.employee.full_name}\n"
        f"Month: {record.salary_month}\n"
        f"Gross: {record.gross_salary}\n"
        f"PF Employee: {record.pf_employee}\n"
        f"ESI Employee: {record.esi_employee}\n"
        f"Welfare Fund: {record.welfare_fund_deduction}\n"
        f"Other Deductions: {record.other_deductions}\n"
        f"Net Salary: {record.net_salary}\n"
    )
    return Response(content=content, media_type="text/plain")
