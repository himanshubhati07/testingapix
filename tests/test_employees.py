# Tests for employee endpoints
from httpx import AsyncClient
from tests.utils.factories import employee_payload


async def test_create_employee(client: AsyncClient):
    response = await client.post("/api/v1/employees", json=employee_payload(1))
    assert response.status_code == 201
    assert response.json()["email"] == "employee1@example.com"


async def test_list_employees(client: AsyncClient):
    await client.post("/api/v1/employees", json=employee_payload(2))
    response = await client.get("/api/v1/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_update_employee(client: AsyncClient):
    create_resp = await client.post("/api/v1/employees", json=employee_payload(3))
    employee_id = create_resp.json()["id"]
    get_resp = await client.get(f"/api/v1/employees/{employee_id}")
    assert get_resp.status_code == 200

    update_resp = await client.put(
        f"/api/v1/employees/{employee_id}",
        json={"department": "HR", "status": "Inactive"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["department"] == "HR"
    assert update_resp.json()["status"] == "Inactive"


async def test_employee_limit_validation(client: AsyncClient):
    for i in range(1, 11):
        response = await client.post("/api/v1/employees", json=employee_payload(i + 10))
        assert response.status_code in (201, 409)
    response = await client.post("/api/v1/employees", json=employee_payload(999))
    assert response.status_code == 422
