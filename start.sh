#!/usr/bin/env bash
set -e
PORT=45783
export PORT=45783
export PYTHONUNBUFFERED=1
python3 -m pip install -r requirements.txt -q
exec uvicorn app.main:app --host 0.0.0.0 --port 45783
