import streamlit as st
from pathlib import Path

st.set_page_config(page_title="GRAIL Roadmap", layout="wide")
st.title("🗺️ GRAIL Project Roadmap")

roadmap_file = (Path(__file__).resolve().parents[1] / "ROADMAP.md")

if roadmap_file.exists():
    with open(roadmap_file, "r") as f:
        roadmap_md = f.read()
    st.markdown(roadmap_md)
else:
    st.warning("ROADMAP.md not found. Please generate it.")
