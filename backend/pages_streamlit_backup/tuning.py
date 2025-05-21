import streamlit as st
from transformers import AutoTokenizer

def run():
    st.title("🎛️ Model Tuning")

    config = st.session_state.get("config", {
        "model_name": "gpt2",
        "attention": "dense",
        "precision": "fp16",
        "ffn_mode": "standard",
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
        "max_tokens": 128,
    })

    config["model_name"] = st.selectbox("Model", ["gpt2", "distilgpt2"], index=["gpt2", "distilgpt2"].index(config["model_name"]))
    config["attention"] = st.selectbox("Attention", ["dense", "sparse", "flash"], index=["dense", "sparse", "flash"].index(config["attention"]))
    config["precision"] = st.selectbox("Precision", ["float32", "fp16", "int8"], index=["float32", "fp16", "int8"].index(config["precision"]))
    config["ffn_mode"] = st.selectbox("FFN Mode", ["standard", "lowrank", "fused", "quantized"], index=["standard", "lowrank", "fused", "quantized"].index(config["ffn_mode"]))

    config["temperature"] = st.slider("Temperature", 0.0, 1.5, config["temperature"])
    config["top_k"] = st.slider("Top-k", 0, 100, config["top_k"])
    config["top_p"] = st.slider("Top-p", 0.0, 1.0, config["top_p"])
    config["max_tokens"] = st.slider("Max Tokens", 16, 2048, config["max_tokens"])

    tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
    prompt_sample = st.text_area("Prompt Preview", value="Explain quantum physics like I'm five.")
    prompt_length = len(tokenizer.encode(prompt_sample))

    used_pct = prompt_length / config["max_tokens"]
    st.caption(f"🧮 Tokens: {prompt_length} used / {config['max_tokens']} total ({used_pct:.0%})")
    st.progress(min(used_pct, 1.0))
    if used_pct > 0.9:
        st.warning("⚠️ You’re nearing the model’s token limit.")

    st.session_state["config"] = config

    st.button("💾 Save Preset")
