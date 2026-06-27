#!/usr/bin/env bash
set -e
<<<<<<< HEAD
export PYTHONUNBUFFERED=1
PORT=33047

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

. .venv/bin/activate
pip install -r requirements.txt

exec uvicorn app.main:app --host 0.0.0.0 --port 33047
=======
PORT=56961
export PORT=56961
export PYTHONUNBUFFERED=1
python3 -m pip install -r requirements.txt -q
exec uvicorn app.main:app --host 0.0.0.0 --port 56961
>>>>>>> origin/main
