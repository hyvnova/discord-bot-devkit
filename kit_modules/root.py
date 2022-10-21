from collections import namedtuple
import discord
from typing import *

from .embed import Embed
from .modal import Modal
from .view import View


RootItems = namedtuple("RootItems", ["embeds", "view", "modal"])
# class RootItems(TypedDict):
#     embeds: discord.Embed = None
#     view: discord.ui.View = None
#     modal: discord.ui.Modal = None


class Root:
    def __init__(
        self,
        respondable: Union[discord.Message, discord.Interaction],
        ctx: discord.ApplicationContext = None,
    ):
        self.origin = respondable
        self.ctx = ctx

        self.__set_edit_func()

        # set root items
        self._set_root_items(RootItems(None, None, None))

        # use to remove the starting content from the message when it loads
        self.__loaded: bool = False

    def items(self) -> Tuple[List[Embed], View, Modal]:
        """Returns A tuple containing root items"""
        return (self._items.embeds, self._items.view, self._items.modal)
        
    def __set_edit_func(self):
        self.__edit_func = (
            self.origin.response.edit_message
            if isinstance(self.origin, discord.Interaction)
            else self.origin.edit
        )

    def _set_root_items(self, items: RootItems):
        self._items = items

        for key in items._fields:
            self.__setattr__(
                key,
                self._items.__getattribute__(key),
            )

    def __iter__(self):
        return self._items.__iter__()

    def __next__(self):
        return self._items.__next__()

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

    # NOT DONE YET
    async def relocate(self, respondable: Union[discord.Message,discord.Interaction], ctx: discord.ApplicationContext = None) -> None:
        if respondable == self.origin:
            return

        # deleted old origin
        try:
            if isinstance(self.origin, discord.Message):
                await self.origin.delete()

            elif isinstance(self.origin, discord.Interaction):
                await self.origin.delete_original_response()

        except:
            await self.edit(
                content="`[Deleted]`",
                embeds=[],
                view=None
            )

        # set new origin
        self.origin = respondable
        self.ctx = ctx or self.ctx

        self.__set_edit_func()

        # set up origin
        await self.edit(
            embeds=self.embeds,
            view=self.view
        )
