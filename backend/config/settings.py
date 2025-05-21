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
