# grail/ui/chat.py


def run():
    import streamlit as st
    import requests
    import json
    from grail.eval.metrics import plot_token_entropy

    st.title("💬 Chat with GRAIL")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.container():
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.text_area("Enter your prompt:", height=150, key="input")

        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.experimental_rerun()

        with st.expander("Advanced Settings (Optional)", expanded=False):
            model_name = st.selectbox("Model", ["gpt2", "distilgpt2"])
            attention = st.selectbox("Attention Type", ["dense", "sparse", "flash"])
            precision = st.selectbox("Precision", ["float32", "fp16", "int8"])
            ffn_mode = st.selectbox("FFN Mode", ["standard", "lowrank", "fused", "quantized"])
            temperature = st.slider("Temperature", 0.0, 1.5, 0.7)
            top_k = st.slider("Top-k", 0, 100, 50)
            top_p = st.slider("Top-p", 0.0, 1.0, 0.9)
            max_tokens = st.slider("Max Tokens", 16, 2048, 128)

            sampling = {
                "temperature": temperature,
                "top_k": top_k,
                "top_p": top_p
            }

        if st.button("Run Inference") and prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})

            payload = {
                "prompt": prompt,
                "model_name": model_name,
                "attention": attention,
                "precision": precision,
                "ffn_mode": ffn_mode,
                "sampling": sampling,
                "max_tokens": max_tokens
            }

            with st.spinner("Invoking the ghost..."):
                res = requests.post("http://localhost:8000/infer", json=payload)
                if res.ok:
                    out = res.json()
                    response_text = out["output"]
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

                    st.subheader("🧠 Response")
                    st.write(response_text)

                    st.subheader("📊 Metrics")
                    st.json(out["metrics"])

                    if "tokens_generated" in out["metrics"]:
                        used = out["metrics"]["tokens_generated"]
                        max_tok = payload.get("max_tokens", 128)
                        pct = min(used / max_tok, 1.0)
                        st.caption(f"🧮 Tokens generated: {used} / {max_tok}")
                        st.progress(pct, text=f"{int(pct * 100)}% of configured max")
                    else:
                        st.caption("⚠️ Token count not available.")

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
