import ormar
import datetime

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
    start_time: str = ormar.Text()
    end_time: str = ormar.Text()
    voice_needed: VoiceEnum = ormar.Enum(enum_class=VoiceEnum)
    status: StatusEnum = ormar.Enum(enum_class=StatusEnum)


class Participant(ormar.Model):
    ormar_config = base_ormar_config.copy(
        tablename="giveaway_entries",
    )

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    giveaway_id: int = ormar.BigInteger()
    user_id: int = ormar.BigInteger()
    entry_time: str = ormar.Text()