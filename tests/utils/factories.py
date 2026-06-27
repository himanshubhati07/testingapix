<<<<<<< HEAD
# Test data factories.
from datetime import date
import uuid


def user_payload(email: str | None = None):
    return {
        "email": email or f"user-{uuid.uuid4()}@example.com",
        "password": "StrongPass123",
        "full_name": "Test User",
    }


def employee_payload(email: str | None = None):
    return {
        "full_name": "Jane Employee",
        "email": email or f"employee-{uuid.uuid4()}@example.com",
        "department": "Engineering",
        "position": "Backend Engineer",
        "salary": 88000,
        "currency": "USD",
        "hire_date": date(2022, 1, 5).isoformat(),
        "is_active": True,
=======
# Factory helpers for tests
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv('.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6', override=True)


def employee_payload(index: int = 1):
    return {
        "full_name": f"Employee {index}",
        "email": f"employee{index}@example.com",
        "phone_number": f"90000000{index:02d}",
        "department": "Engineering",
        "designation": "Developer",
        "date_of_joining": date(2023, 1, 1).isoformat(),
        "status": "Active",
        "pf_eligible": True,
        "esi_eligible": True,
    }


def salary_generate_payload(employee_id: int, month: date, other_deductions: float = 0):
    return {
        "employee_id": employee_id,
        "salary_month": month.isoformat(),
        "other_deductions": other_deductions,
>>>>>>> origin/main
    }
