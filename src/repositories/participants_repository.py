import ormar
import ormar.exceptions
import db


class ParticipantRepository:
    async def create(self, data: dict[str, any]):
        try:
            res = await db.Participant.objects.create(**data)
            return res
        except ormar.exceptions.ModelError:
            return None

    async def get(self, id=None, user_id=None):
        try:
            if id is not None and user_id is not None:
                to_return = await db.Participant.objects.get(giveaway_id=id, user_id=user_id)
                print(to_return)
                if not to_return:
                    return None
                return to_return
            elif id is not None:
                return await db.Participant.objects.filter(giveaway_id=id).all()
            elif user_id is not None:
                return await db.Participant.objects.filter(user_id=user_id).all()
            else:
                return await db.Participant.objects.all()
        except ormar.NoMatch:
            return None

    async def delete(self, id=None, user_id=None):
        try:
            if id is not None and user_id is not None:
                return await db.Participant.objects.filter(giveaway_id=id, user_id=user_id).delete()
            elif id is not None:
                return await db.Participant.objects.filter(giveaway_id=id).delete()
            elif user_id is not None:
                return await db.Participant.objects.filter(user_id=user_id).delete()
            else:
                return None
        except ormar.exceptions.ModelError:
            return None