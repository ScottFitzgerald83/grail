import streamlit as st

st.set_page_config(page_title="GRAIL", layout="wide")
st.title("🧠 GRAIL — Ghost-Refined Architecture for Interpretable Language")

st.markdown(
    """
    Welcome to **GRAIL**, your live transformer sandbox for:
    - 💬 Model exploration and chat
    - 🔁 Architecture and config comparison
    - 🗺️ Roadmap tracking and project evolution

    Use the sidebar to navigate GRAIL's capabilities.

    ---
    **Current model:** GPT-2  
    **Max tokens:** 2048  
    **Presets loaded:** Yes  
    **Entropy visualizer:** Active  
    """
)

with st.expander("📖 What is GRAIL?"):
    st.markdown(
        """
        GRAIL is an interpretability-focused interface for LLM tuning, benchmarking, and architectural experimentation.
        It's not just for using models — it's for *understanding them*.

        - Change attention types (dense/sparse/flash)
        - Adjust FFNs, precision, temperature
        - Compare outputs side-by-side
        - Visualize entropy over time
        """
    )