from collections import namedtuple
import discord
from typing import *

class RootItems(namedtuple):
    embed: discord.Embed = None
    view: discord.ui.View = None
    modal: discord.ui.Modal = None

class RootMessage:
    def __init__(self, message: discord.Message, ctx: discord.ApplicationContext = None, items: RootItems = RootItems(None, None, None)):
        self.original_message = message
        self.ctx = ctx

        # set items
        self.items = items

        for key in items.__init__.keys():
            self.__setattr__(
                key,
                property(
                    self.items.__getattribute__(key), 
                    lambda value: self.items.__setattr__(key, value)
                )
            )

        # use to remove the starting content from the message when it loads
        self.__loaded: bool = False



    def __iter__(self):
        return self.items

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
 