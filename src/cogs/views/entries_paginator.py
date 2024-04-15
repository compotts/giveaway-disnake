import disnake
from typing import List


class EntriePaginator(disnake.ui.View):
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