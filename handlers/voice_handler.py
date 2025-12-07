import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from aiogram import Router, F
from aiogram.types import Message
from services.audio_processor import split_audio_into_chunks, convert_ogg_to_wav
from services.model_inference import predict_emotion_for_chunk

router = Router()

@router.message(F.voice)
async def handle_voice(message: Message):

    input_dir = "temp/input"
    chunks_dir = "temp/chunks"

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(chunks_dir, exist_ok=True)

    for f in os.listdir(chunks_dir):
        os.remove(os.path.join(chunks_dir, f))

    file = await message.bot.get_file(message.voice.file_id)
    input_path_ogg = os.path.join(input_dir, "input.ogg")
    await message.bot.download_file(file.file_path, input_path_ogg)

    input_path_wav = os.path.join(input_dir, "input.wav")
    convert_ogg_to_wav(input_path_ogg,input_path_wav)

    chunk_paths = split_audio_into_chunks(input_path_wav, chunks_dir)

    if not chunk_paths:
        await message.answer("Аудио слишком короткое для анализа.")
        return

    result_text = " *Распознанные эмоции по сегментам:*\n\n"

    for i, chunk in enumerate(chunk_paths):
        emotion, conf = predict_emotion_for_chunk(chunk)
        result_text += f" Сегмент {i+1}: *{emotion}* (уверенность: {conf:.2f})\n"

    await message.answer(result_text, parse_mode="Markdown")
