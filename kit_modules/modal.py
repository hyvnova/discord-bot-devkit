import discord
from typing import Callable, Awaitable, List, Dict, Any


# shortcuts
InputTextStyle = InputTextType = discord.InputTextStyle
InputText = discord.ui.InputText

class Modal(discord.ui.Modal):
    def __init__(
        self,
        title: str,
        items: List[InputText] = [],
        timeout: float = 300,
        custom_id: str | None = None,
        on_submit: Callable[[discord.ui.Modal, discord.Interaction], Awaitable[None]] = None
    ) -> None:

        super().__init__(*items, title=title, custom_id=custom_id, timeout=timeout)
        
        if on_submit:
            self.on_submit = on_submit

    @property
    def on_submit(self):
        return self.callback
    
    @on_submit.setter
    def on_submit(self, callback: Callable[["Modal", discord.Interaction], Awaitable[None]]) -> None:
        self.callback = lambda interaction: callback(self, interaction)

    @property
    def items(self) -> List[InputText]:
        return self.children

    def edit(self, **properties) -> None:
        """
        #### Edits the properties

        #### Properties
        - title: `str`,
        - on_submit: `Callable[[discord.ui.Modal, discord.Interaction], Awaitable[None]]`
        - items: `List[InputText]`
        """

        if (items := properties.pop("items", False)):
            
            # remove old items
            for item in self.items:
                self.remove_item(item)
            
            # add new items
            for item in items:
                self.add_item(item)    
                        
        if (on_submit := properties.pop("on_submit", False)):
            self.on_submit = on_submit

        for name, value in properties.items():
            setattr(self, name, value)

    async def open(self, interaction: discord.Interaction) -> Awaitable[None]:
        """Opens the modal dialog, becareful interaction isn't alredy responded"""
        await interaction.response.send_modal(self)
    
    def as_dict(self, key: str = "custom_id", value: str = "value", skip_null: bool = False) -> Dict[Any, Any]:
        return {
            getattr(item, key) : getattr(item, value) 
            for item in self.children
            if (skip_null == False) or (skip_null==True and bool(getattr(item, value)) == True)
        }
        
    # default on submit
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Ouput")
        for item in self.items:
            embed.add_field(name=item.label, value=item.value)

        await interaction.response.send_message(embeds=[embed])
        