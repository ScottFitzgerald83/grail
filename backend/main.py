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

@app.post("/infer")
async def infer(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        stream = data.get("stream") == "true"
        model_name = data.get("public_model_name") if data.get("use_public_model") == "true" else "local"
        config = {k: v for k, v in data.items() if k not in ["prompt", "use_public_model", "public_model_name", "stream"]}

        response_text = f"(Simulated response to '{prompt}' using model '{model_name}')"

        save_to_memory(model_name, prompt, response_text)

        if stream:
            async def token_stream():
                for char in response_text:
                    yield char
                    await asyncio.sleep(0.01)
            return StreamingResponse(token_stream(), media_type="text/plain")

        return {"output": response_text, "config": config}
    except Exception as e:
        return {"output": None, "error": str(e)}

@app.get("/")
def healthcheck():
    return {"status": "FastAPI is running"}
