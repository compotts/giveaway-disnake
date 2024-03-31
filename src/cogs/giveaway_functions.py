import asyncio
import datetime
import random

import disnake
from disnake.ext import commands

from repositories import GiveawayRepository, ParticipantRepository


class GiveawayFunction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_db = GiveawayRepository()
        self.participants_db = ParticipantRepository()

    async def choose_winners(self, giveaway_id):
        entries = await self.participants_db.get_by_id(giveaway_id)
        giveaway = await self.giveaway_db.get(giveaway_id)
        winners_count = int(giveaway.winers)
        winners = random.sample(
            entries, 
            min(winners_count, len(entries))
        )
        return winners

    async def end_giveaway(self, giveaway_id, guild):
        giveaway = await self.giveaway_db.get(giveaway_id)
        if not giveaway:
            return
        guild = self.bot.get_guild(
            giveaway.guild_id
        )
        channel = guild.get_channel(
            giveaway.channel_id
        )
        if channel is None:
            return
        message = await channel.fetch_message(
            giveaway.message_id
        )
        embed = message.embeds[0]
        ended_time = disnake.utils.format_dt(
            datetime.datetime.now(), 
            "R"
        )
        ended_time_full = disnake.utils.format_dt(
            datetime.datetime.now(), 
            "F"
        )
        winners = await self.choose_winners(
            giveaway.message_id
        )
        if winners:
            winners_mentions = ", ".join(
                [f"<@{winner[2]}>" for winner in winners]
            )
            await message.reply(
                f"Поздравляем {winners_mentions}! Вы выиграли {giveaway.prize}!"
            )
            embed.description = (
                f"- Победитель: {winners_mentions}\n- Завершено: {ended_time} ({ended_time_full})" 
            )
        else:
            await message.reply(
                "Никто не присоединился к розыгрышу."
            )
            embed.description = (
                f"- Нету победителей\n- Завершено: {ended_time} ({ended_time_full})"
            )
        await message.edit(
            embed=embed,
            components=[
                disnake.ui.Button(
                    style=disnake.ButtonStyle.gray,
                    label="Участники",
                    custom_id="giveaway_entries",
                ),
                disnake.ui.Button(
                    style=disnake.ButtonStyle.gray,
                    label="Перевыбрать",
                    custom_id="giveaway_reroll",
                ),
            ],
        )
        await self.giveaway_db.update_custom(
            giveaway.message_id, 
            "status", 
            "ended"
        )

    async def start_giveaway(self, guild, giveaway_id, end_time):
        sleep_seconds = (end_time - datetime.datetime.now()).total_seconds()
        if sleep_seconds > 0:
            await asyncio.sleep(round(sleep_seconds))
            await self.end_giveaway(
                giveaway_id, 
                guild
            )

    async def check_if_user_in_voice_channel(self, interaction: disnake.MessageInteraction):
        member = interaction.guild.get_member(
            interaction.author.id
        )
        if member and member.voice:
            if not isinstance(member.voice.channel, disnake.StageChannel):
                return True
        return False

    async def check_if_user_on_tribune(self, interaction: disnake.MessageInteraction):
        member = interaction.guild.get_member(
            interaction.author.id
        )
        if member and member.voice:
            if isinstance(member.voice.channel, disnake.StageChannel):
                return True
        return False
