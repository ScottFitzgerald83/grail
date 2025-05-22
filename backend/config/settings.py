# backend/config/settings.py

from typing import Dict
import yaml
from pathlib import Path

DEFAULT_CONFIG = {
    "model_name": "gpt2",
    "attention": "dense",  # dense, sparse, flash, local, hybrid
    "precision": "fp16",  # float32, fp16, int8, bf16
    "ffn_mode": "standard",  # standard, lowrank, fused, quantized
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.9,
    "device": "cuda"
}

PRESET_FILE = Path(__file__).parent / "presets.yaml"


def get_config(overrides: Dict = {}) -> Dict:
    config = DEFAULT_CONFIG.copy()
    config.update(overrides)
    return config


# Translate GRAIL unified config to model-specific payload for inference.
def translate_config(config: Dict, model_name: str) -> Dict:
    """Translate GRAIL unified config to model-specific payload for inference."""
    if model_name.startswith("gpt-"):
        return {
            "model": model_name,
            "messages": [{"role": "user", "content": config.get("prompt", "")}],
            "temperature": config.get("temperature", 0.7),
            "top_p": config.get("top_p", 0.9),
            "max_tokens": config.get("max_tokens", 256),
            "presence_penalty": config.get("presence_penalty", 0.0),
            "frequency_penalty": config.get("frequency_penalty", 0.0),
            "stream": config.get("stream", "false") == "true"
        }
    elif model_name.startswith("ollama:"):
        return {
            "model": model_name.split(":", 1)[1],
            "prompt": config.get("prompt", ""),
            "stream": False,
            "options": {
                "temperature": config.get("temperature", 0.7),
                "top_p": config.get("top_p", 0.9),
                "num_predict": config.get("max_tokens", 256)
            }
        }
    else:
        return config  # return as-is for unsupported types


def load_presets() -> Dict:
    if PRESET_FILE.exists():
        with open(PRESET_FILE, "r") as f:
            return yaml.safe_load(f)
    return {}


def save_presets(presets: Dict):
    with open(PRESET_FILE, "w") as f:
        yaml.dump(presets, f, sort_keys=False)


def get_preset(name: str) -> Dict:
    presets = load_presets()
    return presets.get(name, {})
