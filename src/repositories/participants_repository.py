from db import Participant


class ParticipantRepository:
    async def create(self, data: dict[str, any]):
           res = await Participant.objects.create(**data)
           return res
    
    async def get(self, id):
        res = await Participant.objects.get(message_id=id)
        return res
    
    async def get_by_id(self, id):
        res = await Participant.objects.filter(giveaway_id=id).all()
        return res

    async def update(self, id, data):
        res = await Participant.objects.update(giveaway_id=id, **data)
        return res
    
    async def delete(self, id):
        res = await Participant.objects.delete(giveaway_id=id)
        return res
    
    async def delete_by_ids(self, id, id2):
        res = await Participant.objects.filter(id=id, id2=id2).delete()
        return res
    
    async def delete_by_id(self, id):
        res = await Participant.objects.filter(id=id).delete()
        return res
