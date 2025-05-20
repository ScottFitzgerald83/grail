# grail/ui/chat.py

import streamlit as st
import requests
import json
from grail.config.settings import load_presets, get_preset
from grail.eval.metrics import plot_token_entropy  # NEW


# Sidebar: Configuration
st.sidebar.header("Dial Settings")
model_name = st.sidebar.selectbox("Model", ["gpt2", "distilgpt2"])
attention = st.sidebar.selectbox("Attention Type", ["dense", "sparse", "flash"])
precision = st.sidebar.selectbox("Precision", ["float32", "fp16", "int8"])
ffn_mode = st.sidebar.selectbox("FFN Mode", ["standard", "lowrank", "fused", "quantized"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7)
top_k = st.sidebar.slider("Top-k", 0, 100, 50)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.9)

# Chat UI
prompt = st.text_area("Prompt", height=200)
submit = st.button("Run Inference")

if submit and prompt:
    payload = {
        "prompt": prompt,
        "model_name": model_name,
        "attention": attention,
        "precision": precision,
        "ffn_mode": ffn_mode,
        "sampling": {
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        },
        "max_tokens": 128
    }
    with st.spinner("Invoking the ghost..."):
        res = requests.post("http://localhost:8000/infer", json=payload)
        if res.ok:
            out = res.json()
            st.subheader("🧠 Response")
            st.write(out["output"])

            st.subheader("📊 Metrics")
            st.json(out["metrics"])

            # Display token count and usage bar if available
            if "tokens_generated" in out["metrics"]:
                max_tok = payload.get("max_tokens", 2048)
                used = out["metrics"]["tokens_generated"]
                pct = min(used / max_tok, 1.0)
                st.caption(f"🧮 Tokens generated: {used} / {max_tok}")
                st.progress(pct, text=f"{int(pct * 100)}% of configured max")

            st.subheader("📈 Token-Level Entropy")
            if "trace" in out and out["trace"] and "scores" in out["trace"]:
                import torch
                scores = [torch.tensor(s) for s in out["trace"]["scores"]]
                fig = plot_token_entropy(scores)
                if fig:
                    st.pyplot(fig)
                else:
                    st.info("No entropy trace available.")
            else:
                st.info("No entropy trace returned.")
        else:
            st.error("Model failed to respond.")
