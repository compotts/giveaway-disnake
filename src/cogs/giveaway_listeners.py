import disnake
import datetime
from disnake.ext import commands

from ._entries_paginator import EntriePaginator
from .giveaway_functions import GiveawayFunction

from repositories import GiveawayRepository, ParticipantRepository


class GiveawayListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_db = GiveawayRepository()
        self.participants_db = ParticipantRepository()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        if (before.channel is not None and not after.channel is not None) or (isinstance(before.channel, disnake.StageChannel) and not isinstance(after.channel, disnake.StageChannel)):
            entries = await self.participants_db.get_by_user_id(member.id)
            if not entries:
                return
            for entry in entries:
                giveaway = await self.giveaway_db.get(entry.giveaway_id)
                if not giveaway:
                    return
                if giveaway.voice_needed == "Voice" and before.channel is not None and not after.channel is not None:
                    await self.participants_db.delete_by_ids(entry.giveaway_id, member.id)
                elif giveaway.voice_needed == "Tribune" and isinstance(before.channel, disnake.StageChannel) and not isinstance(after.channel, disnake.StageChannel):
                    await self.participants_db.delete_by_ids(entry.giveaway_id, member.id)

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        if interaction.component.custom_id == "giveaway_join":
            giveaway = await self.giveaway_db.get(interaction.message.id)
            if not giveaway or giveaway.end_time < datetime.datetime.now():
                embed = disnake.Embed(
                    description="Розыгрыш уже окончен!", 
                    color=0x2F3136
                )
                await interaction.response.send_message(
                    embed=embed, 
                    ephemeral=True
                )
                return
            if giveaway.voice_needed == "Voice":
                if not await GiveawayFunction(self.bot).check_if_user_in_voice_channel(interaction):
                    embed = disnake.Embed(
                        description="Вы должны находится в голосовом канале для участия!", 
                        color=0x2F3136
                    )
                    await interaction.response.send_message(
                        embed=embed, 
                        ephemeral=True
                    )
                    return
            elif giveaway.voice_needed == "Tribune":
                if not await GiveawayFunction(self.bot).check_if_user_on_tribune(interaction):
                    embed = disnake.Embed(
                        description="Вы должны находится на трибуне для участия!", 
                        color=0x2F3136
                    )
                    await interaction.response.send_message(
                        embed=embed, 
                        ephemeral=True
                    )
                    return
            entry = await self.participants_db.get_by_id_and_user_id(
                interaction.message.id, 
                interaction.author.id
            )
            if entry:
                embed = disnake.Embed(
                    description=f"{interaction.author.mention}, Вы **покинули** розыгрыш!", 
                    color=0x2F3136
                )
                await interaction.response.send_message(
                    embed=embed, 
                    ephemeral=True
                )
                await self.participants_db.delete(
                    interaction.message.id
                )
            else:
                embed = disnake.Embed(
                    description=f"{interaction.author.mention}, Вы ** присоединились** к розыгрышу!",
                    color=0x2F3136
                )
                await interaction.response.send_message(
                    embed=embed, 
                    ephemeral=True
                )
                await self.participants_db.create(data = {
                    "giveaway_id": interaction.message.id,
                    "user_id": interaction.author.id,
                    "entry_time": datetime.datetime.now(),
                })

        elif interaction.component.custom_id == "giveaway_entries":
            entries = await self.participants_db.get(interaction.message.id)
            if not entries:
                embed = disnake.Embed(
                    description="В розыгрыше нету участников!",
                    color=0x2F3136
                )
                await interaction.response.send_message(
                    embed=embed, 
                    ephemeral=True
                )
                return
            embeds = []
            for page_number, i in enumerate(range(0, len(entries), 25), start=1):
                entries_mentions = "\n".join(
                    [f"{index}) <@{entry.user_id}>" for index, entry in enumerate(entries[i:i+25], start=(page_number - 1) * 25)]
                )
                embed = disnake.Embed(
                    title=f"Участники, всего {len(entries)}",
                    description=f"{entries_mentions}",
                    color=0x2F3136
                ).set_thumbnail(
                    url=interaction.author.avatar.url if interaction.author.avatar else interaction.author.default_avatar.url
                )
                embeds.append(embed)
            paginator = EntriePaginator(embeds)
            await interaction.response.send_message(
                embed=embeds[0],
                view=paginator,
                ephemeral=True
            )
                
        elif interaction.component.custom_id == "giveaway_reroll":
            if not interaction.author.guild_permissions.administrator:
                embed = disnake.Embed(
                    description="Вы не можете выполнить это действие!", 
                    color=0x2F3136
                )
                await interaction.response.send_message(
                    embed=embed, 
                    ephemeral=True
                )
                return 
            winners = await GiveawayFunction(self.bot).choose_winners(interaction.message.id)
            giveaway = await self.giveaway_db.get(
                interaction.message.id
            )
            ended_time = disnake.utils.format_dt(
                datetime.datetime.now(), 
                "R"
            )
            ended_time_full = disnake.utils.format_dt(
                datetime.datetime.now(), 
                "F"
            )
            embed_message = interaction.message.embeds[0]
            if winners:
                winners_mentions = ", ".join(
                    [f"<@{winner.user_id}>" for winner in winners]
                )
                await interaction.message.reply(
                    f"Поздравляем {winners_mentions}! Вы выиграли {giveaway.prize}!"
                )
                embed_message.description = (
                    f"- Новый победитель: {winners_mentions}\n- Завершено: {ended_time} ({ended_time_full})"
                )
            else:
                await interaction.message.reply(
                    "Никто не присоединился к розыгрышу."
                )
                embed_message.description = (
                    f"- Нету победителей\n- Завершено: {ended_time} ({ended_time_full})"
                )
            embed_rerolled = disnake.Embed(
                description="Победитель был перевыбран!",
                color=0x2F3136
            )
            await interaction.response.send_message(
                embed=embed_rerolled, 
                ephemeral=True
            )
            await interaction.message.edit(
                embed=embed_message,
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

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: disnake.RawMessageDeleteEvent):
        giveaway = await self.giveaway_db.get(payload.message_id)
        if not giveaway:
            return
        await self.giveaway_db.delete(payload.message_id)
        await self.participants_db.delete(payload.message_id)