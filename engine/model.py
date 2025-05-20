# grail/engine/model.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

_model_cache = {}

def load_model(config):
    model_name = config["model_name"]
    if model_name in _model_cache:
        return _model_cache[model_name]

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    if config["precision"] == "fp16":
        model = model.half()
    elif config["precision"] == "int8":
        from transformers import BitsAndBytesConfig
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=BitsAndBytesConfig(load_in_8bit=True)
        )

    model.to(config["device"])
    model.eval()

    _model_cache[model_name] = (model, tokenizer)
    return model, tokenizer


def run_inference(model_bundle, prompt, req):
    model, tokenizer = model_bundle
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=req.get("max_tokens", 128),
            temperature=req.sampling.get("temperature", 0.7),
            top_k=req.sampling.get("top_k", 50),
            top_p=req.sampling.get("top_p", 0.9),
            return_dict_in_generate=True,
            output_scores=True
        )

    decoded = tokenizer.decode(output.sequences[0], skip_special_tokens=True)
    return decoded, output
