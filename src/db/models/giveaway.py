import ormar

from db import metadata, database


class Giveaway(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata=metadata,
        database=database,
        tablename="giveaways",
    )

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    name: str = ormar.String(max_length=64)
    description: str = ormar.String(max_length=1024)
    prize: str = ormar.String(max_length=1024)
    start_time: int = ormar.DateTime()
    end_time: int = ormar.DateTime()
    winners: int = ormar.Integer()
    voice: str = ormar.String(max_length=64)
    ended: bool = ormar.Boolean(default=False)
