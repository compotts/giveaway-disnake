import disnake
import repositories

from . import views
from disnake.ext import commands



class GiveawayListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False
        self.giveaway_db = repositories.GiveawayRepository()
        self.participants_db = repositories.ParticipantRepository()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        if (before.channel is not None and not after.channel is not None) or (isinstance(before.channel, disnake.StageChannel) and not isinstance(after.channel, disnake.StageChannel)):
            entries = await self.participants_db.get(
                user_id=member.id
            )
            if not entries:
                return
            for entry in entries:
                giveaway = await self.giveaway_db.get(
                    id=entry.giveaway_id
                )
                if not giveaway:
                    return
                if giveaway.voice_needed == "Voice" and before.channel is not None and not after.channel is not None:
                    await self.participants_db.delete(
                        id=entry.giveaway_id, 
                        user_id=member.id
                    )
                elif giveaway.voice_needed == "Tribune" and isinstance(before.channel, disnake.StageChannel) and not isinstance(after.channel, disnake.StageChannel):
                    await self.participants_db.delete(
                        id=entry.giveaway_id, 
                        user_id=member.id
                    )

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: disnake.RawMessageDeleteEvent):
        giveaway = await self.giveaway_db.get(id=payload.message_id)
        if not giveaway:
            return
        await self.giveaway_db.delete(id=payload.message_id)
        await self.participants_db.delete(id=payload.message_id)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.persistent_views_added:
            self.bot.add_view(views.GiveawayCreateView(self.bot))
            self.bot.add_view(views.GiveawayRerollView(self.bot))
            self.persistent_views_added = True