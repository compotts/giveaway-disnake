import schemas.bot.bot_properties as bot_properties
import ujson
import os


class Config:
    """
    TODO:
     - REMOVE DEPRECATED MENTIONS OF SECRET.JSON AND USELESS CLASSMETHODS
    """

    token: str = os.getenv("TOKEN", "")
    db_url: str = os.getenv("DATABASE_URL", "")
    test_guild: str = os.getenv("TEST_GUILD", "")

    """
    REMOVE THE STUFF BELOW, ITS USELESS!!!!! AND THE Config CLASS IS USELESS TOO.
    JUST CREATE VARIABLES INSTEAD OF USING CLASSES
    """

    with open("configs/secret.json", mode="r", encoding="utf-8") as _file:
        _data = ujson.load(_file)

    @classmethod
    def get_bot(cls) -> bot_properties.Bot:
        return bot_properties.Bot(
            token=cls._data["token"],
            database_url=cls._data["databaseUrl"],
            test_guild=int(cls._data["testGuild"]),
        )

    @classmethod
    def get_url(cls):
        return cls._data["databaseUrl"]

