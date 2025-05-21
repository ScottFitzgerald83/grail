from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access (adjust origin in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic test route
@app.get("/")
def read_root():
    return {"message": "Hello from the backend"}

# Chat inference endpoint
@app.post("/infer")
async def infer(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    return {"output": f"Echo: {prompt}"}