import disnake
from disnake.ext import commands


class GiveawayTwo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="giveawaytwo")
    async def giveawaytwo(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_message(
            "Hello, world!", ephemeral=True
        )