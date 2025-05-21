#!/bin/bash
trap "kill 0" EXIT

cd frontend && npm run dev &
uvicorn backend.main:app --reload --port 8081 &
wait