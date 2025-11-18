import librosa
import numpy as np
import scipy.signal
import soundfile as sf
import os

TARGET_SR = 44100
CHUNK_DURATION = 2.5
N_MFCC = 13


def split_audio(input_path: str, output_folder: str):

    audio, sr = librosa.load(input_path, sr=None)
    duration = librosa.get_duration(y=audio, sr=sr)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    chunks_paths = []

    start = 0
    index = 0

    while start + CHUNK_DURATION <= duration:
        start_sample = int(start * sr)
        end_sample = int((start + CHUNK_DURATION) * sr)

        chunk_audio = audio[start_sample:end_sample]

        chunk_path = os.path.join(output_folder, f"chunk_{index}.wav")
        
        sf.write(chunk_path, chunk_audio, sr)

        chunks_paths.append(chunk_path)

        start += CHUNK_DURATION
        index += 1

    return chunks_paths


def extract_features(path: str):
    X, orig_sr = librosa.load(path, sr=None)

    # Ресэмплирование под 44100
    num_samples = int(len(X) * TARGET_SR / orig_sr)
    X_resampled = scipy.signal.resample(X, num_samples)

    # MFCC
    mfccs = np.mean(
        librosa.feature.mfcc(
            y=X_resampled,
            sr=TARGET_SR,
            n_mfcc=N_MFCC
        ),
        axis=0
    )

    return mfccs
