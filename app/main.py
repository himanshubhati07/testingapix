# FastAPI application entrypoint
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import text

load_dotenv('.env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2', override=True)

from app.database import engine, Base
from app.routers import auth, employees, salaries, reports, welfare_fund

app = FastAPI(title="test new api", version="0.1.0")

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(employees.router, prefix=API_PREFIX)
app.include_router(salaries.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)
app.include_router(welfare_fund.router, prefix=API_PREFIX)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            text(
                "ALTER TABLE employees "
                "ADD COLUMN IF NOT EXISTS welfare_fund_eligible BOOLEAN DEFAULT true"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE salary_records "
                "ADD COLUMN IF NOT EXISTS welfare_fund_deduction NUMERIC(12, 2) DEFAULT 0"
            )
        )


@app.get("/health")
async def health():
    return {"status": "ok"}
