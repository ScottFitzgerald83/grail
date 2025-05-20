# grail/config/settings.py

from typing import Dict

DEFAULT_CONFIG = {
    "model_name": "gpt2",
    "attention": "dense",         # dense, sparse, flash, local, hybrid
    "precision": "fp16",          # float32, fp16, int8, bf16
    "ffn_mode": "standard",       # standard, lowrank, fused, quantized
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.9,
    "device": "cuda"
}

def get_config(overrides: Dict = {}) -> Dict:
    config = DEFAULT_CONFIG.copy()
    config.update(overrides)
    return config
