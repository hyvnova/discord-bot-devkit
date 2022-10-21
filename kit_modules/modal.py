import discord
from typing import *

from .types import _Root

# shortcuts
InputTextStyle = InputTextType = discord.InputTextStyle
InputText = discord.ui.InputText


async def default_on_submit(modal: discord.ui.Modal, interaction: discord.Interaction):
    embed = discord.Embed(title="Modal Results")
    for item in modal:
        embed.add_field(name=item.label, value=item.value)

    await interaction.response.send_message(embeds=[embed])

class Modal(discord.ui.Modal):
    def __init__(
        self,
        root: _Root,
        title: str,
        items: List[InputText] = [],
        timeout: float = 300,
        custom_id: str | None = None,
        on_submit: Callable[[discord.ui.Modal, discord.Interaction], Awaitable[None]] = default_on_submit
    ) -> None:

        super().__init__(*items, title=title, custom_id=custom_id, timeout=timeout)

        self.root = root
        self.on_submit = self.set_on_submit(on_submit)

    def set_on_submit(self, callback) -> None:
        self.callback = lambda interaction: callback(self, interaction) 

    @property
    def items(self) -> List[InputText]:
        return self.children

    async def edit(self, **properties):
        """
        #### Edits the properties of the modal then updates it

        #### Properties
        `root: Root`,
        `title: str`,
        `timeout: float `
        `on_submit: Callable[[discord.ui.Modal, discord.Interaction], Awaitable[None]]`
        `items: List[InputText]`
        """

        items = properties["items"]
        items = [items] if not isinstance(items, list) else items

        for item in items:
            super().add_item(item)

        del properties["items"]

        if properties.get("on_submit"):
            self.set_on_submit(properties["on_submit"])
            del properties["on_submit"]

        for name, value in properties.items():
            setattr(self, name, value)

    async def open(self, interaction: discord.Interaction):
        """Opens the modal dialog, becareful interactin isn't alredy responded"""
        await interaction.response.send_modal(self)
            

    def __iter__(self):
        return self.children.__iter__()

    def __next__(self):
        return self.children.__next__()
        