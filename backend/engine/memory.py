import json
from datetime import datetime
import os

def save_session(session_id, messages, model_name, total_tokens):
    session_data = {
        "id": session_id,
        "messages": messages,
        "model": model_name,
        "tokens_used": total_tokens,
        "cost_estimate": round(total_tokens * 0.00002, 4),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    filename = f"session_{session_id}.json"
    with open(filename, 'w') as f:
        json.dump(session_data, f, indent=2)

def load_session(session_id):
    filename = f"session_{session_id}.json"
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as f:
        try:
            data = json.load(f)
            # Validate expected keys
            if all(key in data for key in ("id", "messages", "model", "tokens_used", "cost_estimate", "created_at")):
                return data
            else:
                # Fallback for legacy format: assume entire file is messages list
                return {
                    "id": session_id,
                    "messages": data,
                    "model": None,
                    "tokens_used": 0,
                    "cost_estimate": 0.0,
                    "created_at": None
                }
        except json.JSONDecodeError:
            # Fallback for legacy format: try to read as plain text or other format
            return None
