

import json
import time
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "events.log"
KEY_LOG_FILE = LOG_DIR / "api_key_usage.jsonl"

LOG_DIR.mkdir(exist_ok=True)

def log_event(event_type: str, payload: dict):
    """
    Log general backend events to a flat file.
    """
    entry = {
        "timestamp": time.time(),
        "event_type": event_type,
        "payload": payload
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def log_api_key_usage(api_key_id: str, model_name: str, tokens_used: int):
    """
    Log per-API key usage in a structured JSONL format.
    """
    entry = {
        "timestamp": time.time(),
        "api_key_id": api_key_id,
        "model": model_name,
        "tokens": tokens_used
    }
    with open(KEY_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")