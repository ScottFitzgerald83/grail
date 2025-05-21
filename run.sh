#!/bin/bash

echo "🔮 Starting GRAIL backend..."
# Start backend in background
uvicorn grail.app:app --reload --port 8000 &

echo "🧠 Launching GRAIL frontend..."
streamlit run Main.py