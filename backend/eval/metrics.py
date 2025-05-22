# backend/eval/metrics.py

import matplotlib.pyplot as plt
import torch


def plot_token_entropy(scores):
    """
    Visualize the entropy per token based on generation scores.
    :param scores: list of score tensors from model.generate(..., output_scores=True)
    :return: matplotlib figure
    """
    if not scores:
        print("[GRAIL] No scores to visualize.")
        return None

    entropy = []
    for i, s in enumerate(scores):
        prob = torch.nn.functional.softmax(s, dim=-1)
        ent = -(prob * torch.log(prob + 1e-9)).sum(dim=-1).mean().item()
        entropy.append(ent)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(entropy, marker='o', label="Entropy")
    ax.set_title("Token-Level Entropy Over Time")
    ax.set_xlabel("Token Index")
    ax.set_ylabel("Entropy")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    return fig


def score_output(prompt: str, response: str) -> dict:
    """
    Simple heuristic scoring function to evaluate an output.
    This version scores length, overlap, and response diversity.

    :param prompt: original prompt string
    :param response: model's generated response
    :return: dictionary of scores
    """
    from collections import Counter
    import re

    def tokenize(text):
        return re.findall(r'\b\w+\b', text.lower())

    prompt_tokens = tokenize(prompt)
    response_tokens = tokenize(response)

    overlap = len(set(prompt_tokens) & set(response_tokens)) / (len(set(prompt_tokens)) + 1e-6)
    diversity = len(set(response_tokens)) / (len(response_tokens) + 1e-6)
    length_score = min(len(response_tokens) / 50.0, 1.0)

    return {
        "overlap": round(overlap, 3),
        "diversity": round(diversity, 3),
        "length_score": round(length_score, 3),
        "total_score": round((overlap + diversity + length_score) / 3, 3)
    }
