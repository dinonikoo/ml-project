import torchaudio
from speechbrain.inference import EncoderClassifier

torchaudio.set_audio_backend("sox_io")
print("Audio backend:", torchaudio.get_audio_backend())

xvector = EncoderClassifier.from_hparams(
    source="xvector_model",
    savedir="xvector_model"
)
