import datetime

import disnake
from disnake.ext import commands

from cogs.giveaway_functions import GiveawayFunctions
from db.database import Database


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.slash_command(name="giveaway")
    async def giveaway(self, interaction):
        ...

    @giveaway.sub_command(name="create", description="Create giveaway")
    async def giveaway_create(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        duration: str = commands.Param(description="Example: 30m"),
        winners: int = commands.Param(description="Count of winners"),
        prize: str = commands.Param(description="Prize in the giveaway"),
        voice=commands.Param(
            choices=["No", "Voice", "Tribune"],
            description="The need to be in the voice channel",
        ),
    ):
        try:
            winers = int(winners)
        except ValueError:
            embed = disnake.Embed(title="Create giveaway", color=0x2F3136)
            embed.description = f"{interaction.author.mention}, Ошибка при конвертировании `{
                winners}` в кол.во победителей"
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        start_time = datetime.datetime.now()
        duration = duration.lower()
        if duration.endswith("m"):
            minutes = int(duration[:-1])
            if minutes > 60:
                await interaction.response.send_message(
                    "Продолжительность не должна превышать 60 минут", ephemeral=True
                )
                return
            end_time = start_time + datetime.timedelta(minutes=minutes)
        elif duration.endswith("h"):
            hours = int(duration[:-1])
            if hours > 24:
                await interaction.response.send_message(
                    "Продолжительность не должна превышать 24 часа", ephemeral=True
                )
                return
            end_time = start_time + datetime.timedelta(hours=hours)
        elif duration.endswith("d"):
            days = int(duration[:-1])
            if days > 1:
                await interaction.response.send_message(
                    "Продолжительность не должна превышать 1 день", ephemeral=True
                )
                return
            end_time = start_time + datetime.timedelta(days=days)
        else:
            embed = disnake.Embed(title="Create giveaway", color=0x2F3136)
            embed.description = f"{
                interaction.author.mention}, Неправильный формат продолжительности, пример: 30m, 1h, 1d"
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        beautiful_end_time1 = disnake.utils.format_dt(end_time, "R")
        beautiful_end_time2 = disnake.utils.format_dt(end_time, "f")
        embed = disnake.Embed(title=f"Giveaway - {prize}", color=0x2F3136)
        embed.description = f"- **Number of winners:** {winers}\n- **Ends at:** {
            beautiful_end_time1} ({beautiful_end_time2})"
        embed.set_footer(text=f"Entries - 0")
        components = [
            disnake.ui.Button(
                style=disnake.ButtonStyle.blurple,
                label="Join",
                custom_id="giveaway_join",
            ),
            disnake.ui.Button(
                style=disnake.ButtonStyle.gray,
                label="Entries",
                custom_id="giveaway_entries",
            ),
        ]
        message = await interaction.channel.send(embed=embed, components=components)
        await self.db.add_giveaway(
            message.id,
            interaction.guild.id,
            interaction.channel.id,
            interaction.author.id,
            prize,
            winers,
            start_time,
            end_time,
            str(voice),
            "False",
        )
        self.bot.loop.create_task(
            GiveawayFunctions(self.bot).start_giveaway(
                interaction.guild.id, message.id, end_time
            )
        )
        await interaction.response.send_message(
            embed=disnake.Embed(
                description="You have successfully created a giveaway!", color=0x2F3136
            ),
            ephemeral=True,
        )

