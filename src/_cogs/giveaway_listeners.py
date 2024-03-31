import disnake
from disnake.ext import commands


class GiveawayListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        ...

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        ...

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        if interaction.component.custom_id == "giveaway_join":
            ...

        elif interaction.component.custom_id == "giveaway_entries":
            ...

        elif interaction.component.custom_id == "giveaway_reroll":
            ...

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: disnake.RawMessageDeleteEvent):
        ...