from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from config import BOT_TOKEN
from loguru import logger
from handlers import start, info



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())



# Логирование запуска
logger.add("bot.log", rotation="1 MB")


# Интегрируем хендлеры
dp.include_routers(start.router, info.router)


async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
