#!/bin/bash

# File: run_dev.sh
# Purpose: Start GRAIL dev backend and frontend with hot reload

# Start the FastAPI backend in a new Terminal window
osascript <<END
tell application "Terminal"
    do script "cd \"$(pwd)\" && source venv/bin/activate && uvicorn grail.app:app --reload --port 8000"
end tell
END

# Delay briefly to ensure backend is ready
sleep 2

# Start the Streamlit frontend
echo "🧠 Launching Streamlit UI..."
source venv/bin/activate && streamlit run Main.py