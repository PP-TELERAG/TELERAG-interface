import asyncio

from aiogram import Bot, Dispatcher

from src.config import app_config
from src.bot.routers import router as main_router
from src.database.db_setup import create_tables

async def main():
    await create_tables()
    bot = Bot(app_config.BOT.TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExit")