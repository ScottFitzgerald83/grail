from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio, time, json
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or "http://localhost:5173"
    allow_methods=["*"],
    allow_headers=["*"]
)


def save_to_memory(model_name: str, prompt: str, output: str):
    model_key = model_name.replace(":", "_") if model_name else "local"
    memory_path = Path(f"memory/chat_{model_key}.json")
    memory_path.parent.mkdir(exist_ok=True)
    history = []
    if memory_path.exists():
        try:
            with open(memory_path, "r") as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append({"timestamp": time.time(), "prompt": prompt, "output": output})
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
        config = {k: v for k, v in data.items() if
                  k not in ["prompt", "use_public_model", "public_model_name", "stream", "message_id"]}

        # Persona support: inject system prompt if persona is set and no system_prompt provided
        persona_map = {
            "friendly": "You are a helpful, friendly assistant who explains things clearly and kindly.",
            "creative": "You are a poetic and imaginative assistant who speaks with flair and metaphor.",
            "concise": "You are a brief, precise assistant who avoids unnecessary elaboration."
        }
        if "persona" in config and config["persona"] != "none" and "system_prompt" not in config:
            config["system_prompt"] = persona_map.get(config["persona"], "")

        response_text = None if prompt.strip().lower() == "fail" else route_model(model_name, prompt, config)

        if response_text:
            save_to_memory(model_name, prompt, response_text)

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
def load_memory(model_name: str):
    model_key = model_name.replace(":", "_")
    memory_path = Path(f"memory/chat_{model_key}.json")
    if memory_path.exists():
        try:
            with open(memory_path, "r") as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to load history: {str(e)}"}
    return []


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

        model_a = config_a.get("public_model_name", "local")
        model_b = config_b.get("public_model_name", "local")

        def simulate(prompt, model, config):
            output = route_model(model, prompt, config)
            latency = len(output) * 0.5  # simulate latency in ms
            tokens = len(output.split())
            return {
                "output": output,
                "latency_ms": round(latency),
                "tokens": tokens,
                "model": model,
                "config": config
            }

        result_a = simulate(prompt, model_a, config_a)
        result_b = simulate(prompt, model_b, config_b)

        return {
            "result_a": result_a,
            "result_b": result_b,
            "prompt": prompt
        }

    except Exception as e:
        return {"error": str(e)}
