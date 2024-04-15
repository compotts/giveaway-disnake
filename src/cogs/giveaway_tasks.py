import disnake
import datetime
import asyncio
import repositories

from disnake.ext import commands, tasks
from . import giveaway_functions


class GiveawayTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_db = repositories.GiveawayRepository()
        self.participants_db = repositories.ParticipantRepository()

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.update_footer.is_running():
            self.update_footer.start()
            
        if not self.update_giveaways.is_running():
            self.update_giveaways.start()

        if not self.clear_entries.is_running():
            self.clear_entries.start()

    @tasks.loop(hours=2)
    async def clear_entries(self):
        entries = await self.participants_db.get()
        if not entries:
            return
        for participant in entries:
            if datetime.datetime.strptime(participant.entry_time, "%Y-%m-%d %H:%M:%S") < datetime.datetime.now() - datetime.timedelta(days=14):
                await self.participants_db.delete(
                    id=participant.giveaway_id
                )

    @tasks.loop(seconds=5)
    async def update_giveaways(self):
        giveaways = await self.giveaway_db.get()
        if not giveaways:
            return
        for giveaway in giveaways:
            if datetime.datetime.strptime(giveaway.end_time, "%Y-%m-%d %H:%M:%S") < datetime.datetime.now() and giveaway.status == "active":
                guild = self.bot.get_guild(
                    giveaway.guild_id
                )
                await giveaway_functions.GiveawayFunction(self.bot).end_giveaway(
                    giveaway.message_id, 
                    guild
                )

    @tasks.loop(seconds=5)
    async def update_footer(self):
        giveaways = await self.giveaway_db.get()
        if not giveaways:
            return
        for giveaway in giveaways:
            if giveaway.status == "ended":
                continue
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
                finally_count = await self.participants_db.get(
                    giveaway_id=giveaway.message_id
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
                        id=giveaway.message_id
                    )
                    await self.participants_db.delete(
                        id=giveaway.message_id
                    )