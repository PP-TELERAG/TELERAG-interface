from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log"
)
logger = logging.getLogger(__name__)

bot = Bot(token=".")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Добро пожаловать! Используйте /help для получения инструкций.")

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Руководство пользования:\n"
                         "/help - Получить помощь\n"
                         "/info - Информация о проекте\n"
                         "/license - Лицензия")

@dp.message(Command("info"))
async def info_command(message: Message):
    await message.answer("Информация о проекте и обратная связь:\n"
                         "Здесь будет информация о проекте и контакты для обратной связи.")

@dp.message(Command("license"))
async def license_command(message: Message):
    await message.answer("Лицензия:\n"
                         "Здесь будет текст лицензии.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())