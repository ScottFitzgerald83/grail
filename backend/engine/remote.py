from transformers import GPT2TokenizerFast
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
import json

import time
import requests


def estimate_tokens(text):
    return len(tokenizer.encode(text))

def model_router(prompt, config):
    """Entry point to route inference to a remote model if public mode is enabled."""
    model_name = config.get("public_model_name", "gpt-4")
    try:
        if config.get("stream", "false") == "true":
            return stream_public_model(model_name, prompt, config)
        if model_name.startswith("gpt-"):
            return run_openai(model_name, prompt, config)
        elif model_name.startswith("ollama:"):
            return run_ollama(model_name, prompt, config)
        else:
            return {"output": f"⚠️ Unsupported model: {model_name}", "model": model_name, "fallback_used": False}
    except Exception as e:
        fallback = config.get("fallback_model")
        if fallback and fallback != model_name:
            print(f"[GRAIL] Primary model failed, attempting fallback: {fallback}")
            config["public_model_name"] = fallback
            fallback_response = model_router(prompt, config)
            fallback_response["fallback_used"] = True
            fallback_response["fallback_model"] = fallback
            return fallback_response
        return {"output": f"⚠️ Model error and no fallback: {e}", "model": model_name, "fallback_used": False}

def run_openai(model_name, prompt, config):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.get('openai_api_key') or 'sk-REPLACE'}",
        "Content-Type": "application/json"
    }
    body = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": float(config.get("temperature", 0.7)),
        "top_p": float(config.get("top_p", 0.9)),
        "max_tokens": int(config.get("max_tokens", 256)),
        "presence_penalty": float(config.get("presence_penalty", 0.0)),
        "frequency_penalty": float(config.get("frequency_penalty", 0.0)),
        "stream": config.get("stream", "false") == "true"
    }
    estimated_tokens = estimate_tokens(prompt)
    print(f"[GRAIL] Estimated OpenAI input tokens: {estimated_tokens}")
    start = time.time()
    try:
        res = requests.post(url, headers=headers, json=body)
        delta = int((time.time() - start) * 1000)
        out = res.json()
        result = summarize_result(out["choices"][0]["message"]["content"], model_name, config, delta, out.get("usage", {}).get("total_tokens", 0))
        result["fallback_used"] = False
        return result
    except Exception as e:
        return {"output": f"⚠️ OpenAI error: {e}", "model": model_name, "fallback_used": False}

def run_ollama(model_name, prompt, config):
    model = model_name.split(":", 1)[1]
    url = f"http://localhost:11434/api/generate"
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": float(config.get("temperature", 0.7)),
            "top_p": float(config.get("top_p", 0.9)),
            "num_predict": int(config.get("max_tokens", 256))
        }
    }
    estimated_tokens = estimate_tokens(prompt)
    print(f"[GRAIL] Estimated Ollama input tokens: {estimated_tokens}")
    start = time.time()
    try:
        res = requests.post(url, json=body)
        delta = int((time.time() - start) * 1000)
        out = res.json()
        result = summarize_result(out.get("response", ""), model_name, config, delta, out.get("eval_count", len(out.get("response", "").split())))
        result["fallback_used"] = False
        return result
    except Exception as e:
        return {"output": f"⚠️ Ollama error: {e}", "model": model_name, "fallback_used": False}
import aiohttp
import asyncio

async def stream_public_model(model_name: str, prompt: str, config: dict):
    """Stream OpenAI-compatible model output character by character."""
    if model_name.startswith("gpt-"):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.get('openai_api_key') or 'sk-REPLACE'}",
            "Content-Type": "application/json"
        }
        body = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": float(config.get("temperature", 0.7)),
            "top_p": float(config.get("top_p", 0.9)),
            "presence_penalty": float(config.get("presence_penalty", 0.0)),
            "frequency_penalty": float(config.get("frequency_penalty", 0.0)),
            "stream": True
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=body) as resp:
                async for line in resp.content:
                    if line.startswith(b'data:'):
                        try:
                            json_str = line.decode().split("data: ")[1].strip()
                            if json_str == "[DONE]":
                                break
                            delta = json.loads(json_str)["choices"][0]["delta"]
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except Exception:
                            continue
        yield f"\n[GRAIL_END] model={model_name} tokens=?"

def summarize_result(raw, model_name, config, delta, token_est):
    return {
        "output": raw,
        "tokens": token_est,
        "latency_ms": delta,
        "model": model_name,
        "config": config,
        "fallback_used": False
    }