# Reporting routes for salary management
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv('.env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2', override=True)

from app.database import get_db
from app.models import SalaryRecord, Employee
from app.schemas import SalaryReportOut, MonthlyPayrollSummaryOut, EmployeeSalaryReportOut

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/total-salary-paid", response_model=SalaryReportOut)
async def total_salary_paid(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            func.coalesce(func.sum(SalaryRecord.net_salary), 0),
            func.coalesce(func.sum(SalaryRecord.pf_employee), 0),
            func.coalesce(func.sum(SalaryRecord.esi_employee), 0),
            func.coalesce(func.sum(SalaryRecord.welfare_fund_deduction), 0),
        )
    )
    total_salary, total_pf, total_esi, total_welfare = result.first()
    return {
        "total_salary_paid": float(total_salary),
        "total_pf_deducted": float(total_pf),
        "total_esi_deducted": float(total_esi),
        "total_welfare_fund_deducted": float(total_welfare),
    }


@router.get("/monthly-payroll-summary", response_model=list[MonthlyPayrollSummaryOut])
async def monthly_payroll_summary(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            SalaryRecord.salary_month,
            func.count(SalaryRecord.id),
            func.coalesce(func.sum(SalaryRecord.net_salary), 0),
            func.coalesce(func.sum(SalaryRecord.pf_employee), 0),
            func.coalesce(func.sum(SalaryRecord.esi_employee), 0),
            func.coalesce(func.sum(SalaryRecord.welfare_fund_deduction), 0),
        ).group_by(SalaryRecord.salary_month)
    )
    summaries = []
    for month, count, total_salary, total_pf, total_esi, total_welfare in result.all():
        summaries.append(
            {
                "month": month.strftime("%Y-%m"),
                "total_employees": int(count),
                "total_salary_paid": float(total_salary),
                "total_pf_deducted": float(total_pf),
                "total_esi_deducted": float(total_esi),
                "total_welfare_fund_deducted": float(total_welfare),
            }
        )
    return summaries


@router.get("/employee-salary-report/{employee_id}", response_model=EmployeeSalaryReportOut)
async def employee_salary_report(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    result = await db.execute(select(SalaryRecord).where(SalaryRecord.employee_id == employee_id))
    records = result.scalars().all()
    total_paid = sum(float(r.net_salary) for r in records)
    total_pf = sum(float(r.pf_employee) for r in records)
    total_esi = sum(float(r.esi_employee) for r in records)
    total_welfare = sum(float(r.welfare_fund_deduction) for r in records)
    return {
        "employee_id": employee.id,
        "employee_name": employee.full_name,
        "total_paid": total_paid,
        "total_pf": total_pf,
        "total_esi": total_esi,
        "total_welfare_fund": total_welfare,
        "records": records,
    }
