import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


def generate_answer(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return result["response"].strip()