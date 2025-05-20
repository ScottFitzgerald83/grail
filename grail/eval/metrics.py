# grail/eval/metrics.py

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
