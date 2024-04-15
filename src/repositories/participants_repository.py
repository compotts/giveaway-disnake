import ormar
import ormar.exceptions
import db


class ParticipantRepository:
    async def create(self, giveaway_id: int, user_id: int, entry_time: str):
        """
        Creates a participant in the database
        Args:
            giveaway_id (int): The ID of the giveaway
            user_id (int): The ID of the user
            entry_time (str): The time the participant joined the giveaway
        :return: The created participant
        """
        try:
            res = await db.Participant.objects.create(
                giveaway_id=giveaway_id,
                user_id=user_id,
                entry_time=entry_time
            )
            return res
        except ormar.exceptions.ModelError:
            return None

    async def get(self, giveaway_id: int=None, user_id: int=None):
        """
        Gets a participant from the database
        Args:
            giveaway_id (int): The ID of the giveaway
            user_id (int): The ID of the user
        :return: The participant
        """
        try:
            if giveaway_id is not None and user_id is not None:
                to_return = await db.Participant.objects.get(giveaway_id=giveaway_id, user_id=user_id)
                if not to_return:
                    return None
                return to_return
            elif giveaway_id is not None:
                return await db.Participant.objects.filter(giveaway_id=giveaway_id).all()
            elif user_id is not None:
                return await db.Participant.objects.filter(user_id=user_id).all()
            else:
                return await db.Participant.objects.all()
        except ormar.NoMatch:
            return None

    async def delete(self, giveaway_id=None, user_id=None):
        try:
            if giveaway_id is not None and user_id is not None:
                return await db.Participant.objects.filter(giveaway_id=giveaway_id, user_id=user_id).delete()
            elif giveaway_id is not None:
                return await db.Participant.objects.filter(giveaway_id=giveaway_id).delete()
            elif user_id is not None:
                return await db.Participant.objects.filter(user_id=user_id).delete()
            else:
                return None
        except ormar.exceptions.ModelError:
            return None