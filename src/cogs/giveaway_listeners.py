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
                    await self.participants_db.delete_by_id_and_user_id(entry.giveaway_id, member.id)
                elif giveaway.voice_needed == "Tribune" and isinstance(before.channel, disnake.StageChannel) and not isinstance(after.channel, disnake.StageChannel):
                    await self.participants_db.delete_by_id_and_user_id(entry.giveaway_id, member.id)

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
                    interaction.message.id, 
                    interaction.author.id
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
            ...

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: disnake.RawMessageDeleteEvent):
        giveaway = await self.giveaway_db.get(payload.message_id)
        if not giveaway:
            return
        await self.giveaway_db.delete(payload.message_id)
        await self.participants_db.delete(payload.message_id)