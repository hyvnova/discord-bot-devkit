from collections import namedtuple
import discord
from typing import *


RootItems = namedtuple("RootItems", ["embeds", "view", "modal"])
# class RootItems(TypedDict):
#     embeds: discord.Embed = None
#     view: discord.ui.View = None
#     modal: discord.ui.Modal = None


class RootMessage:
    def __init__(
        self,
        message: Union[discord.Message, discord.Interaction],
        ctx: discord.ApplicationContext = None,
    ):
        self.original_message = message
        self.ctx = ctx

        self.__edit_func = (
            self.original_message.edit_original_response
            if isinstance(message, discord.Interaction)
            else message.edit
        )

        # set root items
        self._set_root_items(RootItems(None, None, None))

        # use to remove the starting content from the message when it loads
        self.__loaded: bool = False

    def _set_root_items(self, items: RootItems):
        self.items = items

        for key in items._fields:
            self.__setattr__(
                key,
                self.items.__getattribute__(key),
            )

    def __iter__(self):
        return self.items.__iter__()

    def __next__(self):
        return self.items.__next__()

    async def edit(self, **kwargs):
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

        await self.__edit_func(**kwargs)

    async def add_modal(self, modal: discord.ui.Modal):
        """Sends a modal, only allowed in slash commands context"""
        await self.ctx.send_modal(modal)
