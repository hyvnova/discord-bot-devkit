import asyncio, os
from dotenv import load_dotenv
from kit import *
from search import search_image


def get_prefix(bot, message):
    return ["."]


bot = Bot(prefix=get_prefix, intents=discord.Intents.all())


@bot.slash_command(name="image", description="Busca imagenes en internet")
async def slash_search_image(
    ctx: discord.ApplicationContext,
    query: discord.Option(name="query", description="Imagen que quieres buscar"),
    cantidad: discord.Option(
        OptionType.integer,
        name="cantidad",
        min_value=1,
        max_value=4,
        description="Cantidad de Images a buscar",
        required=False,
    ) = 1,
    type: discord.Option(
        name="type",
        choices=["jpg", "png", "gif", "any"],
        description="Tipo de la imagen",
        required=False,
    ) = "any",
):

    links = search_image(query, cantidad, '.' + type)
    await ctx.respond(f"**Query**: {query}\n**Type**: {type} \n" + "\n".join(links) if links else "No se encontraron imagenes correspondientes a la busqueda." )


@bot.slash_command(name="modal")
async def modal_slash(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""

    root, items = createRootMessage(ctx, create_modal=True)

    await items.modal.add_items([
        InputText(style=InputTextType.short, label="Input Cort"),
        InputText(style=InputTextType.long, label="Input LArgo")
    ])


@bot.slash_command(name="embed")
async def create_embed(ctx):

    root

    data = {
        "title" : "Sin titulo",
        "description" : "Sin description"
    }


load_dotenv()
bot.run(os.environ.get("TOKEN"))
