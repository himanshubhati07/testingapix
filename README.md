# test new api

<<<<<<< HEAD
Salary Management REST API with JWT authentication and an Add Employee endpoint.

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Create env file:

```
cp .env.example .env_c517696b-c1ad-4fbe-ac2d-9f27763c2096
```

## Run

```bash
chmod +x ./start.sh
PORT=33047 bash ./start.sh
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL async URL
- `SECRET_KEY` - JWT signing key
- `JWT_ALGORITHM` - HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES` - token expiry in minutes
- `PORT` - server port (33047)

## API Endpoints

- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Current user
- `POST /api/v1/employees` - Add employee
- `GET /health` - Health check

## Tests

=======
Salary Management System API built with FastAPI.

## Features
- Employee CRUD with max 10 employees validation
- Automatic salary generation with PF/ESI calculations
- Salary slips and reporting endpoints
- JWT authentication

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables
Defined in `.env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6`:
- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- PORT

## Run
```bash
PORT=56961 bash ./start.sh
```

## API Endpoints (prefix: /api/v1)
- Auth: POST /auth/register, POST /auth/login, GET /auth/me
- Employees: POST /employees, GET /employees, GET /employees/{id}, PUT /employees/{id}, DELETE /employees/{id}
- Salaries: POST /salaries/generate, GET /salaries, GET /salaries/{id},
  GET /salaries/employee/{employee_id}, GET /salaries/month/{year}/{month},
  PUT /salaries/{id}, GET /salaries/{id}/slip, GET /salaries/{id}/download
- Reports: GET /reports/total-salary-paid, /reports/total-pf-deducted, /reports/total-esi-deducted,
  /reports/monthly-payroll-summary, /reports/employee-salary-report/{employee_id}

## Tests
>>>>>>> origin/main
```bash
pytest tests/ -v --tb=short
```

## Docker
<<<<<<< HEAD

```bash
docker compose up --build
```

## Project Tree

=======
```bash
docker build -t salary-api .
docker run -p 56961:56961 --env-file .env_d3b2dbc6-eb80-47a1-8fc6-6d72dad7f2f6 salary-api
```

## Project Tree
>>>>>>> origin/main
```
app/
  core/
  routers/
  database.py
<<<<<<< HEAD
  main.py
  models.py
  schemas.py
tests/
  utils/
seed.py
=======
  models.py
  schemas.py
seed.py
start.sh
start.bat
>>>>>>> origin/main
```
