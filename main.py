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
        choices=["jpg", "png", "gif"],
        description="Tipo de la imagen",
        required=False,
    ) = "jpg",
):

    links = search_image(query, cantidad, '.' + type)
    await ctx.respond(f"**Query**: {query}\n**Type**: {type} \n" + "\n".join(links) if links else "No se encontraron imagenes correspondientes a la busqueda." )


@bot.command(name="t")
async def test(ctx):
    root = await createRootMessage(ctx)

    embed = await Embed(root, title="Hiii").update()

    await asyncio.sleep(5)

    await embed.edit(title="Mooo")


@bot.command(name="c")
async def count(ctx, end: int):

    root, items = await createRootMessage(ctx, create_embed=True)

    for i in range(end):
        await asyncio.sleep(1)
        await items.embed.edit(title=str(i))


@bot.command(name="cn")
async def count(ctx, end: int):

    embed = discord.Embed(title="0")
    msg = await ctx.channel.send(embed=embed)

    for i in range(end):
        await asyncio.sleep(1)

        embed.title = str(i)
        await msg.edit(embed=embed)


load_dotenv()
bot.run(os.environ.get("TOKEN"))
