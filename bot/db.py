import json

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from bot.config import config

engine = create_async_engine(
    config.sqlalchemy_url,
    echo=False,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
    json_deserializer=json.loads,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
