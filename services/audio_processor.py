import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import torch
import numpy as np
from tqdm import tqdm
import torchaudio
from .embedding_model import xvector
from pydub import AudioSegment
from sklearn.preprocessing import StandardScaler

TARGET_SR = 16000
CHUNK_DURATION = 2.5

def pad_waveform(waveform, sr=TARGET_SR, min_len_sec=CHUNK_DURATION):
    min_samples = int(min_len_sec * sr)
    if waveform.shape[1] < min_samples:
        pad_len = min_samples - waveform.shape[1]
        waveform = torch.nn.functional.pad(waveform, (0, pad_len))
    return waveform

def convert_ogg_to_wav(ogg_path, wav_path):
    audio = AudioSegment.from_file(ogg_path, format="ogg")
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(wav_path, format="wav")

def load_audio(path):
    waveform, sr = torchaudio.load(path)

    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    if sr != TARGET_SR:
        waveform = torchaudio.functional.resample(waveform, sr, TARGET_SR)

    return waveform

def extract_xvector_embedding(path_or_waveform):
    if isinstance(path_or_waveform, str):
        waveform = load_audio(path_or_waveform)
    else:
        waveform = path_or_waveform

    print(waveform.shape)

    with torch.no_grad():
        emb = xvector.encode_batch(waveform)
    return emb.squeeze().cpu().numpy()


def split_audio_into_chunks(input_path, output_path):
    waveform = load_audio(input_path)
    total_samples = waveform.shape[1]
    chunk_samples = int(CHUNK_DURATION * TARGET_SR)
    chunks = []

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    start = 0
    index = 0
    while start + chunk_samples <= total_samples:
        chunk = waveform[:, start:start + chunk_samples]

        chunk_path = os.path.join(output_path, f"chunk_{index}.wav")
        torchaudio.save(chunk_path, chunk, TARGET_SR)

        chunks.append(chunk_path)

        start += chunk_samples
        index += 1

    #для коротких аудио
    rest_waveform = pad_waveform(waveform=waveform[:,start:])
    if waveform[:,start:].shape[1] != rest_waveform.shape[1]: 
        chunk_path = os.path.join(output_path, f"chunk_{index}.wav")
        torchaudio.save(chunk_path, rest_waveform, TARGET_SR)
        chunks.append(chunk_path)

    return chunks

def scale_audio(emb_vector):
    scaler = StandardScaler()
    return scaler.fit_transform(emb_vector)
