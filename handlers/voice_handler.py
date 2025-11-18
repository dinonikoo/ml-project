from aiogram import Router, F
from aiogram.types import Message
from config import INPUT_DIR
from services.audio_processor import split_audio
import os

router = Router()

@router.message(F.voice)
async def handle_voice(message: Message):
    file_id = message.voice.file_id
    file = await message.bot.get_file(file_id)

    input_path = f"{INPUT_DIR}/{file_id}.oga"
    await message.bot.download_file(file.file_path, input_path)

    chunks = split_audio(input_path)

    info_text = "Аудио разбито на фрагменты:\n"
    for i, ch in enumerate(chunks):
        info_text += f"> Фрагмент {i+1}: {os.path.basename(ch)}\n"

    await message.answer(info_text)
