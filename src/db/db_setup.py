import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

from config import DATABASE_URL


async def db_setup(
    metadata: sqlalchemy.MetaData,
) -> sqlalchemy.engine.Engine:
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    if not engine:
        raise RuntimeError("Database engine was not created properly")

    # metadata.drop_all(engine)
    # metadata.create_all(engine)

    return engine
