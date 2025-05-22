def is_valid_openai_key(key: str) -> bool:
    """Basic check for OpenAI key format."""
    return isinstance(key, str) and key.startswith("sk-") and len(key) > 30

def is_valid_ollama_key(key: str) -> bool:
    return True  # Placeholder for future validation

def is_valid_anthropic_key(key: str) -> bool:
    return key.startswith("cla-") if key else False
