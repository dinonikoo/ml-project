import os
from pydub import AudioSegment
from config import CHUNKS_DIR

def split_audio(file_path):
    clear_chunk_folder()

    audio = AudioSegment.from_file(file_path, format="ogg")
    chunks = []
    for i, start in enumerate(range(0, len(audio), 5000)):
        chunk = audio[start:start+5000]
        chunk_path = f"temp/chunks/chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks

def clear_chunk_folder():
    from pathlib import Path
    folder = Path("temp/chunks")
    if folder.exists():
        for f in folder.iterdir():
            if f.is_file():
                f.unlink()