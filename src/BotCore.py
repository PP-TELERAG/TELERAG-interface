import logging
from typing import Any, Dict

from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from pydantic_settings import BaseSettings
from aiogram import Router

# Config должен быть в отдельном файле ((config.py))и загружать переменные из .env

class BotCore:
    def __init__(self, config: Any):  # Здесь будет использоваться Config
        self.bot = Bot(token=config.BOT_TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.router = Router()  # Создаем роутер для  с версией aiogram 3.x
        self.dp.include_router(self.router)
        self._setup_handlers()

        # здесь настройка логирования в файле(!)
        logging.basicConfig(
            filename='bot.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def _setup_handlers(self) -> None:
        self.router.message.register(self._start_handler, F.text == '/start')
        self.router.message.register(self._help_handler, F.text == '/help')
        self.router.message.register(self._info_handler, F.text == '/info')
        self.router.message.register(self._license_handler, F.text == '/license')
        self.router.message.register(self._add_source_handler, F.text == '/add_source')

    async def _start_handler(self, message: types.Message) -> None:
        """Обработчик команды /start с аутентификацией"""
        user_id = message.from_user.id

        # ДОЛЖЕН БЫТЬ ЗДЕСЬ ЗАПРОС К БАЗЕ ДАННЫХ ДЛЯ СОЗДАНИЯ ТАБЛИЦЫ
        try:
            # Вызов RAG модуля если сообщение содержит аргументы
            if len(message.text.split()) > 1:
                await self._handle_rag_input(message)
                return

            await message.answer("Добро пожаловать! Я проект TELERAG, используйте /help для того чтобы узнать больше\n"
                                 "обо мне:)")
        except Exception as e:
            logging.error(f"Start error: {e}")
            await self._handle_error(message, e)

    async def _handle_rag_input(self, message: types.Message) -> None:
        """Перенаправление запроса в RAG модуль"""
        #ЗДЕСЬ БУДЕТ ИНТЕГРАЦИЯ С RAG МОДУЛЕМ
        response = "Заглушка для RAG ответа"
        await message.answer(response)
        logging.info(f"RAG request: {message.text}")

    async def _help_handler(self, message: types.Message) -> None:
        """Руководство пользователя"""
        help_text = (
            "Руководство:\n"
            "/start - Начать работу\n"
            "/add_source - Добавить интересующий Вас источник\n"
            "/info - Информация о проекте"
        )
        await message.answer(help_text)

    async def _info_handler(self, message: types.Message) -> None:
        """Информация о проекте"""
        info_text = (
            "Название проекта: TELERAG\n"
            "Цель проекта:\n"
            "Основная цель проекта заключается в организации поиска информации по нескольким Telegram-каналам\n"
            "с использованием технологии Retrieval Augmented Generation (RAG) и генерации ответа посредством\n"
            "большой языковой модели. Проект решает проблему поиска информации для клиентов, обладающих большим\n"
            "числом каналов, и ориентирован преимущественно на сегмент B2C\n"
            "Версия проекта: 1.0\n"
            "Обратная связь: (Обратная связь (Что-то)"
        )
        await message.answer(info_text)

    async def _license_handler(self, message: types.Message) -> None:
        """Лицензионная информация"""
        await message.answer("Лицензия: (Что-то)")

    async def _add_source_handler(self, message: types.Message) -> None:
        """Добавление источников"""
        #зДЕСЬ БУДЕТ ИНТЕРФЕЙС ВЫБОРА ИСТОЧНИКОВ
        await message.answer("Источники могут быть добавлены через кнопки")
        #ЗДЕСЬ БУДЕТ ЗАПРОС К БАЗЕ ДАННЫХ

    async def _handle_error(self, message: types.Message, error: Exception) -> None:
        """Обработка и логирование ошибок"""
        error_msg = (
            f"Ошибка: {str(error)}\n"
            "Ошибка, пожалуйста, попробуйте позже или обратитесь в поддержку :( "
        )
        await message.answer(error_msg)
        logging.error(f"User {message.from_user.id} error: {str(error)}")

    async def start(self) -> None:
        """Запуск бота"""
        logging.info("Starting bot...")
        await self.dp.start_polling(self.bot)