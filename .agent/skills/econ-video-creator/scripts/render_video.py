#!/usr/bin/env python3
"""
CLI automation script to render EconLab Manim scenes (Long 16:9 or Short 9:16).
Validates environment, system dependencies (SoX, FFmpeg), and passes correct quality flags.

Usage:
  python render_video.py <script_path> <scene_name> [--quality {l,m,h,k}] [--aspect {16:9,9:16}] [--tts {piper,elevenlabs}]
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Verify that FFmpeg and SoX are available on system PATH."""
    errors = []
    if not shutil.which("ffmpeg"):
        errors.append("FFmpeg not found in PATH. Install via 'winget install Gyan.FFmpeg' or 'choco install ffmpeg'.")
    if not shutil.which("sox"):
        errors.append("SoX not found in PATH. manim-voiceover requires SoX to splice audio. Install via 'choco install sox.portable'.")
    return errors

def main():
    parser = argparse.ArgumentParser(description="Render EconLab Manim Video")
    parser.add_argument("script", help="Path to Python Manim script (e.g. tax_dwl.py)")
    parser.add_argument("scene", help="Scene class name to render (e.g. TaxDWLCameraVoiceover)")
    parser.add_argument("--quality", "-q", choices=["l", "m", "h", "k"], default="l",
                        help="Render quality: l=480p15, m=720p30, h=1080p60, k=4K60 (default: l)")
    parser.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9",
                        help="Aspect ratio: 16:9 for YouTube Long, 9:16 for YouTube Shorts (default: 16:9)")
    parser.add_argument("--tts", choices=["piper", "elevenlabs"], default="piper",
                        help="Text-to-speech backend to use (default: piper)")
    
    args = parser.parse_args()

    # 1. Dependency Check
    dep_errors = check_dependencies()
    if dep_errors:
        print("\n[!] Dependency Warnings:")
        for err in dep_errors:
            print(f"    - {err}")
        print()

    # 2. Setup Environment Variables
    env = os.environ.copy()
    env["TTS_SERVICE"] = args.tts

    # 3. Construct Manim Command
    cmd = ["manim", f"-q{args.quality}"]
    
    if args.aspect == "9:16":
        # Force vertical resolution
        if args.quality == "l":
            cmd += ["--pixel_width=480", "--pixel_height=854"]
        elif args.quality == "m":
            cmd += ["--pixel_width=720", "--pixel_height=1280"]
        else:
            cmd += ["--pixel_width=1080", "--pixel_height=1920"]

    cmd += [args.script, args.scene]

    print(f"\n[EconLab] Executing: {' '.join(cmd)}")
    print(f"[EconLab] TTS Engine: {args.tts.upper()}")
    print(f"[EconLab] Aspect Ratio: {args.aspect}")
    print("=" * 60)

    result = subprocess.run(cmd, env=env)
    if result.returncode == 0:
        print("\n[✔] Render completed successfully!")
    else:
        print(f"\n[✘] Render failed with exit code {result.returncode}")
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
