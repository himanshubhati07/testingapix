# Server Logs [Iteration 0]

## Platform - OS + python version
- OS: linux
- Python: 3.11.2

## Database
- Original URLs : postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_6511e82291
- Resolved URLs : postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_6511e82291
- Env file      : .env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2

## Start Script - which script was used
- start.sh (PORT=45783)

## Files Generated / Modified
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/.env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2 - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/start.sh - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/main.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/models.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/schemas.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/routers/employees.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/routers/salaries.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/routers/reports.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/routers/welfare_fund.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/database.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/core/auth.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/core/security.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/conftest.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/test_employees.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/test_reports.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/test_salaries.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/test_welfare_fund.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/utils/factories.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/seed.py - OK

## API Test Results

| Method | Path | Status | HTTP Code | Notes |
|---|---|---:|---:|---|
| GET | /health | PASSED | 200 | Health check OK |
| POST | /api/v1/auth/register | PASSED | 201 | User registration |
| POST | /api/v1/auth/login | PASSED | 200 | User login |
| GET | /api/v1/auth/me | PASSED | 200 | Authenticated user |
| POST | /api/v1/employees | PASSED | 201 | Create employee |
| GET | /api/v1/employees | PASSED | 200 | List employees |
| GET | /api/v1/employees/{id} | PASSED | 200 | Get employee |
| PUT | /api/v1/employees/{id} | PASSED | 200 | Update employee + inactive status |
| POST | /api/v1/salaries/generate | PASSED | 201 | Generate salary |
| GET | /api/v1/salaries | PASSED | 200 | List salaries |
| GET | /api/v1/salaries/{id} | PASSED | 200 | Get salary |
| PUT | /api/v1/salaries/{id} | PASSED | 200 | Update salary |
| GET | /api/v1/salaries/{id}/slip | PASSED | 200 | Salary slip |
| GET | /api/v1/salaries/{id}/download | PASSED | 200 | Salary slip download |
| GET | /api/v1/reports/total-salary-paid | PASSED | 200 | Salary totals |
| GET | /api/v1/reports/monthly-payroll-summary | PASSED | 200 | Monthly payroll summary |
| GET | /api/v1/reports/employee-salary-report/{id} | PASSED | 200 | Employee report |
| POST | /api/v1/welfare-fund/config | PASSED | 201 | Create welfare config |
| PUT | /api/v1/welfare-fund/config/{id} | PASSED | 200 | Update welfare config |
| GET | /api/v1/welfare-fund/config | PASSED | 200 | Get welfare config |
| POST | /api/v1/welfare-fund/calculate | PASSED | 200 | Calculate welfare deduction |
| GET | /api/v1/welfare-fund/employee/{id} | PASSED | 200 | Employee welfare details |
| GET | /api/v1/welfare-fund/report | PASSED | 200 | Welfare fund report |
| GET | /api/v1/welfare-fund/monthly-summary | PASSED | 200 | Monthly welfare summary |

## Errors Fixed This Iteration
1. start.sh -> hardcoded port 56961 -> updated to 45783 for required port
2. tests/conftest.py/app/main.py -> missing welfare fund columns in existing DB -> added ALTER TABLE migrations before usage

## Still Failing
- None

