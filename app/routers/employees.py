<<<<<<< HEAD
# Employee routes for salary management.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.auth import get_current_user
from ..database import get_db
from ..models import Employee, User
from ..schemas import EmployeeCreate, EmployeeOut
=======
# Employee management routes
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)

from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeOut, EmployeeUpdate
>>>>>>> origin/main

router = APIRouter(prefix="/employees", tags=["employees"])


<<<<<<< HEAD
@router.post("", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
async def add_employee(
    payload: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    existing = await db.execute(select(Employee).where(Employee.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee email already exists")
    employee = Employee(
        full_name=payload.full_name,
        email=payload.email,
        department=payload.department,
        position=payload.position,
        salary=payload.salary,
        currency=payload.currency,
        hire_date=payload.hire_date,
        is_active=payload.is_active,
    )
    db.add(employee)
    await db.commit()
    await db.refresh(employee)
    return employee
=======
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


@router.delete("/{employee_id}", status_code=204)
async def delete_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    await db.delete(employee)
    await db.commit()
    return None
>>>>>>> origin/main
