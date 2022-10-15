from typing import Awaitable, Callable, Iterable
import discord
from discord import Component
from .root import RootMessage


async def default_on_timeout(view: discord.ui.View) -> None:
    return None


class View(discord.ui.View):
    """Default View class"""

    def __init__(
        self,
        root_message: RootMessage,
        timeout: float | None = 60,
        disable_on_timeout: bool = True,
        on_timeout: Callable[[discord.ui.View], Awaitable[None]] = default_on_timeout,
    ):

        super().__init__(timeout=timeout, disable_on_timeout=disable_on_timeout)

        self.root_message = root_message

        self.on_timeout_callback = on_timeout

    async def on_timeout(self) -> None:
        if self.disable_on_timeout:
            await self.disable()

        # custom timeout func
        await self.on_timeout_callback(self)

        return await super().on_timeout()

    async def update(self):
        if self.root_message:
            await self.root_message.edit(view=self)

    async def add_item(self, item: Component) -> None:
        super().add_item(item)
        # update view
        await self.update()

    async def add_items(self, items: Iterable[Component]) -> None:
        for item in items:
            super().add_item(item)

        await self.update()

    async def disable(self):
        """Disables all items and stops the view"""
        self.disable_all_items()
        self.stop()

        self.update()
