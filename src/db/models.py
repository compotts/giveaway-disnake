import ormar
import datetime

from sqlalchemy import text
from enum import Enum

from db import base_ormar_config


class StatusEnum(str, Enum):
    active = "active"
    ended = "ended"


class VoiceEnum(str, Enum):
    no = "No"
    voice = "Voice"
    tribune = "Tribune"


class Giveaway(ormar.Model):
    ormar_config = base_ormar_config.copy(
        tablename="giveaways",
    )

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    message_id: int = ormar.BigInteger()
    channel_id: int = ormar.BigInteger()
    guild_id: int = ormar.BigInteger()
    hoster_id: int = ormar.BigInteger()
    prize: str = ormar.String(minimum=1, max_length=64)
    winers: int = ormar.Integer()
    start_time: int = ormar.DateTime(default=datetime.datetime.now())
    end_time: int = ormar.DateTime()
    voice_needed: VoiceEnum = ormar.Enum(enum_class=VoiceEnum)
    status: StatusEnum = ormar.Enum(enum_class=StatusEnum)


class Participant(ormar.Model):
    ormar_config = base_ormar_config.copy(
        tablename="giveaway_entries",
    )

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    giveaway_id: int = ormar.BigInteger()
    user_id: int = ormar.BigInteger()
    entry_time: int = ormar.DateTime(default=datetime.datetime.now())


"""
ormar.String(max_length: int, min_length: int = None, regex: str = None,) has a required max_length parameter
ormar.Text() has no required parameters.
ormar.Boolean() has no required parameters.
ormar.Integer(minimum: int = None, maximum: int = None, multiple_of: int = None) has no required parameters
ormar.BigInteger(minimum: int = None, maximum: int = None, multiple_of: int = None) has no required parameters
ormar.SmallInteger(minimum: int = None, maximum: int = None, multiple_of: int = None) has no required parameters
ormar.Float(minimum: float = None, maximum: float = None, multiple_of: int = None) has no required parameters
ormar.Decimal(minimum: float = None, maximum: float = None, multiple_of: int = None, precision: int = None, scale: int = None, max_digits: int = None, decimal_places: int = None) has no required parameters
ormar.Date() has no required parameters
ormar.Time(timezone: bool = False) has no required parameters
ormar.DateTime(timezone: bool = False) has no required parameters
ormar.JSON() has no required parameters
ormar.LargeBinary(max_length) has a required max_length parameter
ormar.UUID(uuid_format: str = 'hex') has no required parameters
ormar.Enum(enum_class=Type[Enum]) has a required enum_class parameter
"""