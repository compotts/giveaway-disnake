import sqlalchemy

from config import DATABASE_URL


def db_setup(
    metadata: sqlalchemy.MetaData,
) -> sqlalchemy.engine.Engine:
    engine = sqlalchemy.create_engine(DATABASE_URL)

    if not engine:
        raise RuntimeError("Database engine was not created properly")

    metadata.drop_all(engine)
    metadata.create_all(engine)

    return engine
