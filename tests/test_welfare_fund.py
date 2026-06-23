# Tests for welfare fund endpoints
from datetime import date
from httpx import AsyncClient
from tests.utils.factories import employee_payload, salary_generate_payload, welfare_config_payload, welfare_calculate_payload


async def test_welfare_fund_config_and_calculation(client: AsyncClient):
    create_resp = await client.post("/api/v1/welfare-fund/config", json=welfare_config_payload("percentage", 0.01))
    assert create_resp.status_code == 201
    config_id = create_resp.json()["id"]

    get_resp = await client.get("/api/v1/welfare-fund/config")
    assert get_resp.status_code == 200
    assert get_resp.json()["deduction_type"] == "percentage"

    update_resp = await client.put(
        f"/api/v1/welfare-fund/config/{config_id}",
        json={"deduction_value": 0.02},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["deduction_value"] == 0.02

    emp_resp = await client.post("/api/v1/employees", json=employee_payload(31))
    employee_id = emp_resp.json()["id"]
    calc_resp = await client.post(
        "/api/v1/welfare-fund/calculate",
        json=welfare_calculate_payload(employee_id, gross_salary=50000),
    )
    assert calc_resp.status_code == 200
    assert calc_resp.json()["welfare_fund_deduction"] == 1000.0


async def test_welfare_fund_employee_and_reports(client: AsyncClient, seeded_data):
    await client.post("/api/v1/welfare-fund/config", json=welfare_config_payload())
    emp_resp = await client.post("/api/v1/employees", json=employee_payload(32))
    employee_id = emp_resp.json()["id"]
    payload = salary_generate_payload(employee_id, date(2024, 5, 1))
    await client.post("/api/v1/salaries/generate", json=payload)

    employee_resp = await client.get(f"/api/v1/welfare-fund/employee/{employee_id}")
    assert employee_resp.status_code == 200
    assert employee_resp.json()["total_welfare_fund"] == 500.0

    report_resp = await client.get("/api/v1/welfare-fund/report")
    assert report_resp.status_code == 200
    assert report_resp.json()["total_welfare_fund_deducted"] >= 500.0

    monthly_resp = await client.get("/api/v1/welfare-fund/monthly-summary")
    assert monthly_resp.status_code == 200
    assert isinstance(monthly_resp.json(), list)
