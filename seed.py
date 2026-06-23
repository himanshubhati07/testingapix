# Seed script for initial data
import os
import asyncio
from datetime import date
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

load_dotenv('.env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2', override=True)

from app.database import engine, SessionLocal, Base
from app.models import Employee, SalaryConfig, SalaryRecord, WelfareFundConfig


async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    async with SessionLocal() as session:
        result = await session.execute(select(SalaryConfig))
        if not result.scalar_one_or_none():
            session.add(SalaryConfig())
            await session.commit()

        result = await session.execute(select(WelfareFundConfig))
        if not result.scalar_one_or_none():
            session.add(WelfareFundConfig(deduction_type="amount", deduction_value=500, is_active=True))
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
                        welfare_fund_deduction=500,
                        other_deductions=0,
                        net_salary=43500,
                    )
                )
            await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_data())
