import os
import json
from datetime import datetime

EVAL_LOG = "eval_log.jsonl"

def save_prompt_feedback(session_id, prompt, model, metrics: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": session_id,
        "prompt": prompt,
        "model": model,
        "metrics": metrics
    }
    with open(EVAL_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return {"status": "saved", "entry": entry}
