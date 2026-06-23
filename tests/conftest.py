# Pytest fixtures for async database and client
import os
from datetime import date
import pytest
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)

from app.main import app
from app.database import Base, get_db
from app.models import Employee, SalaryRecord, SalaryConfig, User

MAIN_DB_URL = os.getenv("DATABASE_URL", "")
_parts = MAIN_DB_URL.rsplit("/", 1)
TEST_DB_URL = (_parts[0] + "/" + _parts[1] + "_test") if len(_parts) == 2 else MAIN_DB_URL


@pytest.fixture(scope="session")
async def db_engine():
    from sqlalchemy.pool import NullPool

    main_engine = create_async_engine(MAIN_DB_URL, poolclass=NullPool)
    async with main_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await main_engine.dispose()

    engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):
    factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        await session.execute(delete(SalaryRecord))
        await session.execute(delete(Employee))
        await session.execute(delete(User))
        await session.execute(delete(SalaryConfig))
        await session.commit()
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
async def seeded_data(db_session: AsyncSession):
    config = SalaryConfig()
    db_session.add(config)
    employees = [
        Employee(
            full_name="Seed User 1",
            email="seed1@example.com",
            phone_number="9000000101",
            department="Engineering",
            designation="Developer",
            date_of_joining=date(2022, 1, 1),
        ),
        Employee(
            full_name="Seed User 2",
            email="seed2@example.com",
            phone_number="9000000102",
            department="Finance",
            designation="Accountant",
            date_of_joining=date(2021, 6, 1),
        ),
    ]
    db_session.add_all(employees)
    await db_session.flush()
    db_session.add(
        SalaryRecord(
            employee_id=employees[0].id,
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
    await db_session.commit()
    return employees
