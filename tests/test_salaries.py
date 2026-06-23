# Tests for salary endpoints
from datetime import date
from httpx import AsyncClient
from tests.utils.factories import employee_payload, salary_generate_payload, welfare_config_payload


async def test_generate_salary_and_calculation(client: AsyncClient):
    await client.post("/api/v1/welfare-fund/config", json=welfare_config_payload())
    emp_resp = await client.post("/api/v1/employees", json=employee_payload(21))
    employee_id = emp_resp.json()["id"]
    payload = salary_generate_payload(employee_id, date(2024, 2, 1), other_deductions=500)
    response = await client.post("/api/v1/salaries/generate", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["pf_employee"] == 6000.0
    assert data["esi_employee"] == 0.0
    assert data["welfare_fund_deduction"] == 500.0
    assert data["net_salary"] == 43000.0


async def test_list_and_get_salary(client: AsyncClient):
    await client.post("/api/v1/welfare-fund/config", json=welfare_config_payload())
    emp_resp = await client.post("/api/v1/employees", json=employee_payload(22))
    employee_id = emp_resp.json()["id"]
    payload = salary_generate_payload(employee_id, date(2024, 3, 1))
    create_resp = await client.post("/api/v1/salaries/generate", json=payload)
    salary_id = create_resp.json()["id"]

    list_resp = await client.get("/api/v1/salaries")
    assert list_resp.status_code == 200

    get_resp = await client.get(f"/api/v1/salaries/{salary_id}")
    assert get_resp.status_code == 200


async def test_update_salary_and_slip_download(client: AsyncClient):
    await client.post("/api/v1/welfare-fund/config", json=welfare_config_payload())
    emp_resp = await client.post("/api/v1/employees", json=employee_payload(23))
    employee_id = emp_resp.json()["id"]
    payload = salary_generate_payload(employee_id, date(2024, 4, 1))
    create_resp = await client.post("/api/v1/salaries/generate", json=payload)
    salary_id = create_resp.json()["id"]

    update_resp = await client.put(f"/api/v1/salaries/{salary_id}", json={"other_deductions": 1000})
    assert update_resp.status_code == 200
    assert update_resp.json()["net_salary"] == 42500.0

    slip_resp = await client.get(f"/api/v1/salaries/{salary_id}/slip")
    assert slip_resp.status_code == 200

    download_resp = await client.get(f"/api/v1/salaries/{salary_id}/download")
    assert download_resp.status_code == 200
    assert "Salary Slip" in download_resp.text
