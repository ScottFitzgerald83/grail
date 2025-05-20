import streamlit as st
import torch
from grail.engine.model import run_inference, load_model
from grail.eval.profiler import profile_run
from grail.eval.metrics import plot_token_entropy
from grail.config.settings import load_presets

st.set_page_config(page_title="GRAIL Compare", layout="wide")
st.title("🔁 GRAIL Config Comparison")

presets = load_presets()
preset_names = list(presets.keys())

col1, col2 = st.columns(2)

with col1:
    st.header("🔧 Config A")
    config_a_name = st.selectbox("Preset A", preset_names, key="preset_a")
    config_a = presets[config_a_name]
with col2:
    st.header("🧪 Config B")
    config_b_name = st.selectbox("Preset B", preset_names, key="preset_b")
    config_b = presets[config_b_name]

prompt = st.text_area("Prompt", "What is the purpose of GRAIL?", height=100)

if st.button("Compare"):
    with st.spinner("Running Config A..."):
        model_a = load_model(config_a)
        out_a, trace_a, start_a, end_a = run_inference(model_a, prompt, config_a)
        metrics_a = profile_run(trace_a, start_a, end_a)

    with st.spinner("Running Config B..."):
        model_b = load_model(config_b)
        out_b, trace_b, start_b, end_b = run_inference(model_b, prompt, config_b)
        metrics_b = profile_run(trace_b, start_b, end_b)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"🔧 Output from {config_a_name}")
        st.write(out_a)
        st.json(metrics_a)
        st.subheader("📈 Entropy (A)")
        if hasattr(trace_a, "scores") and trace_a.scores:
            scores_a = [torch.tensor(s) for s in trace_a.scores]
            fig_a = plot_token_entropy(scores_a)
            if fig_a:
                st.pyplot(fig_a)

    with col2:
        st.subheader(f"🧪 Output from {config_b_name}")
        st.write(out_b)
        st.json(metrics_b)
        st.subheader("📈 Entropy (B)")
        if hasattr(trace_b, "scores") and trace_b.scores:
            scores_b = [torch.tensor(s) for s in trace_b.scores]
            fig_b = plot_token_entropy(scores_b)
            if fig_b:
                st.pyplot(fig_b)
