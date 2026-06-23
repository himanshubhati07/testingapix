# Factory helpers for tests
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv('.env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2', override=True)


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
    }


def welfare_config_payload(deduction_type: str = "amount", deduction_value: float = 500.0, is_active: bool = True):
    return {
        "deduction_type": deduction_type,
        "deduction_value": deduction_value,
        "is_active": is_active,
    }


def welfare_calculate_payload(employee_id: int, gross_salary: float | None = None):
    payload = {"employee_id": employee_id}
    if gross_salary is not None:
        payload["gross_salary"] = gross_salary
    return payload
