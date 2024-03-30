import sqlalchemy
from sqlalchemy.engine import Engine

from config import DATABASE_URL

from .base import metadata, database, base_ormar_config


def db_setup(
    metadata: sqlalchemy.MetaData,
) -> Engine:
    engine = sqlalchemy.create_engine(DATABASE_URL)

    if not engine:
        raise RuntimeError("Database engine was not created properly")

    metadata.drop_all(engine)
    metadata.create_all(engine)

    return engine


__all__ = (
    "db_setup",
    "base_ormar_config",
    "database",
    "metadata",
)

