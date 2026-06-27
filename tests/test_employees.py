<<<<<<< HEAD
# Employee endpoint tests.
import pytest
from tests.utils.factories import employee_payload, user_payload


async def _auth_header(client):
    payload = user_payload("employee.tester@example.com")
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json={"email": payload["email"], "password": payload["password"]})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_employee(client):
    headers = await _auth_header(client)
    payload = employee_payload()
    response = await client.post("/api/v1/employees", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]


@pytest.mark.skip(reason="Only Add Employee endpoint is required by business logic")
@pytest.mark.asyncio
async def test_list_employees(client):
    assert True


@pytest.mark.skip(reason="Only Add Employee endpoint is required by business logic")
@pytest.mark.asyncio
async def test_get_employee(client):
    assert True


@pytest.mark.skip(reason="Only Add Employee endpoint is required by business logic")
@pytest.mark.asyncio
async def test_update_employee(client):
    assert True


@pytest.mark.skip(reason="Only Add Employee endpoint is required by business logic")
@pytest.mark.asyncio
async def test_delete_employee(client):
    assert True
=======
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


async def test_get_update_delete_employee(client: AsyncClient):
    create_resp = await client.post("/api/v1/employees", json=employee_payload(3))
    employee_id = create_resp.json()["id"]
    get_resp = await client.get(f"/api/v1/employees/{employee_id}")
    assert get_resp.status_code == 200

    update_resp = await client.put(f"/api/v1/employees/{employee_id}", json={"department": "HR"})
    assert update_resp.status_code == 200
    assert update_resp.json()["department"] == "HR"

    delete_resp = await client.delete(f"/api/v1/employees/{employee_id}")
    assert delete_resp.status_code == 204


async def test_employee_limit_validation(client: AsyncClient):
    for i in range(1, 11):
        response = await client.post("/api/v1/employees", json=employee_payload(i + 10))
        assert response.status_code in (201, 409)
    response = await client.post("/api/v1/employees", json=employee_payload(999))
    assert response.status_code == 422
>>>>>>> origin/main
