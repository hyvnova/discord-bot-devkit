import discord
from discord.ext import commands
from typing import Union

# local modules
from kit_modules import *

# shortcuts
ui = discord.ui
OptionType = discord.SlashCommandOptionType

class Bot(commands.Bot):
    def __init__(
        self,
        prefix: str = ".",
        intents: discord.Intents = discord.Intents.default(),
        **kwargs,
    ):
        intents.message_content = True
        super().__init__(command_prefix=prefix, intents=intents, **kwargs)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

async def create_root(
    ctx: Union[commands.context.Context, discord.ApplicationContext],
    create_embeds: bool = True,
    create_view: bool = True,
    loading_message: str = "Preparing Contents....",
) -> Awaitable[Root]:
    """
    #### Creates a Root and (optinal) items as `embeds` or `view`

    #### Example
    `root = await createRoot(ctx)`

    #### items are unpackable and accessible as properties
    `view = root.view`
    ##### Unpack order: embeds, view
    `embeds, view = root.items`
    ```
    """

    respondable : Union[discord.Interaction, discord.Message] = await (
        ctx.respond(content=loading_message)
        if isinstance(ctx, discord.ApplicationContext)
        else ctx.channel.send(loading_message)
    )

    root = Root(
        respondable, ctx if isinstance(ctx, discord.ApplicationContext) else None
    )

    root._set_root_items(
        RootItems(
            EmbedList(root) if create_embeds else None,
            View(root) if create_view else None,
        )
    )

    return root
