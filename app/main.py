# FastAPI application entrypoint
import os
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)

from app.routers import auth, employees, salaries, reports

app = FastAPI(title="test new api", version="0.1.0")

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(employees.router, prefix=API_PREFIX)
app.include_router(salaries.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)


@app.get("/health")
async def health():
    return {"status": "ok"}
