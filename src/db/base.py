import databases
import sqlalchemy
import ormar

from config import DATABASE_URL


metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)

base_ormar_config = ormar.OrmarConfig(
    metadata=metadata,
    database=database,
)
