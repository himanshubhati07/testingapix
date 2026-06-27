@echo off
<<<<<<< HEAD
set PORT=33047
set PYTHONUNBUFFERED=1

if not exist .venv (
  python -m venv .venv
)

call .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 33047
=======
set PORT=56961
python -m pip install -r requirements.txt -q
uvicorn app.main:app --host 0.0.0.0 --port 56961
>>>>>>> origin/main
