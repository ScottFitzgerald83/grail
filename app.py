from fastapi import FastAPI
from pydantic import BaseModel
from engine.model import load_model, run_inference
from config.settings import get_config
from eval.profiler import profile_run

app = FastAPI(title="GRAIL: Ghost-Refined Architecture for Interpretable Language")

# Global model and config
model = None
config = None


class InferenceRequest(BaseModel):
    prompt: str
    attention: str = "dense"
    precision: str = "fp16"
    ffn_mode: str = "standard"
    sampling: dict = {}


@app.on_event("startup")
async def startup_event():
    global config, model
    config = get_config()
    model = load_model(config)


@app.post("/infer")
async def infer(req: InferenceRequest):
    output, trace, start_time, end_time = run_inference(model, req.prompt, req)
    metrics = profile_run(trace, start_time, end_time)
    return {
        "output": output,
        "metrics": metrics,
        "trace": trace
    }
