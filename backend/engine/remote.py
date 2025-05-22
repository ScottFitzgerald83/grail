

import time
import requests

def run_remote_inference(model_name, prompt, config):
    """Route to a hosted model API and return a GRAIL-compatible response dict."""
    if model_name.startswith("gpt-"):
        return run_openai(model_name, prompt, config)
    elif model_name.startswith("ollama:"):
        return run_ollama(model_name, prompt, config)
    else:
        return {"output": f"⚠️ Unsupported model: {model_name}"}

def run_openai(model_name, prompt, config):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.get('openai_api_key') or 'sk-REPLACE'}",
        "Content-Type": "application/json"
    }
    body = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": config.get("temperature", 0.7),
        "top_p": config.get("top_p", 0.9),
        "max_tokens": config.get("max_tokens", 256),
        "presence_penalty": config.get("presence_penalty", 0.0),
        "frequency_penalty": config.get("frequency_penalty", 0.0)
    }
    start = time.time()
    res = requests.post(url, headers=headers, json=body)
    delta = int((time.time() - start) * 1000)
    try:
        out = res.json()
        return {
            "output": out["choices"][0]["message"]["content"],
            "tokens": out["usage"]["total_tokens"],
            "latency_ms": delta,
            "model": model_name,
            "config": config
        }
    except Exception as e:
        return {"output": f"⚠️ OpenAI error: {e}", "model": model_name}

def run_ollama(model_name, prompt, config):
    model = model_name.split(":", 1)[1]
    url = f"http://localhost:11434/api/generate"
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": config.get("temperature", 0.7),
            "top_p": config.get("top_p", 0.9),
            "num_predict": config.get("max_tokens", 256)
        }
    }
    start = time.time()
    res = requests.post(url, json=body)
    delta = int((time.time() - start) * 1000)
    try:
        out = res.json()
        return {
            "output": out["response"],
            "tokens": out.get("eval_count", len(out["response"].split())),
            "latency_ms": delta,
            "model": model_name,
            "config": config
        }
    except Exception as e:
        return {"output": f"⚠️ Ollama error: {e}", "model": model_name}