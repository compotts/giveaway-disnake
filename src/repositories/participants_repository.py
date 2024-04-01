import ormar
from db import Participant


class ParticipantRepository:
    # async def create(self, data: dict[str, any]):
    #        res = await Participant.objects.create(**data)
    #        return res
    
    # async def get(self, id):
    #     try:
    #         res = await Participant.objects.filter(giveaway_id=id).all()
    #         return res
    #     except ormar.NoMatch:
    #         return None
    
    # async def get_all(self):
    #     try:
    #         res = await Participant.objects.all()
    #         return res
    #     except ormar.NoMatch:
    #         return None

    # async def get_by_id(self, id):
    #     try:
    #         res = await Participant.objects.filter(giveaway_id=id).all()
    #         return res
    #     except ormar.NoMatch:
    #         return None
    
    # async def get_by_user_id(self, user_id):
    #     try:
    #         res = await Participant.objects.filter(user_id=user_id).all()
    #         return res
    #     except ormar.NoMatch:
    #         return None
    
    # async def get_by_id_and_user_id(self, id, user_id):
    #     try:
    #         res = await Participant.objects.filter(giveaway_id=id, user_id=user_id).all()
    #         return res
    #     except ormar.NoMatch:
    #         return None

    # async def update(self, id, data):
    #     res = await Participant.objects.update(giveaway_id=id, **data)
    #     return res
    
    # async def delete(self, id):
    #     res = await Participant.objects.filter(giveaway_id=id).delete()
    #     return res
    
    # async def delete_by_ids(self, id, user_id):
    #     res = await Participant.objects.filter(giveaway_id=id, user_id=user_id).delete()
    #     return res


    async def create(self, data: dict[str, any]):
        try:
            res = await Participant.objects.create(**data)
            return res
        except ormar.ModelError:
            return None

    async def get(self, id=None, user_id=None):
        try:
            if id:
                return await Participant.objects.filter(giveaway_id=id).all()
            elif user_id:
                return await Participant.objects.filter(user_id=user_id).all()
            else:
                return await Participant.objects.all()
        except ormar.NoMatch:
            return None

    async def delete(self, id=None, user_id=None):
        try:
            if id and user_id:
                return await Participant.objects.filter(giveaway_id=id, user_id=user_id).delete()
            elif id:
                return await Participant.objects.filter(giveaway_id=id).delete()
            elif user_id:
                return await Participant.objects.filter(user_id=user_id).delete()
            else:
                return None
        except ormar.ModelError:
            return None