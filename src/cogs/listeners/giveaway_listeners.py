import disnake
import asyncio
import datetime

from cogs.giveaway_tasks import GiveawayTasks
from cogs.giveaway_functions import GiveawayFunctions

from disnake.ext import commands
from cogs._entriesPaginator import EntriesPaginator

from database.database import Database

from loguru import logger



class GiveawayListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(2)
        if not GiveawayTasks.update_footer.is_running():
            GiveawayTasks.update_footer.start(self)
            logger.info("Update footer loop started")
        if not GiveawayTasks.update_giveaways.is_running():
            GiveawayTasks.update_giveaways.start(self)
            logger.info("Update giveaways loop started")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
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
                if not await GiveawayFunctions(self.bot).check_if_user_on_tribune(interaction):
                    embed = disnake.Embed(description="You must be on a tribune to join the giveaway!", color=0x2F3136)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
            elif message[0][9] == "Voice":
                if not await GiveawayFunctions(self.bot).check_if_user_in_voice_channel(interaction):
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
                for i in range(0, len(entries), 50):
                    entries_mentions = "\n".join([f"{i+1}) <@{entry[2]}>" for i, entry in enumerate(entries[i:i+50])])
                    embed = disnake.Embed(title=f"Participants of the giveaway, total {len(entries)}", description=entries_mentions, color=0x2F3136)
                    embed.set_thumbnail(url=interaction.author.avatar.url if interaction.author.avatar else interaction.author.default_avatar.url)
                    embeds.append(embed)
                await interaction.response.send_message(embed=embeds[0], view=EntriesPaginator(embeds), ephemeral=True)

        elif interaction.component.custom_id == "giveaway_reroll":
            if not interaction.author.guild_permissions.administrator:
                embed = disnake.Embed(description="You must be an administrator to reroll the giveaway!", color=0x2F3136)
                return await interaction.response.send_message(embed=embed, ephemeral=True)
            winners = await GiveawayFunctions(self.bot).choose_winners(interaction.message.id)
            giveaway = await self.db.get_giveaway(interaction.message.id)
            ended_time = disnake.utils.format_dt(datetime.datetime.now(), "R")
            ended_time_full = disnake.utils.format_dt(datetime.datetime.now(), "F")
            if winners:
                winners_mentions = ", ".join([f"<@{winner[2]}>" for winner in winners])
                await interaction.message.reply(f"Congratulations {winners_mentions}! You have won {giveaway[0][5]}!")
                interaction.message.embeds[0].description = f"- Winners: {winners_mentions}\n- Ended: {ended_time} ({ended_time_full})"
            else:
                await interaction.message.reply("No one entered the giveaway.")
                interaction.message.embeds[0].description = f"- No winners\n- Ended: {ended_time} ({ended_time_full})"
            await interaction.response.send_message(embed=disnake.Embed(description="The giveaway has been rerolled!", color=0x2F3136), ephemeral=True) 

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: disnake.RawMessageDeleteEvent):
        giveaway = await self.db.get_giveaway(payload.message_id)
        if giveaway:
            await self.db.set_true_ended(payload.message_id)
            await self.db.delete_giveaway_entries(payload.message_id)