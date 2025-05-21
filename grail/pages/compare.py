def run():
    import streamlit as st
    import torch
    from grail.engine.model import run_inference, load_model
    from grail.eval.profiler import profile_run
    from grail.eval.metrics import plot_token_entropy
    from grail.config.settings import load_presets
    import json
    from datetime import datetime

    st.title("🔁 Compare Configurations Side by Side")

    presets = load_presets()
    preset_names = list(presets.keys())

    # Move preset selectors to main layout instead of sidebar
    st.markdown("### Choose Presets")
    col1, col2 = st.columns(2)

    with col1:
        config_a_name = st.selectbox("🔧 Preset A", preset_names, key="preset_a")
        config_a = presets[config_a_name]
    with col2:
        config_b_name = st.selectbox("🧪 Preset B", preset_names, key="preset_b")
        config_b = presets[config_b_name]

    prompt = st.text_area("Prompt", "What is the purpose of GRAIL?", height=100)

    # Initialize variables for outputs and metrics
    out_a = out_b = metrics_a = metrics_b = None
    trace_a = trace_b = None

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
            st.subheader("📊 Metrics")
            st.json(metrics_a)
            if "tokens_generated" in metrics_a:
                used = metrics_a["tokens_generated"]
                max_tok = config_a.get("max_tokens", 2048)
                pct = min(used / max_tok, 1.0)
                st.caption(f"🧮 Tokens generated: {used} / {max_tok}")
                st.progress(pct, text=f"{int(pct * 100)}% of configured max")
            else:
                st.caption("⚠️ Token count not available.")
            st.subheader("📈 Entropy (A)")
            if hasattr(trace_a, "scores") and trace_a.scores:
                scores_a = [torch.tensor(s) for s in trace_a.scores]
                fig_a = plot_token_entropy(scores_a)
                if fig_a:
                    st.pyplot(fig_a)

        with col2:
            st.subheader(f"🧪 Output from {config_b_name}")
            st.write(out_b)
            st.subheader("📊 Metrics")
            st.json(metrics_b)
            if "tokens_generated" in metrics_b:
                used = metrics_b["tokens_generated"]
                max_tok = config_b.get("max_tokens", 2048)
                pct = min(used / max_tok, 1.0)
                st.caption(f"🧮 Tokens generated: {used} / {max_tok}")
                st.progress(pct, text=f"{int(pct * 100)}% of configured max")
            else:
                st.caption("⚠️ Token count not available.")
            st.subheader("📈 Entropy (B)")
            if hasattr(trace_b, "scores") and trace_b.scores:
                scores_b = [torch.tensor(s) for s in trace_b.scores]
                fig_b = plot_token_entropy(scores_b)
                if fig_b:
                    st.pyplot(fig_b)

    # Only allow saving if outputs and metrics are available
    if st.button("💾 Save Comparison Result"):
        if all(x is not None for x in [prompt, config_a_name, config_b_name, out_a, out_b, metrics_a, metrics_b]):
            result = {
                "prompt": prompt,
                "config_a_name": config_a_name,
                "config_b_name": config_b_name,
                "output_a": out_a,
                "output_b": out_b,
                "metrics_a": metrics_a,
                "metrics_b": metrics_b
            }
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"grail_comparison_{timestamp}.json"
            with open(filename, "w") as f:
                json.dump(result, f, indent=2)
            st.success(f"Saved to {filename}")
        else:
            st.warning("Please run a comparison first before saving.")
