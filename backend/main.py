from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, PlainTextResponse
import asyncio, time, json
from pathlib import Path
from backend.engine.model import load_model, run_inference
from backend.engine.remote import model_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or "http://localhost:5173"
    allow_methods=["*"],
    allow_headers=["*"]
)


def save_to_memory(model_name: str, prompt: str, output: str, metadata: dict = None):
    model_key = model_name.replace(":", "_") if model_name else "local"
    memory_path = Path(f"memory/chat_{model_key}.json")
    memory_path.parent.mkdir(exist_ok=True)

    history = []
    if memory_path.exists():
        try:
            with open(memory_path, "r") as f:
                history = json.load(f)
                if not isinstance(history, list):
                    history = []
        except Exception:
            history = []

    # Truncate old messages if configured
    limit = metadata.get("truncate_prompt") if metadata else 0
    if limit and isinstance(limit, int) and limit > 0:
        def token_len(x): return len(x["prompt"].split()) + len(x["output"].split())
        total = 0
        new_history = []
        for msg in reversed(history):
            total += token_len(msg)
            if total > limit:
                break
            new_history.insert(0, msg)
        history = new_history

    entry = {
        "timestamp": time.time(),
        "prompt": prompt,
        "output": output,
        "model": model_name,
    }
    if metadata:
        entry.update(metadata)

    history.append(entry)

    with open(memory_path, "w") as f:
        json.dump(history, f, indent=2)


def route_model(model_name: str, prompt: str, config: dict) -> str:
    if model_name.startswith("ollama:"):
        return f"(Ollama reply from {model_name} to '{prompt}')"
    elif model_name.startswith("gpt"):
        return f"(OpenAI reply from {model_name} to '{prompt}')"
    elif model_name == "mixtral":
        return f"(Mixtral reply to '{prompt}')"
    else:
        return f"(Local model reply to '{prompt}')"


@app.post("/infer")
async def infer(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        message_id = data.get("message_id", str(time.time()))
        if not prompt:
            return {"output": None, "error": "Empty prompt received."}
        stream = data.get("stream") == "true"
        model_name = data.get("public_model_name") if data.get("use_public_model") == "true" else "local"

        # Validate API key if public model is selected
        if model_name != "local" and not data.get("openai_api_key"):
            return {"output": None, "error": "Missing OpenAI API key"}
        config = {k: v for k, v in data.items() if
                  k not in ["prompt", "use_public_model", "public_model_name", "stream", "message_id"]}
        config["openai_api_key"] = data.get("openai_api_key", "")

        # Persona support: inject system prompt if persona is set and no system_prompt provided
        persona_map = {
            "friendly": "You are a helpful, friendly assistant who explains things clearly and kindly.",
            "creative": "You are a poetic and imaginative assistant who speaks with flair and metaphor.",
            "concise": "You are a brief, precise assistant who avoids unnecessary elaboration."
        }
        if "persona" in config and config["persona"] != "none" and "system_prompt" not in config:
            config["system_prompt"] = persona_map.get(config["persona"], "")

        if model_name != "local":
            from backend.engine.remote import stream_public_model
            if stream:
                return StreamingResponse(stream_public_model(model_name, prompt, config), media_type="text/plain")
            else:
                response_text = route_model(model_name, prompt, config)
        else:
            response_text = route_model(model_name, prompt, config)

        if response_text:
            token_count = len(response_text.split()) if response_text else 0
            save_to_memory(model_name, prompt, response_text, {
                "tokens": token_count,
                "cost_estimate": round(token_count * 0.00002, 4),
                "config": config
            })

        if stream and response_text is not None:
            async def token_stream():
                for char in response_text:
                    yield char
                    await asyncio.sleep(0.01)
            return StreamingResponse(token_stream(), media_type="text/plain")

        return {
            "output": response_text,
            "config": config,
            "message_id": message_id,
            "retryable": response_text is None
        }
    except Exception as e:
        return {"output": None, "error": str(e)}


@app.get("/memory/{model_name}")
def load_memory(model_name: str, format: str = "json"):
    model_key = model_name.replace(":", "_")
    memory_path = Path(f"memory/chat_{model_key}.json")
    if memory_path.exists():
        try:
            with open(memory_path, "r") as f:
                history = json.load(f)
            if format == "txt":
                lines = []
                for item in history:
                    lines.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['timestamp']))}]")
                    lines.append(f"User: {item['prompt']}")
                    lines.append(f"Assistant: {item['output']}\n")
                return PlainTextResponse("\n".join(lines))
            return JSONResponse(content=history)
        except Exception as e:
            return {"error": f"Failed to load history: {str(e)}"}
    return JSONResponse(content=[])


