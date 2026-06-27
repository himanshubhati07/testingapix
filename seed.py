<<<<<<< HEAD
# Seed the database with initial data.
import asyncio
from datetime import date
from dotenv import load_dotenv
from sqlalchemy import select
from app.database import Base, async_session, engine
from app.core.security import get_password_hash
from app.models import Employee, User

load_dotenv('.env_c517696b-c1ad-4fbe-ac2d-9f27763c2096', override=True)


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        user_count = len((await session.execute(select(User))).scalars().all())
        if user_count == 0:
            users = [
                User(email="admin@example.com", full_name="Admin User", hashed_password=get_password_hash("AdminPass123")),
                User(email="hr@example.com", full_name="HR Manager", hashed_password=get_password_hash("HRPass123")),
                User(email="finance@example.com", full_name="Finance Lead", hashed_password=get_password_hash("FinancePass123")),
            ]
            session.add_all(users)

        employee_count = len((await session.execute(select(Employee))).scalars().all())
        if employee_count == 0:
            employees = [
                Employee(
                    full_name="Alice Johnson",
                    email="alice.johnson@example.com",
                    department="Engineering",
                    position="Software Engineer",
                    salary=90000,
                    currency="USD",
                    hire_date=date(2022, 6, 1),
                    is_active=True,
                ),
                Employee(
                    full_name="Bob Smith",
                    email="bob.smith@example.com",
                    department="Sales",
                    position="Account Executive",
                    salary=75000,
                    currency="USD",
                    hire_date=date(2021, 3, 15),
                    is_active=True,
                ),
                Employee(
                    full_name="Carol White",
                    email="carol.white@example.com",
                    department="HR",
                    position="HR Specialist",
                    salary=68000,
                    currency="USD",
                    hire_date=date(2020, 11, 30),
                    is_active=True,
                ),
            ]
            session.add_all(employees)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
=======
# Seed script for initial data
import os
import asyncio
from datetime import date
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)

from app.database import engine, SessionLocal, Base
from app.models import Employee, SalaryConfig, SalaryRecord


async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    async with SessionLocal() as session:
        result = await session.execute(select(SalaryConfig))
        if not result.scalar_one_or_none():
            session.add(SalaryConfig())
            await session.commit()

        result = await session.execute(select(Employee))
        if len(result.scalars().all()) == 0:
            employees = [
                Employee(
                    full_name="Aarav Sharma",
                    email="aarav@example.com",
                    phone_number="9000000001",
                    department="Engineering",
                    designation="Developer",
                    date_of_joining=date(2023, 1, 10),
                ),
                Employee(
                    full_name="Diya Singh",
                    email="diya@example.com",
                    phone_number="9000000002",
                    department="Finance",
                    designation="Accountant",
                    date_of_joining=date(2022, 6, 5),
                ),
                Employee(
                    full_name="Rohan Patel",
                    email="rohan@example.com",
                    phone_number="9000000003",
                    department="HR",
                    designation="Manager",
                    date_of_joining=date(2021, 9, 15),
                ),
            ]
            session.add_all(employees)
            await session.commit()

        result = await session.execute(select(SalaryRecord))
        if len(result.scalars().all()) == 0:
            result = await session.execute(select(Employee))
            employees = result.scalars().all()
            for emp in employees:
                session.add(
                    SalaryRecord(
                        employee_id=emp.id,
                        salary_month=date(2024, 1, 1),
                        gross_salary=50000,
                        pf_employee=6000,
                        pf_employer=6000,
                        esi_employee=0,
                        esi_employer=0,
                        other_deductions=0,
                        net_salary=44000,
                    )
                )
            await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_data())
>>>>>>> origin/main
