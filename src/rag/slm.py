import os
from typing import Optional

import requests


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

SLM_BACKEND = os.getenv("SLM_BACKEND", "ollama").lower()

HF_BASE_MODEL_PATH = os.getenv("HF_BASE_MODEL_PATH", "")
HF_LORA_ADAPTER_PATH = os.getenv("HF_LORA_ADAPTER_PATH", "models/mistral7b-lora")
HF_MAX_NEW_TOKENS = int(os.getenv("HF_MAX_NEW_TOKENS", "256"))

_hf_model: Optional[object] = None
_hf_tokenizer: Optional[object] = None


def _load_hf_model():
    global _hf_model, _hf_tokenizer

    if _hf_model is not None and _hf_tokenizer is not None:
        return _hf_model, _hf_tokenizer

    if not HF_BASE_MODEL_PATH:
        raise ValueError("HF_BASE_MODEL_PATH is not set.")

    if not os.path.isdir(HF_BASE_MODEL_PATH):
        raise FileNotFoundError(f"Base model path not found: {HF_BASE_MODEL_PATH}")

    if not os.path.isdir(HF_LORA_ADAPTER_PATH):
        raise FileNotFoundError(f"LoRA adapter path not found: {HF_LORA_ADAPTER_PATH}")

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(HF_BASE_MODEL_PATH, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    use_cuda = torch.cuda.is_available()
    dtype = torch.float16 if use_cuda else torch.float32
    device_map = "auto" if use_cuda else "cpu"

    base_model = AutoModelForCausalLM.from_pretrained(
        HF_BASE_MODEL_PATH,
        device_map=device_map,
        torch_dtype=dtype,
    )

    model = PeftModel.from_pretrained(base_model, HF_LORA_ADAPTER_PATH)

    _hf_model = model
    _hf_tokenizer = tokenizer
    return _hf_model, _hf_tokenizer


def _generate_answer_hf(prompt: str) -> str:
    model, tokenizer = _load_hf_model()

    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = inputs.to(model.device)

    output = model.generate(
        **inputs,
        max_new_tokens=HF_MAX_NEW_TOKENS,
        do_sample=False,
    )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    if decoded.startswith(prompt):
        return decoded[len(prompt):].lstrip()
    return decoded.strip()


def _generate_answer_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    result = response.json()
    answer = result.get("response")
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("Ollama returned an empty or malformed response.")
    return answer.strip()


def generate_answer(prompt: str) -> str:
    if SLM_BACKEND not in {"hf", "ollama"}:
        raise ValueError("SLM_BACKEND must be ollama or hf.")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")
    if SLM_BACKEND == "hf":
        return _generate_answer_hf(prompt)

    return _generate_answer_ollama(prompt)