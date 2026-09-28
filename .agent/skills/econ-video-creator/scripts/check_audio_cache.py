#!/usr/bin/env python3
"""
Inspects and audits manim-voiceover audio caches.
Prevents accidental re-rendering and credit burn on ElevenLabs.
"""

from pathlib import Path

def inspect_cache(cache_dir="media/voiceovers"):
    path = Path(cache_dir)
    if not path.exists():
        print(f"[!] No audio cache directory found at '{cache_dir}'.")
        return

    wav_files = list(path.glob("*.wav"))
    mp3_files = list(path.glob("*.mp3"))
    json_files = list(path.glob("*.json"))

    print(f"\n--- EconLab Audio Cache Summary ---")
    print(f"Location: {path.resolve()}")
    print(f"Total Cached Audio Files: {len(wav_files) + len(mp3_files)}")
    print(f"  - WAV (Piper): {len(wav_files)}")
    print(f"  - MP3 (ElevenLabs): {len(mp3_files)}")
    print(f"  - Metadata / Transcripts: {len(json_files)}")

    total_bytes = sum(f.stat().st_size for f in wav_files + mp3_files)
    print(f"Total Cache Size: {total_bytes / (1024 * 1024):.2f} MB")
    print("-----------------------------------\n")

if __name__ == "__main__":
    inspect_cache()
