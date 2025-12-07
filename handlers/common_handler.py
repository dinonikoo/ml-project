from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

router = Router()

@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(
        "Привет! 👋\n"
        "Я могу распознавать эмоции в голосовых сообщениях. "
        "Отправь мне аудио, и я скажу, какая эмоция там выражена."
    )