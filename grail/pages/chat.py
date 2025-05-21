from pathlib import Path
import json

def run():
    import streamlit as st
    import requests
    import json
    import time

    st.title("💬 Chat with GRAIL")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        memory_path = Path("memory.json")

        if memory_path.exists():
            with open(memory_path, "r") as f:
                try:
                    st.session_state.messages = json.load(f)
                except json.JSONDecodeError:
                    st.session_state.messages = []
    else:
        memory_path = Path("memory.json")

    if "run_inference" not in st.session_state:
        st.session_state.run_inference = False
    if "prompt_input" not in st.session_state:
        st.session_state.prompt_input = ""

    st.toggle("Enable Inference", key="run_inference")

    # Prompt template selectbox above chat input
    prompt_templates = {
        "Select a prompt template...": "",
        "Summarize this text": "Summarize this text",
        "Explain like I'm five": "Explain like I'm five",
        "Translate into pirate speak": "Translate into pirate speak",
        "Give a haiku": "Give a haiku"
    }

    # Always-visible prompt template selectbox
    st.selectbox(
        "Choose a template...",
        list(prompt_templates.keys()),
        index=0,
        key="prompt_template_select"
    )

    # Immediately apply template to input
    template_key = st.session_state.prompt_template_select
    if template_key != "Select a prompt template...":
        st.session_state.prompt_input = prompt_templates[template_key]

    def submit_prompt():
        prompt = st.session_state.prompt_input.strip()
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with open(memory_path, "w") as f:
                json.dump(st.session_state.messages, f, indent=2)
            if st.session_state.run_inference:
                payload = st.session_state.get("config", {}).copy()
                payload["prompt"] = prompt
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
                        with open(memory_path, "w") as f:
                            json.dump(st.session_state.messages, f, indent=2)
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": "⚠️ Error from model API."})
                        with open(memory_path, "w") as f:
                            json.dump(st.session_state.messages, f, indent=2)
            else:
                st.session_state.messages.append({"role": "assistant", "content": "💬 Okay. Message received."})
                with open(memory_path, "w") as f:
                    json.dump(st.session_state.messages, f, indent=2)
            st.session_state.prompt_input = ""  # clear input

    # Chat input
    st.text_input("Enter your message", key="prompt_input", value=st.session_state.prompt_input, on_change=submit_prompt)

    if st.button("🧹 Clear Memory"):
        st.session_state.messages = []
        if memory_path.exists():
            memory_path.unlink()

    # Display messages with custom styles and headers
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            with st.container():
                st.markdown(f"**🧍‍♂️ You said:**")
                st.markdown(
                    f"<div style='background-color:#f0f2f6; padding:10px; border-radius:8px; text-align:right; max-width:70%; margin-left:auto;'>{message['content']}</div>",
                    unsafe_allow_html=True
                )
        else:
            with st.container():
                st.markdown(f"**🤖 GRAIL replied:**")
                st.markdown(
                    f"<div style='margin-left:20px; padding:5px;'>{message['content']}</div>",
                    unsafe_allow_html=True
                )
        if i < len(st.session_state.messages) - 1:
            st.markdown("<hr style='opacity:0.1'>", unsafe_allow_html=True)

    # Ensure directory exists
    Path("memories").mkdir(exist_ok=True)

    # Save chat to timestamped file
    if st.button("💾 Save Chat"):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        memory_file = Path(f"memories/chat_{timestamp}.json")
        with open(memory_file, "w") as f:
            json.dump(st.session_state.messages, f, indent=2)
        st.success(f"Chat saved as {memory_file.name}")

    # Load saved memory
    uploaded = st.file_uploader("📂 Load a saved chat", type=["json"])
    if uploaded:
        try:
            loaded = json.load(uploaded)
            if isinstance(loaded, list):
                st.session_state.messages = loaded
                st.success("Memory loaded.")
            else:
                st.error("Invalid file format.")
        except Exception as e:
            st.error(f"Error loading file: {e}")
