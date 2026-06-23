# Employee management routes
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

load_dotenv('.env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2', override=True)

from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeOut, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeOut, status_code=201)
async def create_employee(payload: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    count_result = await db.execute(select(func.count(Employee.id)))
    if count_result.scalar_one() >= 10:
        raise HTTPException(status_code=422, detail="Employee limit reached (max 10)")
    employee = Employee(**payload.model_dump())
    db.add(employee)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate employee record") from exc
    await db.refresh(employee)
    return employee


@router.get("", response_model=list[EmployeeOut])
async def list_employees(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).limit(limit).offset(offset))
    return result.scalars().all()


@router.get("/{employee_id}", response_model=EmployeeOut)
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeOut)
async def update_employee(employee_id: int, payload: EmployeeUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate employee record") from exc
    await db.refresh(employee)
    return employee
