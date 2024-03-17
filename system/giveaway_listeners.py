import disnake
import asyncio
import datetime

from disnake.ext import commands, tasks
from typing import List

from database.database import Database


class EntriesPaginator(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.index = 0

        self._update_state()

    def _update_state(self) -> None:
        self.prev_page.disabled = self.index == 0
        self.next_page.disabled = self.index == len(self.embeds) - 1

    @disnake.ui.button(label="<<", style=disnake.ButtonStyle.secondary)
    async def prev_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.index -= 1
        self._update_state()

        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(label=">>", style=disnake.ButtonStyle.secondary)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.index += 1
        self._update_state()

        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)


class GiveawayListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    async def check_if_user_in_voice_channel(self, interaction):
        member = interaction.guild.get_member(interaction.author.id)
        if member and member.voice:
            if not isinstance(member.voice.channel, disnake.StageChannel):
                return True
        return False

    async def check_if_user_on_tribune(self, interaction):
        member = interaction.guild.get_member(interaction.author.id)
        if member and member.voice:
            if isinstance(member.voice.channel, disnake.StageChannel):
                return True
        return False

    @tasks.loop(seconds=5)
    async def update_footer(self):
        giveaways = await self.db.get_all_giveaways()
        for giveaway in giveaways:
            guild = self.bot.get_guild(giveaway[2])
            channel = guild.get_channel(giveaway[3])
            message = await channel.fetch_message(giveaway[1])
            embed = message.embeds[0]
            finally_count = await self.db.get_giveaway_entries(giveaway[1])
            embed.set_footer(text=f"Entries - {len(finally_count)}")
            await message.edit(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(2)
        if not self.update_footer.is_running():
            self.update_footer.start()
            print("Update footer loop started")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (before.channel is not None and not after.channel is not None) or (isinstance(before.channel, disnake.StageChannel) and not isinstance(after.channel, disnake.StageChannel)):
            entries = await self.db.get_user_giveaway_entries(member.id)
            if not entries:
                return
            for entry in entries:
                giveaway = await self.db.get_giveaway(entry[1])
                if not giveaway:
                    return
                if giveaway[0][9] == "Voice" and before.channel is not None and not after.channel is not None:
                    await self.db.delete_user_giveaway_entries(entry[1], member.id)
                elif giveaway[0][9] == "Tribune" and isinstance(before.channel, disnake.StageChannel) and not isinstance(after.channel, disnake.StageChannel):
                    await self.db.delete_user_giveaway_entries(entry[1], member.id)

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        if interaction.component.custom_id == "giveaway_join":
            message = await self.db.get_giveaway(interaction.message.id)
            if not message or message[0][8] < datetime.datetime.now():
                embed = disnake.Embed(description="The giveaway has already ended!", color=0x2F3136)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            if message[0][9] == "Tribune":
                if not await self.check_if_user_on_tribune(interaction):
                    embed = disnake.Embed(description="You must be on a tribune to join the giveaway!", color=0x2F3136)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
            elif message[0][9] == "Voice":
                if not await self.check_if_user_in_voice_channel(interaction):
                    embed = disnake.Embed(description="You must be in a voice channel to join the giveaway!", color=0x2F3136)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
            entry = await self.db.get_user_giveaway_entry(interaction.message.id, interaction.author.id)
            if entry:
                embed = disnake.Embed(description=f"{interaction.author.mention}, You ** left** the giveaway!", color=0x2F3136)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                await self.db.delete_user_giveaway_entries(interaction.message.id, interaction.author.id)
            else:
                await self.db.add_giveaway_entry(interaction.message.id, interaction.author.id, datetime.datetime.now())
                embed = disnake.Embed(description=f"{interaction.author.mention}, You **entered** the giveaway!", color=0x2F3136)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif interaction.component.custom_id == "giveaway_entries":
            entries = await self.db.get_giveaway_entries(interaction.message.id)
            if not entries:
                embed = disnake.Embed(description="No one entered the giveaway.", color=0x2F3136)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embeds = []
                for i in range(0, len(entries), 10):
                    entries_mentions = "\n".join([f"{i+1}) <@{entry[2]}>" for i, entry in enumerate(entries[i:i+10])])
                    embed = disnake.Embed(title=f"Participants of the giveaway, total {len(entries)}", description=entries_mentions, color=0x2F3136)
                    embed.set_thumbnail(url=interaction.author.avatar.url if interaction.author.avatar else interaction.author.default_avatar.url)
                    embeds.append(embed)
                await interaction.response.send_message(embed=embeds[0], view=EntriesPaginator(embeds), ephemeral=True)


    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        giveaway = await self.db.get_giveaway(payload.message_id)
        if giveaway:
            await self.db.delete_giveaway(payload.message_id)
            await self.db.delete_giveaway_entries(payload.message_id)