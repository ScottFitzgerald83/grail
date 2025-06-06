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
    prompt = config.get("prompt", "")

    if model_name.startswith("gpt-"):
        return {
            "model": model_name,
            "messages": (
                ([{"role": "system", "content": config.get("system_prompt", "")}] if config.get("system_prompt") else [])
                + [{"role": "user", "content": prompt}]
            ),
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
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": config.get("temperature", 0.7),
                "top_p": config.get("top_p", 0.9),
                "num_predict": config.get("max_tokens", 256)
            }
        }

    else:
        return {
            "model": model_name,
            "input": prompt,
            "generation_params": {
                "max_tokens": config.get("max_tokens", 256),
                "temperature": config.get("temperature", 0.7),
                "top_k": config.get("top_k", 50),
                "top_p": config.get("top_p", 0.9),
                "presence_penalty": config.get("presence_penalty", 0.0),
                "frequency_penalty": config.get("frequency_penalty", 0.0),
                "stop": config.get("stop_sequence", None),
                "stream": config.get("stream", "false") == "true"
            },
            "metadata": {
                "system_prompt": config.get("system_prompt", "")
            }
        }


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


# Validate GRAIL config schema for runtime use
def validate_config_schema(cfg: Dict):
    if not isinstance(cfg, dict):
        raise ValueError("Configuration must be a dictionary.")

    required_keys = ["prompt", "temperature", "top_p", "max_tokens"]
    for key in required_keys:
        if key not in cfg:
            raise ValueError(f"Missing required key: '{key}'")

    if not isinstance(cfg["prompt"], str):
        raise TypeError("Prompt must be a string.")
    if not isinstance(cfg["temperature"], (float, int)):
        raise TypeError("Temperature must be a number.")
    if not isinstance(cfg["top_p"], (float, int)):
        raise TypeError("Top-p must be a number.")
    if not isinstance(cfg["max_tokens"], int):
        raise TypeError("Max tokens must be an integer.")
