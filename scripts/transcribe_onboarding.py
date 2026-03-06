import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"
import whisper
from pathlib import Path
import sys

def transcribe_audio(audio_path, output_path):
    print("Loading Whisper model")
    model = whisper.load_model("base")
    print("Transcribing audio")
    result = model.transcribe(str(audio_path))
    transcript = result["text"]
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    print("Transcript saved to:", output_path)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        audio_file = Path(sys.argv[1])
    else:
        audio_file = Path("dataset/onboarding_calls/audio1975518882.m4a")
    output_file = Path("outputs/onboarding_transcript.txt")

    if not audio_file.exists():
        print("Audio file not found:", audio_file)
    else:
        transcribe_audio(audio_file, output_file)