import disnake
import datetime

from disnake.ext import commands, tasks

from cogs.giveaway_functions import GiveawayFunctions
from db.database import Database


class GiveawayTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @tasks.loop(hours=2)
    async def clear_entries(self):
        entries = await self.db.get_all_giveaway_entries()
        for entry in entries:
            if entry[3] < datetime.datetime.now() - datetime.timedelta(days=14):
                await self.db.delete_giveaway_entries(entry[1])

    @tasks.loop(seconds=10)
    async def update_giveaways(self):
        giveaways = await self.db.get_all_giveaways()
        for giveaway in giveaways:
            if giveaway[8] < datetime.datetime.now() and giveaway[10] == "False":
                guild = self.bot.get_guild(giveaway[2])
                await GiveawayFunctions(self.bot).end_giveaway(giveaway[1], guild)

    @tasks.loop(seconds=5)
    async def update_footer(self):
        giveaways = await self.db.get_all_giveaways()
        for giveaway in giveaways:
            try:
                guild = self.bot.get_guild(giveaway[2])
                channel = guild.get_channel(giveaway[3])
                message = await channel.fetch_message(giveaway[1])
                embed = message.embeds[0]
                finally_count = await self.db.get_giveaway_entries(giveaway[1])
                embed.set_footer(text=f"Entries - {len(finally_count)}")
                await message.edit(embed=embed)
            except disnake.NotFound:
                if giveaway is not None:
                    await self.db.delete_giveaway(giveaway[1])

    @tasks.loop(hours=2)
    async def clear_entries(self):
        entries = await self.db.get_all_giveaway_entries()
        for entry in entries:
            if entry[3] < datetime.datetime.now() - datetime.timedelta(days=14):
                await self.db.delete_giveaway_entries(entry[1])

