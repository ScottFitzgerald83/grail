# grail/ui/chat.py


def run():
    import streamlit as st
    import requests
    import json
    import time

    st.title("💬 Chat with GRAIL")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "run_inference" not in st.session_state:
        st.session_state.run_inference = True

    st.toggle("Enable Inference", key="run_inference")

    def submit_prompt():
        prompt = st.session_state.prompt_input.strip()
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            if st.session_state.run_inference:
                payload = {
                    "prompt": prompt,
                    "model_name": "gpt2",
                    "attention": "dense",
                    "precision": "fp16",
                    "ffn_mode": "standard",
                    "sampling": {
                        "temperature": 0.7,
                        "top_k": 50,
                        "top_p": 0.9
                    },
                    "max_tokens": 128
                }
                with st.spinner("Invoking the ghost..."):
                    res = requests.post("http://localhost:8000/infer", json=payload)
                    if res.ok:
                        out = res.json()
                        response_text = out["output"]
                        # Streaming effect
                        placeholder = st.empty()
                        displayed_text = ""
                        for char in response_text:
                            displayed_text += char
                            with placeholder.container():
                                st.chat_message("assistant").markdown(displayed_text)
                            time.sleep(0.02)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": "⚠️ Error from model API."})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "💬 Okay. Message received."})
            st.session_state.prompt_input = ""  # clear input

    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Persistent chat input
    st.text_input("Enter your message", key="prompt_input", on_change=submit_prompt)
