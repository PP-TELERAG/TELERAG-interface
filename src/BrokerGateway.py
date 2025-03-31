import asyncio
import httpx
from Models import RAGResponse, RAGRequest, RAGAddSourcesRequest
from loguru import logger
class BrokerGateway:
    def __init__(self, broker_url:str, broker_search_in_topic: str, broker_search_out_topic: str, broker_add_document_topic: str):
        self.broker_search_produce = f"{broker_url}/topics/{broker_search_in_topic}/produce"
        self.broker_search_consume = f"{broker_url}/topics/{broker_search_out_topic}/consume"
        self.broker_add_document_produce = f"{broker_url}/topics/{broker_add_document_topic}/produce"

        self.__search_request_queue = asyncio.Queue()
        self.__search_result_queue = asyncio.Queue()
        self.__add_sources_request_queue = asyncio.Queue()


    async def put_to_search_request_queue(self, request: RAGRequest):
        await self.__search_request_queue.put(request)

    async def put_to_add_sources_request_queue(self, request: RAGAddSourcesRequest):
        await self.__add_sources_request_queue.put(request)

    async def __search(self, request: RAGRequest):
        data = {
            "userId": request.userId,
            "query": request.query,
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.broker_search_produce, json=data)
                if response.status_code != 200:
                    logger.error("Production of search request failed with status code: {}", response.status_code)
                    return
            except Exception as e:
                logger.exception("Exception while producing search request: {}", e)
                return

    async def __add_sources(self, request: RAGAddSourcesRequest):
        data = {
            "userId": request.userId,
            "sources": request.sources,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.__add_sources_request_queue, json=data)
                if response.status_code != 200:
                    logger.error("Sources production failed with status code: {}", response.status_code)
                    return
            except Exception as e:
                logger.exception("Sources production failed with exception: {}", e)
                return

    async def consume_search_response(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.broker_search_consume)
                if response.status_code != 200:
                    logger.error("Search response consumption failed with status code: {}", response.status_code)
                    return
                await self.__search_result_queue.put(response)
            except Exception as e:
                logger.exception("Search response consumption failed with exception: {}", e)
                return

    async def runloop(self):
        # CHECK SEARCH REQUEST QUEUE
        while True:
            request = await self.__search_request_queue.get()
            if type(request) is not RAGRequest:
                logger.warning("Unsupported type of request: {}", type(request))
            else:
                try:
                    await self.__search(request)
                except Exception as e:
                    logger.exception("Search request failed with exception: {}", e)
                finally:
                    self.__search_request_queue.task_done()

            request = await self.__add_sources_request_queue.get()
            if type(request) is not RAGAddSourcesRequest:
                logger.warning("Unsupported type of request: {}", type(request))
            else:
                try:
                    await self.__add_sources(request)
                except Exception as e:
                    logger.exception("Add source request failed with exception: {}", e)
                finally:
                    self.__add_sources_request_queue.task_done()
    async def stop(self):
        await self.__add_sources_request_queue.join()
        try:
            await self.__search_result_queue
        except asyncio.CancelledError:
            pass

        await self.__add_sources_request_queue.join()
        try:
            await self.__add_sources_request_queue
        except asyncio.CancelledError:
            pass

        await self.__search_request_queue.join()
        try:
            await self.__search_result_queue
        except asyncio.CancelledError:
            pass

        logger.info("Broker Gateway stopped successfully!")




