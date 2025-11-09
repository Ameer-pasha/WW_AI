# llama_local.py
# Helper to call local Ollama server

import requests
import os
import json

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_ENDPOINT = f"{OLLAMA_HOST}/api/generate"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")  # change if different

def call_local_llama(prompt, max_tokens=512, temperature=0.3, stream=False):
    """
    Calls Ollama local REST API. Returns text response.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream
    }
    try:
        resp = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        # Ollama may return different JSON shapes based on version. We'll check known keys.
        # Common: data["choices"][0]["message"]["content"] or data.get("response")
        if "response" in data:
            return data["response"]
        choices = data.get("choices", [])
        if choices:
            c = choices[0]
            msg = c.get("message") or c.get("text")
            if isinstance(msg, dict):
                return msg.get("content", "")
            return msg or ""
        # fallback
        return json.dumps(data)
    except Exception as e:
        return f"[Error calling Ollama: {str(e)}]"
