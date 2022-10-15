from typing import Awaitable, Callable
import discord
from discord import ButtonStyle

class Button(discord.ui.Button):
    def __init__(
            self, custom_id: str, callback: Callable[[discord.ui.Button, discord.Interaction], Awaitable[None]], *args, **kwargs
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
        if not kwargs.get("label"): kwargs["label"] = custom_id

        if not kwargs.get("style"): kwargs["style"] = ButtonStyle.primary 

        super().__init__(*args, **kwargs)
        self.custom_id = custom_id
        self.callback = lambda interaction: callback(self, interaction)

