# grail/ui/chat.py

import streamlit as st
import requests
import json

st.set_page_config(page_title="GRAIL", layout="wide")
st.title("🧪 GRAIL — Ghost-Refined Architecture for Interpretable Language")

# Sidebar: Configuration
st.sidebar.header("Dial Settings")
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
        "attention": attention,
        "precision": precision,
        "ffn_mode": ffn_mode,
        "sampling": {
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }
    }
    with st.spinner("Invoking the ghost..."):
        res = requests.post("http://localhost:8000/infer", json=payload)
        if res.ok:
            out = res.json()
            st.subheader("🧠 Response")
            st.write(out["output"])

            st.subheader("📊 Metrics")
            st.json(out["metrics"])
        else:
            st.error("Model failed to respond.")
