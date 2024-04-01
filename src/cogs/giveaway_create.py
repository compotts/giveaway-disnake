import disnake
import datetime

from disnake.ext import commands

from .giveaway_functions import GiveawayFunction
from repositories import GiveawayRepository


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_db = GiveawayRepository()

    @commands.slash_command(name="giveaway")
    async def giveaway(self, interaction):
        ...

    @giveaway.sub_command(name="create", description="Создать розыгрыш")
    async def giveaway_create(self, 
        interaction: disnake.ApplicationCommandInteraction, 
        duration: str=commands.Param(description="Пример: 30m"), 
        winners: int=commands.Param(description="Кол-во победителей"),
        prize: str=commands.Param(description="Приз в розыгрыше"),
        voice=commands.Param(
            choices=["No", "Voice", "Tribune"],
            description="Необходимость быть в голосовом канале для участия",
        )):
        try:
            winners = int(winners)
        except ValueError:
            embed = disnake.Embed(
                title="Создание розыгрыша",
                description="Кол-во победителей должно быть числом",
                color=0x2F3136,
            )
            await interaction.response.send_message(
                embed=embed, 
                ephemeral=True
            )
            return
        start_time = datetime.datetime.now()
        duration = duration.lower()
        if duration.endswith("m"):
            minutes = int(duration[:-1])
            if minutes > 60:
                await interaction.response.send_message(
                    "Длительность не может быть больше 60 минут",
                    ephemeral=True
                )
                return
            end_time = start_time + datetime.timedelta(minutes=minutes)
        elif duration.endswith("h"):
            hours = int(duration[:-1])
            if hours > 24:
                await interaction.response.send_message(
                    "Длительность не может быть больше 24 часов",
                    ephemeral=True
                )
                return
            end_time = start_time + datetime.timedelta(hours=hours)
        elif duration.endswith("d"):
            days = int(duration[:-1])
            if days > 3:
                await interaction.response.send_message(
                    "Длительность не может быть больше 3 дней",
                    ephemeral=True
                )
                return
            end_time = start_time + datetime.timedelta(days=days)
        else:
            embed = disnake.Embed(
                title="Создание розыгрыша",
                description=f"{interaction.author.mention}, длительность должна быть в минутах, часах или днях",
                color=0x2F3136
            )
            await interaction.response.send_message(
                embed=embed, 
                ephemeral=True
            )
            return

        beautiful_end_time1 = disnake.utils.format_dt(
            end_time, 
            "R"
        )
        beautiful_end_time2 = disnake.utils.format_dt(
            end_time, 
            "f"
        )
        embed = disnake.Embed(
            title=f"Розыгрыш - {prize}",
            description=f"Завершается {beautiful_end_time1} ({beautiful_end_time2})",  
            color=0x2F3136
        )
        embed.set_footer(
            text=f"Участники - 0"
        )
        components = [
            disnake.ui.Button(
                style=disnake.ButtonStyle.blurple,
                label="Присоединиться",
                custom_id="giveaway_join",
            ),
            disnake.ui.Button(
                style=disnake.ButtonStyle.gray,
                label="Участники",
                custom_id="giveaway_entries",
            ),
        ]
        message = await interaction.channel.send(
            embed=embed, 
            components=components
        )
        await self.giveaway_db.create(
            data = {
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
            }
        )
        await interaction.response.send_message(
            embed=disnake.Embed(
                description="Вы успешно создали розыгрыш!",
                color=0x2F3136
            ),
            ephemeral=True,
        )
