import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hamsa import transcribe  # noqa: E402

AUDIO_PATH = ROOT / "data" / "WhatsApp Ptt 2026-08-19 at 1.13.33 PM.ogg"

if __name__ == "__main__":
    print(transcribe(AUDIO_PATH))
