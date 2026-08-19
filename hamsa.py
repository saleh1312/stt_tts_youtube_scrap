"""Send audio to Hamsa realtime STT and return the transcribed text."""

from __future__ import annotations

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from audio import load_audio

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

HAMSA_STT_URL = "https://api.tryhamsa.com/v1/realtime/stt"


def _extract_text(payload: object) -> str | None:
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    if isinstance(data, dict) and isinstance(data.get("text"), str):
        return data["text"]
    if isinstance(payload.get("text"), str):
        return payload["text"]
    return None


def transcribe(audio_path: str | Path, language: str = "ar", model: str = "s2") -> str:
    """Load audio at ``audio_path``, send it to Hamsa, and return the text."""
    api_key = os.getenv("HAMSA_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        raise RuntimeError("Set HAMSA_API_KEY in .env before calling transcribe().")

    audio_base64 = load_audio(audio_path)
    response = requests.post(
        HAMSA_STT_URL,
        headers={
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "audioBase64": audio_base64,
            "language": language,
            "model": model,
            "isEosEnabled": False,
        },
    )
    response.raise_for_status()
    payload = response.json()
    text = _extract_text(payload)
    if text is None:
        raise RuntimeError(f"Hamsa response did not include text: {payload}")
    return text
