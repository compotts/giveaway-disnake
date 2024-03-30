import disnake
from disnake.ext import commands

from db.functions import GiveawayRepository


class GiveawayTwo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = GiveawayRepository()

    @commands.slash_command(name="giveawaytwo")
    async def giveawaytwo(self, interaction: disnake.ApplicationCommandInteraction):
        await self.db.example("шлюха тупая")
        await interaction.response.send_message(
            "Hello, world!", ephemeral=True
        )