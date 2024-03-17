import asyncio
import datetime
import random

import disnake
from disnake.ext import commands, tasks

from database.database import Database


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    async def choose_winners(self, giveaway_id):
        entries = await self.db.get_giveaway_entries(giveaway_id)
        giveaway = await self.db.get_giveaway(giveaway_id)
        winners_count = int(giveaway[0][6])
        winners = random.sample(entries, min(winners_count, len(entries)))
        return winners

    async def end_giveaway(self, giveaway_id, guild):
        giveaway = await self.db.get_giveaway(giveaway_id)
        if not giveaway:
            return
        guild = self.bot.get_guild(giveaway[0][2])
        channel = guild.get_channel(giveaway[0][3])
        if channel is None:
            return
        message = await channel.fetch_message(giveaway[0][1])
        embed = message.embeds[0]
        ended_time = disnake.utils.format_dt(datetime.datetime.now(), "R")
        ended_time_full = disnake.utils.format_dt(datetime.datetime.now(), "F")
        winners = await self.choose_winners(giveaway[0][1])
        if winners:
            winners_mentions = ", ".join([f"<@{winner[2]}>" for winner in winners])
            await message.reply(f"Congratulations {winners_mentions}! You have won {giveaway[0][5]}!")
            embed.description = f"- Winners: {winners_mentions}\n- Ended: {ended_time} ({ended_time_full})"
        else:
            await message.reply("No one entered the giveaway.")
            embed.description = f"- No winners\n- Ended: {ended_time} ({ended_time_full})"
        await message.edit(embed=embed, components=[disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Entries", custom_id="giveaway_entries")])
        await self.db.delete_giveaway(giveaway[0][1])

    async def start_giveaway(self, guild, giveaway_id, end_time):
        sleep_seconds = (end_time - datetime.datetime.now()).total_seconds()
        print(round(sleep_seconds))
        if sleep_seconds > 0:
            await asyncio.sleep(round(sleep_seconds))
            await self.end_giveaway(giveaway_id, guild)

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
            if giveaway[8] < datetime.datetime.now():
                guild = self.bot.get_guild(giveaway[2])
                await self.end_giveaway(giveaway[1], guild)

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(2)
        if not self.update_giveaways.is_running():
            self.update_giveaways.start()
            print("Giveaways loop started")
        if not self.clear_entries.is_running():
            self.clear_entries.start()
            print("Entries clear loop started")

    @commands.slash_command(name="giveaway")
    async def giveaway(self, interaction):
        ...

    @giveaway.sub_command(name="create", description="Create giveaway")
    async def giveaway_create(self, 
                              interaction: disnake.ApplicationCommandInteraction, 
                              duration: str=commands.Param(description="Example: 30m"), 
                              winners: int=commands.Param(description="Count of winners"), 
                              prize: str=commands.Param(description="Prize in the giveaway"),
                              voice=commands.Param(choices=["No", "Voice", "Tribune"], description="The need to be in the voice channel")):

        try:
            winers = int(winners)
        except ValueError:
            embed = disnake.Embed(title="Create giveaway", color=0x2F3136)
            embed.description = f"{interaction.author.mention}, Ошибка при конвертировании `{winners}` в кол.во победителей"
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        start_time = datetime.datetime.now()
        duration = duration.lower()
        if duration.endswith('m'):
            minutes = int(duration[:-1])
            if minutes > 60:
                await interaction.response.send_message("Продолжительность не должна превышать 60 минут", ephemeral=True)
                return
            end_time = start_time + datetime.timedelta(minutes=minutes)
        elif duration.endswith('h'):
            hours = int(duration[:-1])
            if hours > 24:
                await interaction.response.send_message("Продолжительность не должна превышать 24 часа", ephemeral=True)
                return
            end_time = start_time + datetime.timedelta(hours=hours)
        elif duration.endswith('d'):
            days = int(duration[:-1])
            if days > 1:
                await interaction.response.send_message("Продолжительность не должна превышать 1 день", ephemeral=True)
                return
            end_time = start_time + datetime.timedelta(days=days)
        else:
            embed = disnake.Embed(title="Create giveaway", color=0x2F3136)
            embed.description = f"{interaction.author.mention}, Неправильный формат продолжительности, пример: 30m, 1h, 1d"
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        

        beautiful_end_time1 = disnake.utils.format_dt(end_time, "R")
        beautiful_end_time2 = disnake.utils.format_dt(end_time, "f")
        embed = disnake.Embed(title=f"Giveaway - {prize}", color=0x2F3136)
        embed.description=f"- **Number of winners:** {winers}\n- **Ends at:** {beautiful_end_time1} ({beautiful_end_time2})"
        embed.set_footer(text=f"Entries - 0")
        components = [
            disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Join", custom_id="giveaway_join"),
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Entries", custom_id="giveaway_entries")
        ]
        message = await interaction.channel.send(embed=embed, components=components)
        await self.db.add_giveaway(message.id, interaction.guild.id,
                                   interaction.channel.id, 
                                   interaction.author.id, 
                                   prize, winers, start_time, end_time, str(voice))
        self.bot.loop.create_task(self.start_giveaway(interaction.guild.id, message.id, end_time))
        await interaction.response.send_message(embed=disnake.Embed(description="Вы успешно создали розыгрыш!", color=0x2F3136), ephemeral=True)