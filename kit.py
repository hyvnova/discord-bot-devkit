import discord
from discord.ext import commands

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


async def createRootMessage(
    ctx: Union[commands.Context, discord.ApplicationContext],
    create_embed: bool = False,
    create_view: bool = False,
    create_modal: bool = False,
    loading_message: str = "Preparing Contents....",
) -> RootMessage:
    """
    #### Creates a RootMessage and (optinal) items as `embed` or `view`
    If neither `create_embed`, `create_view` or `create_modal` are `True` only the root will be returned if any of them is `True` then a tuple will be returned

    #### Example
    `root = createRootMessage(ctx)`

    ##### Pre-creation of objects (shortcut)
    `root = createRootMessage(ctx, create_embed=True, create_view=True)`
    #### items are unpackable and accessible as properties
    ##### Unpack order: embeds, view, modal
    `embed, view, modal = items`

    `embed = root.embeds[0]`
    ##### `create_embed` adds a `Embed` into `root.embeds`
    ```
    """

    msg = await (
        ctx.respond(content=loading_message)
        if isinstance(ctx, discord.ApplicationContext)
        else ctx.channel.send(loading_message)
    )

    root = RootMessage(
        msg, ctx if isinstance(ctx, discord.ApplicationContext) else None
    )

    root._set_root_items(
        RootItems(
            EmbedList(Embed(root)) if create_embed else None,
            View(root) if create_view else None,
            Modal(root, title="Default Title") if create_modal else None,
        )
    )

    return root
