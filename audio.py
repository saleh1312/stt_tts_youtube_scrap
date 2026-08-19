"""Load audio files of any format and return base64-encoded WAV."""

from __future__ import annotations

import base64
import struct
import subprocess
from pathlib import Path

import imageio_ffmpeg

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit PCM


def _pcm_to_wav(pcm: bytes) -> bytes:
    """Wrap raw PCM in a WAV header with correct chunk sizes.

    ffmpeg cannot write valid RIFF sizes to a pipe (it uses 0xFFFFFFFF),
    and Hamsa then only transcribes the start of the audio.
    """
    byte_rate = SAMPLE_RATE * CHANNELS * SAMPLE_WIDTH
    block_align = CHANNELS * SAMPLE_WIDTH
    data_size = len(pcm)
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        36 + data_size,
        b"WAVE",
        b"fmt ",
        16,
        1,
        CHANNELS,
        SAMPLE_RATE,
        byte_rate,
        block_align,
        SAMPLE_WIDTH * 8,
        b"data",
        data_size,
    )
    return header + pcm


def load_audio(path: str | Path) -> str:
    """Load audio at ``path`` (any format) and return base64-encoded WAV.

    The file is decoded with ffmpeg, converted to 16 kHz mono PCM WAV
    (what Hamsa's realtime STT endpoint expects), then encoded as base64.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Audio file not found: {path}")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    result = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(path),
            "-ac",
            str(CHANNELS),
            "-ar",
            str(SAMPLE_RATE),
            "-f",
            "s16le",
            "-acodec",
            "pcm_s16le",
            "pipe:1",
        ],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0 or not result.stdout:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Failed to load audio {path}: {detail or 'unknown ffmpeg error'}")

    wav_bytes = _pcm_to_wav(result.stdout)
    return base64.b64encode(wav_bytes).decode("ascii")
