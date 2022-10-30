import discord
from discord.ext import commands

# local modules
from . import *

# shortcuts
ui = discord.ui
OptionType = discord.SlashCommandOptionType


class Bot(commands.Bot):
    def __init__(
        self,
        prefix: Union[str, list[str]] = ".",
        intents: discord.Intents = discord.Intents.default(),
        cogs: List[str] | CogBundle = [],
        **kwargs,
    ):
        intents.message_content = True
        super().__init__(command_prefix=prefix, intents=intents, **kwargs)  # type: ignore

        # load cogs
        if isinstance(cogs, CogBundle):
            cogs(self)
            
        else:
            self.load_extensions(*cogs)


    async def on_ready(self):
        print(f"Logged in as {self.user}")


async def createRoot(
    ctx: Union[commands.context.Context, discord.ApplicationContext],
    create_embeds: bool = True,
    create_view: bool = True,
    create_modal: bool = True,
    loading_message: str = "Preparing Contents....",
) -> Root:
    """
    #### Creates a RootMessage and (optinal) items as `embed` or `view`
    If neither `create_embed`, `create_view` or `create_modal` are `True` only the root will be returned if any of them is `True` then a tuple will be returned

    #### Example
    `root = createRootMessage(ctx)`

    ##### Pre-creation of objects (shortcut)
    `root = createRootMessage(ctx, create_embed=True, create_view=True)`
    #### items are unpackable and accessible as properties
    `view = root.view`
    ##### Unpack order: embeds, view, modal
    `embeds, view, modal = root.items()`

    `embed = embeds[0]`
    ##### `create_embed` adds a `Embed` into `root.embeds`
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

    root._set_items(
        RootItems(
            EmbedList(Embed(root)) if create_embeds else None,
            View(root) if create_view else None,
            Modal(root, title="Default Title") if create_modal else None,
        )
    )

    return root

