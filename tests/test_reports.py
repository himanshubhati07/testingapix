# Tests for report endpoints
from httpx import AsyncClient


async def test_reports_endpoints(client: AsyncClient, seeded_data):
    total_resp = await client.get("/api/v1/reports/total-salary-paid")
    assert total_resp.status_code == 200
    total_data = total_resp.json()
    assert total_data["total_welfare_fund_deducted"] == 500.0

    monthly_resp = await client.get("/api/v1/reports/monthly-payroll-summary")
    assert monthly_resp.status_code == 200

    employee_id = seeded_data[0].id
    emp_report_resp = await client.get(f"/api/v1/reports/employee-salary-report/{employee_id}")
    assert emp_report_resp.status_code == 200
