import ormar

from enum import Enum

from db import base_ormar_config

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


class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"


class Giveaway(ormar.Model):
    ormar_config = base_ormar_config.copy(
        tablename="giveaways",
    )

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    name: str = ormar.Text(max_length=64)
    description: str = ormar.Text(max_length=1024)
    prize: str = ormar.String(max_length=1024)
    start_time: int = ormar.DateTime()
    end_time: int = ormar.DateTime()
    winners: int = ormar.Integer()
    voice: str = ormar.String(max_length=64)
    ended: StatusEnum = ormar.Enum(enum_class=StatusEnum)


class GiveawayEntry(ormar.Model):
    ormar_config = base_ormar_config.copy(
        tablename="giveaway_entries",
    )

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    giveaway_id: int = ormar.Integer()
    user_id: int = ormar.Integer()
    entry_time: int = ormar.DateTime()


class Example(ormar.Model):
    ormar_config = base_ormar_config.copy(
        tablename="example",
    )

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    name: str = ormar.Text(max_length=64)