from typing import Any, Awaitable, Callable, List
import discord
from discord import ButtonStyle

# shotcuts
SelectOption = discord.SelectOption


class Button(discord.ui.Button):
    def __init__(
        self,
        custom_id: str,
        callback: Callable[[discord.ui.Button, discord.Interaction], Awaitable[None]],
        *args,
        **kwargs
    ):
        """
        Note: if no label is passed custom_id will be used as label

        #### kwargs
            - style: ButtonStyle
            - label: str
            - disabled: bool
            - url: str
            - emoji: str | Emoji
            - row: int
        """

        # if no label is passed use ID as label
        if not kwargs.get("label"):
            kwargs["label"] = custom_id

        if not kwargs.get("style"):
            kwargs["style"] = ButtonStyle.primary

        super().__init__(*args, **kwargs)
        self.custom_id = custom_id
        self.callback = lambda interaction: callback(self, interaction)


async def default_on_select(select_menu, interaction):
     await interaction.response.send_message(f"**Selected:**{select_menu.values[0]}")

class SelectMenu(discord.ui.Select):
    def __init__(
        self,
        options: List[SelectOption],
        on_select: Callable[[discord.ui.Select, discord.Interaction], Awaitable[None]] = default_on_select,
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

