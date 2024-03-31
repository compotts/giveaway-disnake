from db import Giveaway


class GiveawayRepository:
    async def create(self, data: dict[str, any]):
           res = await Giveaway.objects.create(**data)
           return res
    
    async def get(self, id):
        res = await Giveaway.objects.get(message_id=id)
        return res

    async def update(self, id, data):
        res = await Giveaway.objects.update(id=id, **data)
        return res
    
    async def update_custom(self, id, column, new_value):
        res = await Giveaway.objects.filter(message_id=id).update(**{column: new_value})
        return res

    
    async def delete(self, id):
        res = await Giveaway.objects.delete(id=id)
        return res