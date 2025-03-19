from src.database.db_session import db_session
from src.database.models.models import User
from sqlalchemy import select

# Executed after user sends the /start command
async def set_user(telegram_id: int) -> None:
    async with db_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

        if not user:
            session.add(User(telegram_id=telegram_id))
            await session.commit()