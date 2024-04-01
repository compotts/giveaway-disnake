import disnake
import datetime
import asyncio
from disnake.ext import commands, tasks

from loguru import logger as log

from .giveaway_functions import GiveawayFunction
from repositories import GiveawayRepository, ParticipantRepository


class GiveawayTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_db = GiveawayRepository()
        self.participants_db = ParticipantRepository()

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(3)
        if not self.update_footer.is_running():
            self.update_footer.start()
            
        if not self.update_giveaways.is_running():
            self.update_giveaways.start()

        if not self.clear_entries.is_running():
            self.clear_entries.start()

    @tasks.loop(hours=2)
    async def clear_entries(self):
        entries = await self.participants_db.get_all()
        if not entries:
            return
        for participant in entries:
            if participant.entry_time < datetime.datetime.now() - datetime.timedelta(days=14):
                await self.participants_db.delete(
                    participant.giveaway_id
                )

    @tasks.loop(seconds=10)
    async def update_giveaways(self):
        giveaways = await self.giveaway_db.get_all()
        if not giveaways:
            return
        for giveaway in giveaways:
            if giveaway.end_time < datetime.datetime.now() and giveaway.status == "active":
                guild = self.bot.get_guild(
                    giveaway.guild_id
                )
                await GiveawayFunction(self.bot).end_giveaway(
                    giveaway.message_id, 
                    guild
                )

    @tasks.loop(seconds=5)
    async def update_footer(self):
        giveaways = await self.giveaway_db.get_all()
        if not giveaways:
            return
        for giveaway in giveaways:
            try:
                guild = self.bot.get_guild(
                    giveaway.guild_id
                )
                channel = guild.get_channel(
                    giveaway.channel_id
                )
                message = await channel.fetch_message(
                    giveaway.message_id
                )
                embed = message.embeds[0]
                finally_count = await self.participants_db.get_by_id(
                    giveaway.message_id
                )
                embed.set_footer(
                    text=f"Участники - {len(finally_count)}"
                )
                await message.edit(
                    embed=embed
                )
            except disnake.NotFound:
                if giveaway is not None:
                    await self.giveaway_db.delete(
                        giveaway.message_id
                    )
                    await self.participants_db.delete(
                        giveaway.message_id
                    )