# Main.py

import streamlit as st
from grail.pages.chat import run as chat_run
from grail.pages.compare import run as compare_run
from grail.pages.roadmap import run as roadmap_run
from grail.pages.glossary import run as glossary_run

st.set_page_config(
    page_title="GRAIL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean layout without suppressing sidebar (fully enabled now)

# Replace sidebar with horizontal tabs
tabs = st.tabs(["Home", "Chat", "Compare", "Roadmap", "Glossary"])

with tabs[0]:
    st.title("🧠 GRAIL — Ghost-Refined Architecture for Interpretable Language")
    st.markdown(
        """
        Welcome to **GRAIL**, a live transformer sandbox for:

        - 💬 Model exploration and chat
        - 🔁 Architecture and config comparison
        - 🗺️ Roadmap tracking and glossary insight

        Use the tabs above to explore, tune, and measure transformer behavior.
        """
    )

with tabs[1]:
    chat_run()

with tabs[2]:
    compare_run()

with tabs[3]:
    roadmap_run()

with tabs[4]:
    glossary_run()