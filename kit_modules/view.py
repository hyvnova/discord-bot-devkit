from typing import Awaitable, Callable, Iterable
import discord
from discord import Component
from .types import _Root
from .components import SelectMenu


async def default_on_timeout(view: discord.ui.View) -> None:
    return None


class View(discord.ui.View):
    """Kit View class"""
    def __init__(
        self,
        root: _Root,
        timeout: float | None = 300,
        disable_on_timeout: bool = True,
        on_timeout: Callable[[discord.ui.View], Awaitable[None]] = default_on_timeout,
    ):

        super().__init__(timeout=timeout, disable_on_timeout=disable_on_timeout)

        self.root = root

        self.on_timeout_callback = on_timeout

    def __on_add_item(self, item):
        # get on select from select menu
        if isinstance(item, SelectMenu):
            self.select_callback = item.callback

    async def on_timeout(self) -> None:
        if self.disable_on_timeout:
            await self.disable()

        # custom timeout func
        await self.on_timeout_callback(self)

        return await super().on_timeout()

    async def update(self):
        if self.root:
            await self.root.edit(view=self)

    async def add_items(self, *items: Component) -> Awaitable[None]:
        """
        Adds 1 or more items to the View, then updates it.
        """
        for item in items:
            self.__on_add_item(item)
            super().add_item(item)

        await self.update()

    async def disable(self):
        """Disables all items and stops the view"""
        self.disable_all_items()
        self.stop()

        await self.update()