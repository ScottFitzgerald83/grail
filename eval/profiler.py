# grail/eval/profiler.py

import torch

def profile_run(trace):
    """
    Basic stub: profile generation latency and softmax entropy if available.
    """
    metrics = {}

    # Latency (if scores include timing info — placeholder here)
    if hasattr(trace, 'scores') and trace.scores:
        scores = torch.stack(trace.scores, dim=1)  # shape: (batch, seq_len, vocab)
        softmax = torch.nn.functional.softmax(scores, dim=-1)
        entropy = -(softmax * torch.log(softmax + 1e-9)).sum(dim=-1).mean().item()
        metrics["entropy"] = round(entropy, 4)

    # Placeholder: real latency profiling could use torch.profiler or time.time()
    metrics["latency_ms"] = -1  # replace with real timing in future step
    metrics["tokens_generated"] = trace.sequences.shape[-1] if hasattr(trace, 'sequences') else None

    return metrics
