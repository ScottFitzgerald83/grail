def run():
    import streamlit as st

    st.title("📘 GRAIL Glossary")

    st.markdown(
        """
    Welcome to the GRAIL glossary. Here you'll find definitions for the key concepts and controls used throughout the application.

    ---

    ### 🔁 Preset
    A saved configuration of model, attention, sampling, and generation parameters.

    ### 🧠 Entropy
    A measurement of uncertainty in the model's prediction. Higher entropy means the model is less confident.

    ### 🔢 Top-k
    The number of highest probability tokens to consider during sampling. Lower values reduce randomness.

    ### 🎲 Top-p (nucleus sampling)
    The cumulative probability threshold for sampling. Only tokens whose total probability exceeds p are considered.

    ### 🔧 FFN Mode
    Determines the structure of the feedforward network layer in the transformer. Options include:
    - `standard`: default dense layer
    - `lowrank`: reduces parameters
    - `fused`: optimized ops
    - `quantized`: low precision

    ### 🧮 Precision
    The numerical precision used for computation:
    - `float32`: standard
    - `fp16`: faster, less precise
    - `int8`: smallest, fastest, lowest fidelity

    ### ⚙️ Attention Type
    Controls how tokens attend to each other:
    - `dense`: full attention matrix
    - `sparse`: limited connectivity
    - `flash`: optimized CUDA kernel

    ### ⏱️ Latency
    Total time (in ms) from prompt submission to generation completion.

    ### 📈 Entropy Plot
    A graph showing per-token entropy across the generated output. Helps detect drift, instability, or overconfidence.

    ### 📊 Token Count
    Displays how many tokens were generated and how close you are to the configured maximum.
    """
    )