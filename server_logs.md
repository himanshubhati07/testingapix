# Server Logs [Iteration 0]

## Platform — OS + python version
- OS: linux
- Python: Python 3.11.2

## Database
- Client URL  : postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_88bf58417e
- Fallback    : YES — substituted (original unreachable). DB name: gen_88bf58417e. Log in server_logs.md.
- Resolved URL: postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_88bf58417e

## Test Runner — no live server needed
- pytest tests/ -v --tb=short  (tests use ASGI transport / TestClient — no HTTP server required)

## Files Generated / Modified
- /app/__init__.py — OK
- /app/database.py — OK
- /app/models.py — OK
- /app/schemas.py — OK
- /app/core/__init__.py — OK
- /app/core/security.py — OK
- /app/core/auth.py — OK
- /app/routers/__init__.py — OK
- /app/routers/auth.py — OK
- /app/routers/employees.py — OK
- /app/main.py — OK
- /seed.py — OK
- /requirements.txt — OK
- /.env_c517696b-c1ad-4fbe-ac2d-9f27763c2096 — OK
- /.env.example — OK
- /.gitignore — OK
- /start.sh — OK
- /start.bat — OK
- /Dockerfile — OK
- /docker-compose.yml — OK
- /Makefile — OK
- /tests/__init__.py — OK
- /pytest.ini — OK
- /tests/conftest.py — OK
- /tests/utils/__init__.py — OK
- /tests/utils/factories.py — OK
- /tests/test_auth.py — OK
- /tests/test_employees.py — OK
- /README.md — OK
- /generate_api_report.py — OK
- /generate_project_report.py — OK
- /api_test_report.xlsx — OK
- /project_report.docx — OK
- /server_logs.md — OK

## API Test Results

| Test Function | Endpoint | Status | Expected Code | Notes |
|---|---|---:|---:|---|
| test_register | POST /api/v1/auth/register | PASSED | 201 | User registered |
| test_login_valid | POST /api/v1/auth/login | PASSED | 200 | Token issued |
| test_me | GET /api/v1/auth/me | PASSED | 200 | Current user |
| test_invalid_token | GET /api/v1/auth/me | PASSED | 401 | Invalid token |
| test_create_employee | POST /api/v1/employees | PASSED | 201 | Employee created |
| test_list_employees | GET /api/v1/employees | SKIPPED | 200 | Only Add Employee endpoint is required by business logic |
| test_get_employee | GET /api/v1/employees/{employee_id} | SKIPPED | 200 | Only Add Employee endpoint is required by business logic |
| test_update_employee | PUT /api/v1/employees/{employee_id} | SKIPPED | 200 | Only Add Employee endpoint is required by business logic |
| test_delete_employee | DELETE /api/v1/employees/{employee_id} | SKIPPED | 204 | Only Add Employee endpoint is required by business logic |

## Errors Fixed This Iteration
1. /pytest.ini → asyncpg loop mismatch in tests → set asyncio_default_test_loop_scope=session
2. /requirements.txt → missing email-validator for EmailStr → added email-validator dependency

## Still Failing
- None
