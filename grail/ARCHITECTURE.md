# Project: GRAIL

**Ghost-Refined Architecture for Interpretable Language**

A sacred tool of systems insight and model clarity. Tune transformer internals. Watch them think. Ask the right questions, and GRAIL will answer.

---

## Core Architecture Overview

### 1. **Frontend Interface** (`/ui`)

| Component            | Description                                                   |
|----------------------|---------------------------------------------------------------|
| Chat Panel           | Send messages, receive model replies                          |
| Settings Panel       | Sliders + dropdowns for attention type, FFN config, precision |
| Live Charts          | Latency, token entropy, softmax sharpness                     |
| Attention Visualizer | Optional per-layer heatmaps                                   |

### 2. **Backend Engine** (`/engine`)

| Module           | Purpose                                                  |
|------------------|----------------------------------------------------------|
| Model Manager    | Load models (GPT2, Mistral, LLaMA) with config overrides |
| Token Pipeline   | Tokenize input, manage rolling context window            |
| Dial Dispatcher  | Apply user config: attention type, FFN, quantization     |
| Inference Core   | Run model, collect timing + profiling metrics            |
| Result Formatter | Return full trace, stats, and final output text          |

### 3. **Evaluator & Profiler** (`/eval`)

| Tool              | Purpose                                            |
|-------------------|----------------------------------------------------|
| Latency Tracker   | Time per token, per layer, per component           |
| Quality Hooks     | Entropy, repetition rate, softmax spread           |
| Attention Tracer  | Log which tokens attend to which, and how strongly |
| Config Comparator | Run identical prompt across configs (A/B)          |

### 4. **Model Config System** (`/config`)

| Feature           | Description                                 |
|-------------------|---------------------------------------------|
| Attention Options | Dense, Sparse, Flash, Local, Global, Hybrid |
| FFN Modes         | Standard, Low-Rank, Fused, Quantized        |
| Precision         | Float32, FP16, BF16, INT8                   |
| Sampling          | Temperature, Top-K, Top-P controls          |

### 5. **Deployment Options**

- Local with GPU (e.g., RTX, A100)
- Web-hosted with gradio/streamlit frontend + Flask/FastAPI backend
- Cloud-native with Triton or HuggingFace Inference Endpoints

---

## Directory Structure

```
grail/
├── ui/                   # Streamlit/Dash/React interface
├── engine/               # Token, model, and config logic
├── eval/                 # Profiling, metrics, attention tracer
├── config/               # Tunable model settings
├── models/               # Custom weights, adapters, configs
└── app.py                # Main app entrypoint
```

---

Let me know when you're ready for file stubs or a component-by-component plan.
