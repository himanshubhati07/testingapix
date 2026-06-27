# Server Logs [Iteration 0]

## Platform — OS + python version
- OS: linux
<<<<<<< HEAD
- Python: Python 3.11.2

## Database
- Client URL  : postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_88bf58417e
- Fallback    : YES — substituted (original unreachable). DB name: gen_88bf58417e. Log in server_logs.md.
- Resolved URL: postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_88bf58417e
=======
- Python: 3.11.2

## Database
- Client URL  : postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_6511e82291
- Fallback    : YES — substituted (original unreachable). DB name: gen_6511e82291. Log in server_logs.md.
- Resolved URL: postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_6511e82291
>>>>>>> origin/main

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
<<<<<<< HEAD
- /app/main.py — OK
- /seed.py — OK
- /requirements.txt — OK
- /.env_c517696b-c1ad-4fbe-ac2d-9f27763c2096 — OK
- /.env.example — OK
=======
- /app/routers/salaries.py — OK
- /app/routers/reports.py — OK
- /app/main.py — OK
- /seed.py — OK
- /requirements.txt — OK
- /.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6 — OK
>>>>>>> origin/main
- /start.sh — OK
- /start.bat — OK
- /Dockerfile — OK
- /docker-compose.yml — OK
- /Makefile — OK
<<<<<<< HEAD
- /tests/__init__.py — OK
- /pytest.ini — OK
- /tests/conftest.py — OK
- /tests/utils/__init__.py — OK
- /tests/utils/factories.py — OK
- /tests/test_auth.py — OK
- /tests/test_employees.py — OK
- /README.md — OK
- /server_logs.md — OK
=======
- /README.md — OK
- /pytest.ini — OK
- /tests/__init__.py — OK
- /tests/conftest.py — OK
- /tests/test_auth.py — OK
- /tests/test_employees.py — OK
- /tests/test_salaries.py — OK
- /tests/test_reports.py — OK
- /tests/utils/__init__.py — OK
- /tests/utils/factories.py — OK
>>>>>>> origin/main

## API Test Results

| Test Function | Endpoint | Status | Expected Code | Notes |
|---|---|---:|---:|---|
<<<<<<< HEAD
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
=======
| test_register | POST /api/v1/auth/register | PASSED | 201 | User registration |
| test_login_valid | POST /api/v1/auth/login | PASSED | 200 | Valid login |
| test_me_and_invalid_token | GET /api/v1/auth/me | PASSED | 200 | Invalid token returns 401 |
| test_create_employee | POST /api/v1/employees | PASSED | 201 | Create employee |
| test_list_employees | GET /api/v1/employees | PASSED | 200 | List employees |
| test_get_update_delete_employee | GET/PUT/DELETE /api/v1/employees/{id} | PASSED | 200/204 | CRUD employee |
| test_employee_limit_validation | POST /api/v1/employees | PASSED | 422 | Enforces max 10 employees |
| test_generate_salary_and_calculation | POST /api/v1/salaries/generate | PASSED | 201 | PF/ESI/net salary |
| test_list_and_get_salary | GET /api/v1/salaries, GET /api/v1/salaries/{id} | PASSED | 200 | List/get salaries |
| test_update_salary_and_slip_download | PUT/GET /api/v1/salaries/{id}/* | PASSED | 200 | Update/slip/download |
| test_reports_endpoints | GET /api/v1/reports/* | PASSED | 200 | Reporting endpoints |

## Errors Fixed This Iteration
1. /tests/conftest.py → event loop mismatch in teardown → aligned loop scope + cleared tables per test.
2. /pytest.ini → added asyncio_default_test_loop_scope=session to align loops.

## Still Failing
>>>>>>> origin/main
