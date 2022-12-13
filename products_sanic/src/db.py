from sqlalchemy.ext.asyncio import create_async_engine


bind = create_async_engine(
    "sqlite+aiosqlite:///data.db", echo=True)
