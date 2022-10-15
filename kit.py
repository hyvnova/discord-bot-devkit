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
    ctx: discord.context,
    create_embed: bool = False,
    create_view: bool = False,
    loading_message: str = "Preparing Contents....",
) -> Union[RootMessage, Tuple[RootMessage, RootItems]]:
    """
    #### Creates a RootMessage and (optinal) items as `embed` or `view`
    If neither `create_embed` or `create_view` are `True` only the root will be returned if any of them is `True` then a tuple will be returned
    
    #### Example
    ##### only root is returned
    `root = createRootMessage(ctx)`
    
    ##### root and items are returned
    `root, items = createRootMessage(ctx, create_embed=True)`
    ##### items are unpackable and accessible as properties
    `embed, view = items`

    `item.embed`
    ```

    """

    msg = await ctx.channel.send(loading_message)

    root = RootMessage(msg)

    items = RootItems(
        Embed(root) if create_embed else None, View(root) if create_view else None
    )

    return (root, items) if (create_embed or create_view) else root
