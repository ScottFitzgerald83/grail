import json
import time
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "events.log"
KEY_LOG_FILE = LOG_DIR / "api_key_usage.jsonl"

LOG_DIR.mkdir(exist_ok=True)

def log_event(event_type: str, payload: dict, level: str = "info", session_id: str = None, model_name: str = None):
    """
    Log general backend events to a structured log file.
    """
    entry = {
        "timestamp": time.time(),
        "level": level,
        "event_type": event_type,
        "session_id": session_id,
        "model": model_name,
        "payload": payload
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


# Helper for consistently logging inference events
def log_inference(prompt: str, model: str, tokens: int, user: str = "anonymous"):
    log_event("inference", {
        "prompt_preview": prompt[:60],
        "model": model,
        "tokens_used": tokens,
        "user": user
    }, level="info", model_name=model)

def log_api_key_usage(api_key_id: str, model_name: str, tokens_used: int, ip_address: str = None, endpoint: str = None):
    """
    Log per-API key usage in a structured JSONL format.
    """
    entry = {
        "timestamp": time.time(),
        "api_key_id": api_key_id,
        "model": model_name,
        "tokens": tokens_used,
        "ip_address": ip_address,
        "endpoint": endpoint
    }
    with open(KEY_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def log_request(method: str, path: str, status_code: int, duration_ms: float, ip_address: str = None, user_agent: str = None, session_id: str = None):
    """
    Log HTTP requests in a structured format.
    """
    entry = {
        "timestamp": time.time(),
        "event_type": "http_request",
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": duration_ms,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "session_id": session_id
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")