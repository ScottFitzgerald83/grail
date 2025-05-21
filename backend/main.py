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
        config = {k: v for k, v in data.items() if k not in ["prompt", "use_public_model", "public_model_name", "stream", "message_id"]}

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

@app.get("/")
def healthcheck():
    return {"status": "FastAPI is running"}
