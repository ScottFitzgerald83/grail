from fastapi import FastAPI
from pydantic import BaseModel
from grail.engine.model import load_model, run_inference
from grail.config.settings import get_config
from grail.eval.profiler import profile_run
import math

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
    max_new_tokens: int = 128


@app.on_event("startup")
async def startup_event():
    global config, model
    config = get_config()
    model = load_model(config)


@app.post("/infer")
async def infer(req: InferenceRequest):
    print("[GRAIL] Received inference request...")
    output, trace, start_time, end_time = run_inference(model, req.prompt, req)
    print("[GRAIL] Inference complete. Profiling...")

    metrics = profile_run(trace, start_time, end_time)
    print("[GRAIL] Raw metrics:", metrics)

    safe_metrics = {}
    for key, value in metrics.items():
        try:
            if isinstance(value, float):
                if math.isfinite(value):
                    safe_metrics[key] = round(value, 4)
                else:
                    print(f"[GRAIL] Skipping non-finite float metric: {key} = {value}")
            elif isinstance(value, int):
                safe_metrics[key] = value
            else:
                print(f"[GRAIL] Skipping non-numeric metric: {key} = {value}")
        except Exception as e:
            print(f"[GRAIL] Error sanitizing metric '{key}': {e}")

    print("[GRAIL] Final safe metrics:", safe_metrics)

    return {
        "output": output,
        "metrics": safe_metrics,
        "trace": None
    }