@app.patch("/memory/{model_name}")
async def edit_memory(model_name: str, request: Request):
    try:
        model_key = model_name.replace(":", "_")
        memory_path = Path(f"memory/chat_{model_key}.json")
        data = await request.json()
        message_id = data.get("message_id")
        new_prompt = data.get("new_prompt", "")
        config = data.get("config", {})

        if not message_id or not new_prompt:
            return {"error": "Missing message_id or new_prompt"}

        if not memory_path.exists():
            return {"error": "No history found for model"}

        with open(memory_path, "r") as f:
            history = json.load(f)

        found = False
        for msg in history:
            if str(msg.get("timestamp")) == str(message_id):
                msg["prompt"] = new_prompt
                msg["output"] = route_model(model_name, new_prompt, config)
                found = True
                break

        if not found:
            return {"error": "Message not found"}

        with open(memory_path, "w") as f:
            json.dump(history, f, indent=2)

        return {"status": "updated", "message_id": message_id}
    except Exception as e:
        return {"error": str(e)}


@app.delete("/memory/{model_name}/{message_id}")
def delete_message(model_name: str, message_id: str):
    model_key = model_name.replace(":", "_")
    memory_path = Path(f"memory/chat_{model_key}.json")
    if not memory_path.exists():
        return {"error": "No history for model"}

    try:
        with open(memory_path, "r") as f:
            history = json.load(f)

        new_history = [msg for msg in history if str(msg.get("timestamp")) != str(message_id)]

        with open(memory_path, "w") as f:
            json.dump(new_history, f, indent=2)

        return {"status": "deleted", "message_id": message_id}
    except Exception as e:
        return {"error": str(e)}


@app.get("/")
def healthcheck():
    return {"status": "FastAPI is running"}


@app.post("/compare")
async def compare(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        config_a = data.get("config_a", {})
        config_b = data.get("config_b", {})

        def invoke(config):
            if config.get("use_public_model") == "true":
                return model_router(prompt, config)
            else:
                model = load_model(config)
                return run_inference(model, prompt, config)

        result_a = invoke(config_a)
        result_b = invoke(config_b)

        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"{result_a['model']}_vs_{result_b['model']}_{timestamp}.json"

        return {
            "result_a": result_a,
            "result_b": result_b,
            "prompt": prompt,
            "filename": filename
        }

    except Exception as e:
        return {"error": str(e)}

@app.post("/compare/batch")
async def compare_batch(request: Request):
    try:
        data = await request.json()
        prompts = data.get("prompts", [])
        config_a = data.get("config_a", {})
        config_b = data.get("config_b", {})

        def invoke(p, config):
            if config.get("use_public_model") == "true":
                return model_router(p, config)
            else:
                model = load_model(config)
                return run_inference(model, p, config)

        results = []
        for p in prompts:
            result_a = invoke(p, config_a)
            result_b = invoke(p, config_b)
            results.append({
                "prompt": p,
                "result_a": result_a,
                "result_b": result_b
            })

        if results:
            m1 = results[0]["result_a"]["model"]
            m2 = results[0]["result_b"]["model"]
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"{m1}_vs_{m2}_{timestamp}.json"
        else:
            filename = "compare_batch_result.json"

        return {"results": results, "filename": filename}
    except Exception as e:
        return {"error": str(e)}