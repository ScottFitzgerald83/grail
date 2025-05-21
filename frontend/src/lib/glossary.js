export const glossaryMarkdown = `
| Term              | Definition                                                                                     |
|-------------------|-----------------------------------------------------------------------------------------------|
| Preset            | A saved configuration of model, attention, sampling, and generation parameters.              |
| Entropy           | A measurement of uncertainty in the model's prediction. Higher entropy means less confidence. |
| Top-k             | The number of highest probability tokens to consider during sampling.                         |
| Top-p             | The cumulative probability threshold for sampling.                                            |
| FFN Mode          | Controls the structure of the feedforward layer in the transformer.                           |
| Precision         | The numerical precision used during computation (e.g., float32, fp16, int8).                  |
| Attention Type    | The mechanism by which tokens attend to one another: dense, sparse, or flash.                |
| Latency           | Total time (ms) from prompt submission to generation completion.                             |
| Entropy Plot      | A visual showing per-token entropy across generated output to analyze drift or instability.  |
| Token Count       | Displays how many tokens were generated relative to the configured maximum.                  |
| System Prompt       | A hidden instruction prepended to guide the assistant’s tone, behavior, or scope. |
| Temperature         | Controls randomness in sampling; higher = more creative, lower = more deterministic. |
| Top-A Sampling      | Adaptive sampling strategy using cumulative probability mass rather than fixed thresholds. |
| Tokenization        | Converts input text into subword tokens that the model can process. |
| Context Window      | Maximum number of tokens the model can consider at once. |
| System Message      | Special message used to initialize model behavior in chat-like APIs. |
| LoRA (Low-Rank Adaptation) | Lightweight fine-tuning method using adapter weights for domain adaptation. |
| Token Budget        | Total available tokens for input and output in a single model invocation. |
| Prompt Injection    | Attack where malicious input overrides system instructions or controls. |
| Beam Search         | Decoding strategy that explores multiple token paths to select the most likely sequence. |
`;