from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or "http://localhost:5173"
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/infer")
async def infer(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    config = {k: v for k, v in data.items() if k != "prompt"}
    output = f"(Simulated response) Prompt: {prompt} | Config: {config}"
    return {"output": output}
@app.get("/")
def healthcheck():
    return {"status": "FastAPI is running"}
