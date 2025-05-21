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
    prompt = data.get("prompt", "")
    return {"output": f"Echo: {prompt}"}
@app.get("/")
def healthcheck():
    return {"status": "FastAPI is running"}
