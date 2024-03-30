import disnake
from disnake.ext import commands

from db.functions import GiveawayRepository


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = GiveawayRepository()

    @commands.slash_command(name="giveaway")
    async def giveaway(self, interaction: disnake.ApplicationCommandInteraction):
        await self.db.example_create("шлюха тупая")
        await interaction.response.send_message(
            "Hello, world!", ephemeral=True
        )