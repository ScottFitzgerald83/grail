# grail/ui/chat.py

import streamlit as st
import requests
import json
from config.settings import load_presets, get_preset  # NEW

st.set_page_config(page_title="GRAIL", layout="wide")
st.title("🧪 GRAIL — Ghost-Refined Architecture for Interpretable Language")

# Sidebar: Presets
presets = load_presets()
preset_names = list(presets.keys())
selected_preset = st.sidebar.selectbox("Presets", ["(custom)"] + preset_names)

if selected_preset != "(custom)":
    preset_config = get_preset(selected_preset)
else:
    preset_config = {}

# Sidebar: Configuration
st.sidebar.header("Dial Settings")
attention = st.sidebar.selectbox(
    "Attention Type",
    ["dense", "sparse", "flash"],
    index=["dense", "sparse", "flash"].index(preset_config.get("attention", "dense"))
)
precision = st.sidebar.selectbox(
    "Precision",
    ["float32", "fp16", "int8"],
    index=["float32", "fp16", "int8"].index(preset_config.get("precision", "fp16"))
)
ffn_mode = st.sidebar.selectbox(
    "FFN Mode",
    ["standard", "lowrank", "fused", "quantized"],
    index=["standard", "lowrank", "fused", "quantized"].index(preset_config.get("ffn_mode", "standard"))
)
temperature = st.sidebar.slider(
    "Temperature", 0.0, 1.5, preset_config.get("temperature", 0.7)
)
top_k = st.sidebar.slider(
    "Top-k", 0, 100, preset_config.get("top_k", 50)
)
top_p = st.sidebar.slider(
    "Top-p", 0.0, 1.0, preset_config.get("top_p", 0.9)
)

# Sidebar: Save current config as preset
st.sidebar.markdown("---")
preset_name = st.sidebar.text_input("Save as new preset", value="")
if preset_name and st.sidebar.button("Save Preset"):
    from grail.config.settings import save_presets

    new_config = {
        "attention": attention,
        "precision": precision,
        "ffn_mode": ffn_mode,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "max_tokens": 2048
    }
    presets[preset_name] = new_config
    save_presets(presets)
    st.sidebar.success(f"Preset '{preset_name}' saved.")

# Chat UI
prompt = st.text_area("Prompt", height=200)
submit = st.button("Run Inference")

# Show live config payload preview
st.sidebar.markdown("---")
if st.sidebar.checkbox("Preview Active Config"):
    live_config = {
        "prompt": prompt if prompt else "<empty>",
        "attention": attention,
        "precision": precision,
        "ffn_mode": ffn_mode,
        "sampling": {
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }
    }
    st.sidebar.subheader("🔍 Active Payload")
    st.sidebar.json(live_config)

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
