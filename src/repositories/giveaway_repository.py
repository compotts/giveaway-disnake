import ormar
from db import Giveaway

from ormar.exceptions import ModelError


class GiveawayRepository:
    # async def create(self, data: dict[str, any]):
    #        res = await Giveaway.objects.create(**data)
    #        return res
    
    # async def get(self, id):
    #     try:
    #         res = await Giveaway.objects.get(message_id=id)
    #         return res
    #     except ormar.NoMatch:
    #         return None
        
    # async def get_all(self):
    #     try:
    #         res = await Giveaway.objects.all()
    #         return res
    #     except ormar.NoMatch:
    #         return None

    # async def update(self, id, data):
    #     res = await Giveaway.objects.update(id=id, **data)
    #     return res
    
    # async def update_custom(self, id, column, new_value):
    #     res = await Giveaway.objects.filter(message_id=id).update(**{column: new_value})
    #     return res

    # async def delete(self, id):
    #     res = await Giveaway.objects.delete(message_id=id)
    #     return res

    async def create(self, data: dict[str, any]):
        try:
            res = await Giveaway.objects.create(**data)
            return res
        except ModelError:
            return None

    async def get(self, id=None):
        try:
            if id:
                return await Giveaway.objects.get(message_id=id)
            else:
                return await Giveaway.objects.all()
        except ormar.NoMatch:
            return None

    async def update(self, id, data):
        try:
            res = await Giveaway.objects.filter(message_id=id).update(**data)
            return res
        except ModelError:
            return None

    async def delete(self, id):
        try:
            res = await Giveaway.objects.delete(message_id=id)
            return res
        except ModelError:
            return None