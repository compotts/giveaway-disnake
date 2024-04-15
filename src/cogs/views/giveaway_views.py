import disnake
import datetime
import repositories
import cogs as cogs

from .entries_paginator import EntriePaginator


class GiveawayCreateView(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_db = repositories.GiveawayRepository()
        self.participants_db = repositories.ParticipantRepository()
        super().__init__(timeout=None)

    @disnake.ui.button(label="Присоединиться", style=disnake.ButtonStyle.blurple, custom_id="giveaway_join")
    async def join_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        giveaway = await self.giveaway_db.get(
            giveaway_id=interaction.message.id
        )

        if not giveaway or datetime.datetime.strptime(giveaway.end_time, "%Y-%m-%d %H:%M:%S") < datetime.datetime.now():
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
            if not await cogs.GiveawayFunction(self.bot).check_if_user_in_voice_channel(interaction):
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
            if not await cogs.GiveawayFunction(self.bot).check_if_user_on_tribune(interaction):
                embed = disnake.Embed(
                    description="Вы должны находится на трибуне для участия!", 
                    color=0x2F3136
                )
                await interaction.response.send_message(
                    embed=embed, 
                    ephemeral=True
                )
                return
            
        entry = await self.participants_db.get(
            giveaway_id=interaction.message.id, 
            user_id=interaction.author.id
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
                giveaway_id=interaction.message.id,
                user_id=interaction.author.id
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
            await self.participants_db.create(
                giveaway_id=interaction.message.id,
                user_id=interaction.author.id,
                entry_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

    @disnake.ui.button(label="Участники", style=disnake.ButtonStyle.gray, custom_id="giveaway_entries")
    async def entries_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        entries = await self.participants_db.get(
            giveaway_id=interaction.message.id
        )
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


class GiveawayRerollView(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_db = repositories.GiveawayRepository()
        self.participants_db = repositories.ParticipantRepository()
        super().__init__(timeout=None)

    @disnake.ui.button(label="Перевыбрать", style=disnake.ButtonStyle.gray, custom_id="giveaway_reroll")
    async def reroll_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
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
        embed_message = interaction.message.embeds[0]
        winners = await cogs.GiveawayFunction(self.bot).choose_winners(interaction.message.id)
        giveaway = await self.giveaway_db.get(
            giveaway_id=interaction.message.id
        )
        ended_time = disnake.utils.format_dt(
            datetime.datetime.now(), 
            "R"
        )
        ended_time_full = disnake.utils.format_dt(
            datetime.datetime.now(), 
            "F"
        )
        if winners:
            winners_mentions = ", ".join(
                [f"<@{winner.user_id}>" for winner in winners]
            )
            await interaction.message.reply(
                f"Победитель был перевыбран! \nПоздравляем {winners_mentions}! Вы выиграли {giveaway.prize}!"
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
            view=GiveawayRerollView(self.bot),
        )