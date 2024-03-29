import databases
import sqlalchemy

from config import DATABASE_URL


metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)


class BaseMeta:
    metadata = metadata
    database = database
