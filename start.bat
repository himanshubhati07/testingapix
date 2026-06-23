@echo off
set PORT=56961
python -m pip install -r requirements.txt -q
uvicorn app.main:app --host 0.0.0.0 --port 56961
