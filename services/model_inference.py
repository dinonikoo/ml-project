import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import numpy as np
import joblib
from .audio_processor import extract_xvector_embedding,scale_audio

MODEL_PATH = "ml-project/xgboost_model_augmentation_xvector_TESS.joblib"

model = joblib.load(MODEL_PATH)

EMOTIONS = ['fearful', 'surprised', 'happy', 'angry', 'disgust', 'sad']

def predict_emotion_for_chunk(chunk_path: str):
    emb = extract_xvector_embedding(chunk_path)
    print(emb)
    vec_2d = emb.reshape(1, -1)

    pred_idx = model.predict(vec_2d)[0]
    pred_proba = model.predict_proba(vec_2d)[0]
    print(pred_idx)

    return EMOTIONS[pred_idx], pred_proba[pred_idx]
