export const glossaryMarkdown = [
    {
        term: "Preset",
        definition: "A saved configuration of model, attention, sampling, and generation parameters."
    },
    {
        term: "Entropy",
        definition: "A measurement of uncertainty in the model's prediction. Higher entropy means the model is less confident."
    },
    {
        term: "Top-k",
        definition: "The number of highest probability tokens to consider during sampling. Lower values reduce randomness."
    },
    {
        term: "Top-p (nucleus sampling)",
        definition: "The cumulative probability threshold for sampling. Only tokens whose total probability exceeds p are considered."
    },
    {
        term: "FFN Mode",
        definition: "Controls the structure of the feedforward layer in the transformer. Examples: standard, lowrank, fused, quantized."
    },
    {
        term: "Precision",
        definition: "The numerical precision used during computation (e.g., float32, fp16, int8)."
    },
    {
        term: "Attention Type",
        definition: "The mechanism by which tokens attend to one another: dense, sparse, or flash (optimized CUDA)."
    },
    {
        term: "Latency",
        definition: "Total time (ms) from prompt submission to generation completion."
    },
    {
        term: "Entropy Plot",
        definition: "A visual showing per-token entropy across generated output to analyze drift or instability."
    },
    {
        term: "Token Count",
        definition: "Displays how many tokens were generated relative to the configured maximum."
    }
];