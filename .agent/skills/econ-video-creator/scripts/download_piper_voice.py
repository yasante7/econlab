#!/usr/bin/env python3
"""
Downloads Piper TTS ONNX models and JSON configs into the voices/ directory.
Supports medium and high quality tiers.

Usage:
  python download_piper_voice.py [voice_name] [--download-dir voices/]
Default voice: en_US-lessac-medium
"""

import argparse
import subprocess
import sys
from pathlib import Path

DEFAULT_VOICE = "en_US-lessac-medium"
AVAILABLE_RECOMMENDED_VOICES = [
    "en_US-lessac-medium",  # Fast, lightweight default (63MB)
    "en_US-lessac-high",    # High fidelity, great articulation
    "en_US-ryan-high",      # Deeper, authoritative male voice
    "en_US-amy-medium",     # Clear natural female voice
]

def main():
    parser = argparse.ArgumentParser(description="Download Piper TTS voice models")
    parser.add_argument("voice", nargs="?", default=DEFAULT_VOICE,
                        help=f"Voice name to download (default: {DEFAULT_VOICE})")
    parser.add_argument("--download-dir", default="voices",
                        help="Directory to save voice models (default: voices/)")
    
    args = parser.parse_args()
    dest_dir = Path(args.download_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"[EconLab] Downloading Piper voice '{args.voice}' into '{dest_dir}'...")
    
    cmd = [
        sys.executable, "-m", "piper.download_voices",
        args.voice,
        "--download-dir", str(dest_dir)
    ]

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"\n[✔] Successfully downloaded {args.voice} to {dest_dir.resolve()}")
    else:
        print(f"\n[✘] Failed to download {args.voice}. Ensure 'piper-tts' is installed in your python environment.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
