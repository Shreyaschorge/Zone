from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from keys import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE

bind = create_async_engine(
    f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}')

_sessionmaker = sessionmaker(bind, AsyncSession, expire_on_commit=False)
