from src.database.db_session import db_session
from src.database.models import User, Source
from sqlalchemy import select

# Executed after user sends the /start command
async def set_user(telegram_id: int) -> None:
    async with db_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )

        if not user:
            session.add(User(telegram_id=telegram_id))
            await session.commit()

async def select_user_sources(telegram_id: int) -> list[Source]:
    async with db_session() as session:
        query = (
            select(Source).where(Source.user_id == telegram_id)
        )

        result = await session.scalars(query)
        return result.all()

async def set_sources(user_id: int, urls: set) -> None:
    async with db_session() as session:
        sources = [Source(user_id=user_id, url=url) for url in urls]

        session.add_all(sources)
        await session.commit()