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
@app.get("/infer")
async def catch_get():
    print("⚠️ Received unexpected GET /infer")
    return {"error": "GET not allowed. Use POST."}