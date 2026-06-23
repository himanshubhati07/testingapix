COMMIT_MESSAGE: add welfare fund module and update payroll calculations
## Features Added
- Added welfare fund configuration, deduction calculation, employee details, and summary/report APIs
- Integrated welfare fund deductions into salary calculations, slips, and payroll reports
- Added startup migrations to ensure new welfare fund columns exist
- Updated employee lifecycle to mark inactive via update instead of delete

## Files Modified
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/main.py — added welfare router and startup migrations
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/models.py — added welfare fund config and fields
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/schemas.py — added welfare schemas and fields
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/routers/employees.py — removed delete endpoint
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/routers/salaries.py — welfare fund deductions in payroll
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/routers/reports.py — removed PF/ESI summary endpoints, added welfare totals
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/database.py — env file update
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/core/auth.py — env file update
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/core/security.py — env file update
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/conftest.py — welfare migrations and seeded data updates
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/test_employees.py — remove delete test, verify inactive
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/test_salaries.py — welfare deductions in assertions
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/test_reports.py — updated report expectations
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/utils/factories.py — welfare fund payload helpers
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/seed.py — added welfare fund config and deductions
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/start.sh — fixed port 45783

## Files Added
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/app/routers/welfare_fund.py — welfare fund APIs
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/tests/test_welfare_fund.py — welfare fund tests
- /home/ryzen/fast_api_generator_backend/outputs/a4e50816-c0d7-4dbd-b614-aed2c21ff7c2/.env_a4e50816-c0d7-4dbd-b614-aed2c21ff7c2 — runtime configuration

## Secrets Extracted
- None

## DB URLs Resolved
- postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_6511e82291 -> postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_6511e82291

## Test Results Summary
- 13 PASSED, 0 FAILED, 0 SKIPPED
