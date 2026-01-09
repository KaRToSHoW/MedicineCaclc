#!/bin/bash
# Start Python FastAPI backend

cd /home/runner/app/api
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
