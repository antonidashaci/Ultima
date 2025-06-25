#!/usr/bin/env python3
"""Simple async wrapper for chatting with local Ollama server."""
import asyncio, json, requests
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral:instruct"

def _sync_generate(data):
    r = requests.post(OLLAMA_URL, json=data, timeout=180)
    r.raise_for_status()
    return r.json()["response"]

async def chat(prompt: str, model: str = DEFAULT_MODEL, system: Optional[str] = None) -> str:
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if system:
        data["system"] = system
    # run blocking HTTP in thread pool
    return await asyncio.to_thread(_sync_generate, data) 