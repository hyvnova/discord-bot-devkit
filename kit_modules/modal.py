import discord
from typing import *

from .root import RootMessage

# shortcuts
InputTextStyle = InputTextType = discord.InputTextStyle
InputText = discord.InputText


async def default_on_submit(modal: discord.ui.Modal, interaction: discord.Interaction):
    embed = discord.Embed(title="Modal Results")
    for item in modal:
        embed.add_field(name=item.label, value=item.value)

    await interaction.response.send_message(embeds=[embed])

class Modal(discord.ui.Modal):
    def __init__(
        self,
        root_mesage: RootMessage,
        title: str,
        timeout: float = 60,
        custom_id: str | None = None,
        on_submit: Callable[[discord.ui.Modal, discord.Interaction], Awaitable[None]] = default_on_submit
    ) -> None:

        super().__init__(title=title, custom_id=custom_id, timeout=timeout)

        self.root_message = root_mesage
        self.callback = on_submit

    async def update(self):
        await self.root_message.add_modal(self)

    async def add_item(self, item: InputText) -> None:
        super().add_item(item)
        await self.update()

    async def add_items(self, items: List[InputText]) -> None:
        for item in items:
            super().add_item(item)
            
        await self.update()

    def __iter__(self):
        return self.children.__iter__()

    def __next__(self):
        return self.children.__next__()
        