from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time  # NEW
import logging  # NEW

_model_cache = {}
logger = logging.getLogger(__name__)  # NEW


def load_model(config):
    model_name = config["model_name"]
    if config.get("use_public_model") == "true":
        print("[GRAIL] Using public hosted model:", config["public_model_name"])
        return "remote", config["public_model_name"]
    if model_name in _model_cache:
        print("[GRAIL] Model loaded from cache:", model_name)
        return _model_cache[model_name]

    print("[GRAIL] Loading model:", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    if config["precision"] == "fp16":
        print("[GRAIL] Converting model to fp16")
        model = model.half()
    elif config["precision"] == "int8":
        from transformers import BitsAndBytesConfig
        print("[GRAIL] Loading model in int8 mode")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=BitsAndBytesConfig(load_in_8bit=True)
        )

    device = config.get("device", "cuda")
    if device == "cuda" and not torch.cuda.is_available():
        print("[GRAIL] CUDA not available — using CPU instead.")
        device = "cpu"
    print("[GRAIL] Using device:", device)
    model.to(device)
    model.eval()

    _model_cache[model_name] = (model, tokenizer)
    return model, tokenizer


def run_inference(model_bundle, prompt, req):
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("[GRAIL] Invalid prompt: Must be a non-empty string.")

    if isinstance(model_bundle, tuple) and model_bundle[0] == "remote":
        from backend.engine.remote import run_remote_inference
        return run_remote_inference(model_bundle[1], prompt, req)

    model, tokenizer = model_bundle

    token_estimate = len(tokenizer.encode(prompt))
    print(f"[GRAIL] Estimated token count for prompt: {token_estimate}")

    # Enforce prompt truncation if limit is configured
    truncate_limit = req.get("truncate_prompt", 0) if isinstance(req, dict) else getattr(req, "truncate_prompt", 0)
    if truncate_limit > 0:
        tokens = tokenizer(prompt, return_tensors="pt")["input_ids"][0]
        if len(tokens) > truncate_limit:
            print(f"[GRAIL] Truncating prompt from {len(tokens)} to {truncate_limit} tokens.")
            tokens = tokens[-truncate_limit:]
            prompt = tokenizer.decode(tokens, skip_special_tokens=True)

    print("[GRAIL] Prompt:", prompt)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    print("[GRAIL] Inputs shape:", inputs["input_ids"].shape)

    max_new_tokens = req.get("max_new_tokens", 128) if isinstance(req, dict) else getattr(req, "max_new_tokens", 128)
    # Enforce token cap
    max_total_tokens = req.get("max_total_tokens", 4096)
    input_token_count = inputs["input_ids"].shape[1]
    if input_token_count + max_new_tokens > max_total_tokens:
        raise ValueError(f"[GRAIL] Token limit exceeded: {input_token_count} input + {max_new_tokens} gen > {max_total_tokens}")
    print(f"[GRAIL] Token count check passed: input={input_token_count}, max_new={max_new_tokens}, cap={max_total_tokens}")
    sampling = req.get("sampling", {}) if isinstance(req, dict) else getattr(req, "sampling", {})

    start_time = time.time()

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=sampling.get("temperature", 0.7),
            top_k=sampling.get("top_k", 50),
            top_p=sampling.get("top_p", 0.9),
            return_dict_in_generate=True,
            output_scores=True
        )

    end_time = time.time()

    decoded = tokenizer.decode(output.sequences[0], skip_special_tokens=True)
    print("[GRAIL] Decoded output:", decoded)
    print("[GRAIL] Trace sequences shape:", output.sequences.shape)
    if hasattr(output, "scores"):
        print("[GRAIL] Trace scores:", type(output.scores), "length:", len(output.scores))

    return decoded, output, start_time, end_time
