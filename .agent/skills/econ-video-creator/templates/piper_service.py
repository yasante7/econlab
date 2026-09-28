from pathlib import Path
import subprocess
import sys
import wave
from manim_voiceover.services.base import SpeechService

class PiperService(SpeechService):
    """
    Local offline text-to-speech service for manim-voiceover using Piper TTS.
    Allows zero-cost, zero-latency local development and iteration.
    """

    def __init__(
        self,
        model_path: str = "voices/en-us-lessac-medium.onnx",
        config_path: str = None,
        **kwargs
    ):
        self.model_path = Path(model_path).resolve()
        self.config_path = Path(config_path or f"{model_path}.json").resolve()
        
        # Verify model files exist
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Piper voice model not found at {self.model_path}.\n"
                f"Run python -m piper.download_voices en_US-lessac-medium --download-dir voices/"
            )
            
        super().__init__(**kwargs)

    def generate_from_text(self, text: str, cache_dir: str = None, path: str = None, **kwargs) -> dict:
        if cache_dir is None:
            cache_dir = self.cache_dir

        # Use audio hash to ensure deterministic caching
        audio_path = Path(path) if path else Path(cache_dir) / f"{self.get_data_hash(text)}.wav"

        # Generate audio only if not already cached
        if not audio_path.exists():
            cmd = [
                sys.executable, "-m", "piper",
                "--model", str(self.model_path),
                "--config", str(self.config_path),
                "--output_file", str(audio_path)
            ]
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True
            )
            _, stderr = process.communicate(input=text)
            if process.returncode != 0:
                raise RuntimeError(f"Piper TTS generation failed: {stderr}")

        # Compute exact audio duration for Manim animation synchronization
        with wave.open(str(audio_path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)

        return {
            "final_audio": str(audio_path),
            "word_boundaries": [],
            "duration": duration
        }
