from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


bind = create_async_engine(
    "sqlite+aiosqlite:///data.db", echo=True)

_sessionmaker = sessionmaker(bind, AsyncSession, expire_on_commit=False)