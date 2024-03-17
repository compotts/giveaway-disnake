import ujson
import models.bot.bot_properties as bot_properties

from tools.converters import Url


class Config:
    with open("configs/secret.json", mode="r", encoding="utf-8") as _file:
        _data = ujson.load(_file)

    @classmethod
    def get_bot(cls) -> bot_properties.Bot:
        return bot_properties.Bot(token=cls._data["token"], database_url=cls._data["databaseUrl"])
    
    @classmethod
    def get_url(cls):
        return cls._data["databaseUrl"]