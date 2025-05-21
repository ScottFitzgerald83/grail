def run():
    import streamlit as st
    from pathlib import Path

    st.title("🗺️ GRAIL Project Roadmap")

    # Inject CSS to hide sidebar and adjust padding on roadmap view

    roadmap_file = (Path(__file__).resolve().parents[2] / "ROADMAP.md")

    if roadmap_file.exists():
        with open(roadmap_file, "r") as f:
            roadmap_md = f.read()
        st.markdown(roadmap_md)
    else:
        st.warning("ROADMAP.md not found. Please generate it.")
