# backend/eval/profiler.py

import torch
import time


def profile_run(trace, start_time=None, end_time=None):
    """
    Profile generation latency and softmax entropy if available.
    """
    metrics = {}

    # Entropy measurement
    if hasattr(trace, 'scores') and trace.scores:
        scores = torch.stack(trace.scores, dim=1)  # shape: (batch, seq_len, vocab)
        softmax = torch.nn.functional.softmax(scores, dim=-1)
        entropy = -(softmax * torch.log(softmax + 1e-9)).sum(dim=-1).mean().item()
        metrics["entropy"] = round(entropy, 4)

    # Real latency measurement (if provided)
    if start_time is not None and end_time is not None:
        metrics["latency_ms"] = round((end_time - start_time) * 1000, 2)
    else:
        metrics["latency_ms"] = -1

    if hasattr(trace, 'sequences'):
        token_count = trace.sequences.shape[-1]
        metrics["tokens_generated"] = token_count
        print(f"[GRAIL] Tokens generated: {token_count}")
    else:
        print("[GRAIL] No sequences found in trace.")

    return metrics
