import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.voice_handler import router as voice_router
from handlers.common_handler import router as common_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(voice_router)
    dp.include_router(common_router)

    print("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
