from disnake.ext import commands, tasks


class GiveawayTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=2)
    async def clear_entries(self):
        ...

    @tasks.loop(seconds=10)
    async def update_giveaways(self):
        ...

    @tasks.loop(seconds=5)
    async def update_footer(self):
        ...