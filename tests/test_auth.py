# Tests for authentication endpoints
from httpx import AsyncClient


async def test_register(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"full_name": "Test User", "email": "testuser@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"


async def test_login_valid(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"full_name": "Login User", "email": "login@example.com", "password": "secret123"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "login@example.com", "password": "secret123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_me_and_invalid_token(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"full_name": "Me User", "email": "me@example.com", "password": "secret123"},
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "me@example.com", "password": "secret123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login_response.json()["access_token"]
    me_response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200

    invalid_response = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid"})
    assert invalid_response.status_code == 401
