

import os
import uuid
import json
from datetime import datetime

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

def create_session():
    return str(uuid.uuid4())

def save_session(session_id: str, data: dict):
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_session(session_id: str) -> dict:
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No session found with ID {session_id}")
    with open(path) as f:
        return json.load(f)

def list_sessions():
    files = os.listdir(SESSIONS_DIR)
    return sorted([
        {"id": f[:-5], "timestamp": datetime.fromtimestamp(os.path.getmtime(os.path.join(SESSIONS_DIR, f))).isoformat()}
        for f in files if f.endswith(".json")
    ], key=lambda x: x["timestamp"], reverse=True)

def export_session(session_id: str, format="json"):
    data = load_session(session_id)
    if format == "json":
        return json.dumps(data, indent=2)
    elif format == "md":
        return "\n".join(f"### {k}\n```\n{v}\n```" for k, v in data.items())
    else:
        raise ValueError(f"Unsupported export format: {format}")