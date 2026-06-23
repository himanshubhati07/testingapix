# Welfare fund management routes
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv('.env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2', override=True)

from app.database import get_db
from app.models import Employee, SalaryRecord, WelfareFundConfig, WelfareFundType
from app.schemas import (
    WelfareFundConfigCreate,
    WelfareFundConfigUpdate,
    WelfareFundConfigOut,
    WelfareFundCalculateRequest,
    WelfareFundDeductionOut,
    EmployeeWelfareFundReportOut,
    WelfareFundSummaryOut,
    MonthlyWelfareFundSummaryOut,
)

router = APIRouter(prefix="/welfare-fund", tags=["welfare-fund"])


def _round(value: float) -> float:
    return float(round(value, 2))


async def _get_active_config(db: AsyncSession) -> WelfareFundConfig:
    result = await db.execute(select(WelfareFundConfig).where(WelfareFundConfig.is_active.is_(True)))
    config = result.scalar_one_or_none()
    if not config:
        config = WelfareFundConfig(deduction_type=WelfareFundType.amount, deduction_value=0.0, is_active=True)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    return config


def _calculate_welfare_deduction(config: WelfareFundConfig, gross: float) -> float:
    value = float(config.deduction_value)
    if config.deduction_type == WelfareFundType.percentage:
        return _round(gross * value)
    return _round(value)


@router.post("/config", response_model=WelfareFundConfigOut, status_code=201)
async def create_welfare_config(payload: WelfareFundConfigCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WelfareFundConfig))
    configs = result.scalars().all()
    for config in configs:
        config.is_active = False
    config = WelfareFundConfig(
        deduction_type=payload.deduction_type,
        deduction_value=payload.deduction_value,
        is_active=payload.is_active,
    )
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return config


@router.put("/config/{config_id}", response_model=WelfareFundConfigOut)
async def update_welfare_config(
    config_id: int,
    payload: WelfareFundConfigUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(WelfareFundConfig).where(WelfareFundConfig.id == config_id))
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="Welfare fund config not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(config, key, value)
    await db.commit()
    await db.refresh(config)
    return config


@router.get("/config", response_model=WelfareFundConfigOut)
async def get_welfare_config(db: AsyncSession = Depends(get_db)):
    config = await _get_active_config(db)
    return config


@router.post("/calculate", response_model=WelfareFundDeductionOut)
async def calculate_welfare_deduction(
    payload: WelfareFundCalculateRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Employee).where(Employee.id == payload.employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    config = await _get_active_config(db)
    gross = float(payload.gross_salary) if payload.gross_salary is not None else float(employee.gross_salary)
    deduction = 0.0
    if employee.welfare_fund_eligible and config.is_active:
        deduction = _calculate_welfare_deduction(config, gross)
    return {
        "employee_id": employee.id,
        "gross_salary": gross,
        "deduction_type": config.deduction_type,
        "deduction_value": float(config.deduction_value),
        "welfare_fund_deduction": deduction,
    }


@router.get("/employee/{employee_id}", response_model=EmployeeWelfareFundReportOut)
async def get_employee_welfare_fund(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    result = await db.execute(select(SalaryRecord).where(SalaryRecord.employee_id == employee_id))
    records = result.scalars().all()
    total_welfare = sum(float(r.welfare_fund_deduction) for r in records)
    return {
        "employee_id": employee.id,
        "employee_name": employee.full_name,
        "total_welfare_fund": total_welfare,
        "records": records,
    }


@router.get("/report", response_model=WelfareFundSummaryOut)
async def welfare_fund_report(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            func.coalesce(func.sum(SalaryRecord.welfare_fund_deduction), 0),
            func.count(func.distinct(SalaryRecord.employee_id)),
        )
    )
    total_welfare, total_employees = result.first()
    return {
        "total_welfare_fund_deducted": float(total_welfare),
        "total_employees": int(total_employees or 0),
    }


@router.get("/monthly-summary", response_model=list[MonthlyWelfareFundSummaryOut])
async def monthly_welfare_summary(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            SalaryRecord.salary_month,
            func.count(SalaryRecord.id),
            func.coalesce(func.sum(SalaryRecord.welfare_fund_deduction), 0),
        ).group_by(SalaryRecord.salary_month)
    )
    summaries = []
    for month, count, total_welfare in result.all():
        summaries.append(
            {
                "month": month.strftime("%Y-%m"),
                "total_employees": int(count),
                "total_welfare_fund_deducted": float(total_welfare),
            }
        )
    return summaries
