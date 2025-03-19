from sqlalchemy.ext.asyncio import create_async_engine
from src.database.models import Base

from src.config import app_config

engine = create_async_engine(
    app_config.POSTGRES.url,
    echo=False
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)