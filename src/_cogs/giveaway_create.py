import disnake
import datetime

from disnake.ext import commands

from .giveaway_functions import GiveawayFunction
from repositories import GiveawayRepository


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = GiveawayRepository()

    @commands.slash_command(name="giveaway")
    async def giveaway(self, interaction):
        ...

    @giveaway.sub_command(name="create", description="Create giveaway")
    async def giveaway_create(self, 
        interaction: disnake.ApplicationCommandInteraction, 
        duration: str=commands.Param(description="Example: 30m"), 
        winners: int=commands.Param(description="Count of winners"), 
        prize: str=commands.Param(description="Prize in the giveaway"),
        voice=commands.Param(
            choices=["No", "Voice", "Tribune"],
            description="The need to be in the voice channel",
        )):
        try:
            winners = int(winners)
        except ValueError:
            embed = disnake.Embed(
                title="Create giveaway",
                description="Count of winners must be an integer",
                color=0x2F3136,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        start_time = datetime.datetime.now()
        duration = duration.lower()
        if duration.endswith("m"):
            minutes = int(duration[:-1])
            if minutes > 60:
                await interaction.response.send_message(
                    "Duration must be less than 60 minutes", ephemeral=True
                )
                return
            end_time = start_time + datetime.timedelta(minutes=minutes)
        elif duration.endswith("h"):
            hours = int(duration[:-1])
            if hours > 24:
                await interaction.response.send_message(
                    "Duration must be less than 24 hours", ephemeral=True
                )
                return
            end_time = start_time + datetime.timedelta(hours=hours)
        elif duration.endswith("d"):
            days = int(duration[:-1])
            if days > 3:
                await interaction.response.send_message(
                    "Duration must be less than 3 days", ephemeral=True
                )
                return
            end_time = start_time + datetime.timedelta(days=days)
        else:
            embed = disnake.Embed(
                title="Create giveaway",
                description=f"{interaction.author.mention}, duration must be in minutes, hours or days",
                color=0x2F3136
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        beautiful_end_time1 = disnake.utils.format_dt(end_time, "R")
        beautiful_end_time2 = disnake.utils.format_dt(end_time, "f")
        embed = disnake.Embed(
            title=f"Giveaway - {prize}", 
            description=f"Ends {beautiful_end_time1} ({beautiful_end_time2})",  
            color=0x2F3136
        )
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

        await self.db.create(data = {
            "message_id": message.id,
            "channel_id": interaction.channel.id,
            "guild_id": interaction.guild.id,
            "hoster_id": interaction.author.id,
            "prize": prize,
            "winers": winners,
            "start_time": start_time,
            "end_time": end_time,
            "voice_needed": voice,
            "status": "active",
        })
        self.bot.loop.create_task(
            GiveawayFunction(self.bot).start_giveaway(
                interaction.guild.id, 
                message.id, 
                end_time
            )
        )
        await interaction.response.send_message(
            embed=disnake.Embed(
                description="You have successfully created a giveaway!", 
                color=0x2F3136
            ),
            ephemeral=True,
        )
