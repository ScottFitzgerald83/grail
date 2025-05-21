#!/bin/bash

# run.sh — Launch GRAIL backend and frontend in two terminals

echo "🔮 Launching GRAIL backend..."
gnome-terminal -- bash -c "uvicorn grail.app:app --reload --port 8000; exec bash"

echo "🧠 Launching GRAIL UI..."
streamlit run Main.py