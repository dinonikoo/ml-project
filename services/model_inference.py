import numpy as np
from tensorflow.keras.models import load_model
from .audio_processor import extract_features

MODEL_PATH = "Emotion_Model_best.keras"

model = load_model(MODEL_PATH)

EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

def predict_emotion_for_chunk(chunk_path: str):
    features = extract_features(chunk_path)
    print(features)
    features = np.expand_dims(features, axis=0)

    preds = model.predict(features, verbose=0)[0]
    idx = np.argmax(preds)
    conf = preds[idx]

    return EMOTIONS[idx], float(conf)
