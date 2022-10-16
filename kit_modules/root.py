from dis import disco
import discord
from typing import *

class RootItems:
    __slots__ = ("embed", "view", "modal", "__items")
    def __init__(self, embed: discord.Embed, view: discord.ui.View, modal: discord.ui.Modal) -> None:
        
        self.embed: Union[discord.Embed, None] = embed
        self.view: Union[discord.ui.View, None] = view
        self.modal: Union[discord.ui.Modal, None] = modal

        self.__items = (self.embed, self.view, self.modal)

    def __iter__(self):
        return self.__items.__iter__()

    def __next__(self):
        return self.__items.__next__()

class RootMessage:
    def __init__(self, message: discord.Message, ctx: discord.ApplicationContext = None):
        self.original_message = message
        self.ctx = ctx

        # use to remove the starting content from the message when it loads
        self.__loaded: bool = False

    async def edit( self,**kwargs):
        """
        `content: str = None`, 
        `embed: discord.Embed = None`, 
        `embeds: List[discord.Embed ] = None`, 
        `file: Sequence[discord.File] = None`, 
        `files: List[Sequence[discord.File]] = None`, 
        `attachments: List[discord.Attachment] = None`, 
        `suppress: bool = False`, 
        `delete_after: int = None`, 
        `allowed_mentions: discord.AllowedMentions = None`, 
        `view: discord.ui.View = None`
        """

        if not self.__loaded:
            # remove starting content
            if not kwargs.get("content"):
                kwargs["content"] = ""

            self.__loaded = True

        await self.original_message.edit(**kwargs)

        
    async def add_modal(self, modal: discord.ui.Modal):
        """Sends a modal, only allowed in slash commands context"""
        await self.ctx.send_modal(modal)
 