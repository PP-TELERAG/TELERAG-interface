import asyncio

from loguru import logger
from src.config import Settings
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.fsm.storage.memory import MemoryStorage
from src.Models import RAGResponse, RAGRequest
from src.BrokerGateway import BrokerGateway

class BotApp:
    def __init__(self, config: Settings):
        self.bot = Bot(token=config.TOKEN)
        self.dispatcher = Dispatcher(storage=MemoryStorage())
        self.router = Router()
        self.dispatcher.include_router(self.router)

        self.broker_gateway = BrokerGateway(
            broker_url=config.BROKER_URL,
            broker_search_in_topic=config.BROKER_SEARCH_QUERY_IN_TOPIC,
            broker_search_out_topic=config.BROKER_SEARCH_OUT_TOPIC,
            broker_add_document_topic=config.BROKER_ADD_DOCUMENT_TOPIC
        )

        self.response_queue = asyncio.Queue()
        self.pending_messages = {}

    def __include_handlers(self):
        self.router.message.register(self.__start_handler, F.text == '/start')
        self.router.message.register(self.__help_handler, F.text == '/help')
        self.router.message.register(self.__info_handler, F.text == '/info')
        self.router.message.reqister(self.__licence_handler, F.text == '/licence')
        self.router.message.register(self.__add_source_handler, F.text == '/add')
        self.router.message.register(self.__message_handler, F.text)
    @staticmethod
    async def __start_handler(self, message: types.Message):
        try:
            await message.answer("Добро пожаловать! Это проект TELERAG, используйте /help для того чтобы узнать больше\n")
        except Exception as e:
            logger.exception("Exception while handling startup message: {}", e)

    @staticmethod
    async def __help_handler(self, message: types.Message):
        text = (
            "Руководство:\n"
            "/add - Добавление источников (после первого добавленного источника произойдет регистрация в сервисе\n"
            "/info - Информация о проекте"
        )
        await message.answer(text)

    @staticmethod
    async def __info_handler(self, message: types.Message):
       info_text = (
           "Название проекта: TELERAG\n"
           "Цель проекта:\n"
           "Основная цель проекта заключается в организации поиска информации по нескольким Telegram-каналам\n"
           "с использованием технологии Retrieval Augmented Generation (RAG) и генерации ответа посредством\n"
           "большой языковой модели. Проект решает проблему поиска информации для клиентов, обладающих большим\n"
           "числом каналов, и ориентирован преимущественно на сегмент B2C\n"
           "Версия проекта: 1.0\n"
           "Обратная связь: https://github.com/PP-TELERAG \n"
           "Там вы сможете посмотреть исходный код всех сервисов системы"
       )

       await message.answer(info_text)

    @staticmethod
    async def __licence_handler(self, message: types.Message):
       license_text = (
           "Проект находится под лицензией AGPL v3:\n"
           "https://www.gnu.org/licenses/agpl-3.0.txt"
       )
       await message.answer(license_text)

    async def __add_source_handler(self, message: types.Message):
        pass # Нужно будет договорится как мы будем их форматировать


    async def __message_handler(self, message: types.Message):
        request = RAGRequest(
            user_id=message.from_user.id,
            query=message.text,
        )

        await self.broker_gateway.put_to_search_request_queue(request)
        temporary_response_text = await message.answer("Сообщение получено, процесс поиска может занять некоторое время...")
        self.pending_messages[message.from_user.id] = temporary_response_text.message_id


    async def __send_response(self, response: RAGResponse):
        temp_msg_id = self.pending_messages.pop(response.user_id, None)
        if temp_msg_id is not None:
            try:
                await self.bot.delete_message(chat_id=response.user_id, message_id=temp_msg_id)
            except Exception:
                pass
        await self.bot.send_message(chat_id=response.user_id, text=response.response)

    async def poll_responses_queue(self):
        while True:
            if not self.response_queue.empty():
                response = await self.response_queue.get()
                if type(response) is not RAGResponse:
                    logger.warning("Unsupported response type: {}", type(response))
                    continue

                try:
                    await self.__send_response(response)
                except Exception as e:
                    logger.exception("Exception while sending response: {}", e)