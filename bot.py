import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.voice_handler import router as voice_router

async def main():
    bot = Bot(token="7745407172:AAFfpfLFzp6_KKqymqQ7bzktuHwxx0_qi_w")
    dp = Dispatcher()

    dp.include_router(voice_router)

    print("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
