import ormar
from db import Giveaway

from ormar.exceptions import ModelError


class GiveawayRepository:
    async def create(self, data: dict[str, any]) -> Giveaway:
        try:
            res = await Giveaway.objects.create(**data)
            return res
        except ModelError:
            return None

    async def get(self, giveaway_id=None) -> Giveaway:
        try:
            if giveaway_id:
                return await Giveaway.objects.get(message_id=giveaway_id)
            else:
                return await Giveaway.objects.all()
        except ormar.NoMatch:
            return None

    async def update(self, id, data) -> Giveaway:
        try:
            res = await Giveaway.objects.filter(message_id=id).update(**data)
            return res
        except ModelError:
            return None

    async def delete(self, id) -> Giveaway:
        try:
            res = await Giveaway.objects.delete(message_id=id)
            return res
        except ModelError:
            return None