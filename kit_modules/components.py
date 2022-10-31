from typing import Any, Awaitable, Callable, List
import discord
from discord import ButtonStyle, Emoji

# shotcuts
SelectOption = discord.SelectOption


class Button(discord.ui.Button):
    def __init__(
        self,
        callback: Callable[[discord.ui.Button, discord.Interaction], Awaitable[None]],
        label: str,
        style: ButtonStyle = ButtonStyle.blurple,
        disabled: bool = False,
        url: str | None = None, 
        emoji: str | Emoji | None =  None,
        custom_id: str | None = None,
        row: int | None = None    
        ):
        """
        Note: if no `custom_id` is passed `label` will be used as `custom_id`
        """

        if not custom_id:
            custom_id = label

        super().__init__(label=label, style=style, disabled=disabled, url=url, emoji=emoji, custom_id=custom_id, row=row)
        self.custom_id = custom_id
        self.callback = lambda interaction: callback(self, interaction)

async def default_on_select(select_menu, interaction):
     await interaction.response.send_message(f"**Selected:** {select_menu.selected}")

class SelectMenu(discord.ui.Select):
    def __init__(
        self,
        on_select: Callable[[discord.ui.Select, discord.Interaction], Awaitable[None]] = default_on_select,
        options: List[SelectOption] = [],
        placeholder: str = "Select a option",
        min_values: int = 1,
        max_values: int = 1,
        custom_id: Any = None,
        disabled: bool = False,
        row: int = None,
    ) -> None:

        super().__init__(
            options=options,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            custom_id=custom_id,
            disabled=disabled,
            row=row,
        )

        self.callback = lambda interaction: on_select(self, interaction)

    @property
    def selected(self) -> SelectOption:
        return self.values[0] 

