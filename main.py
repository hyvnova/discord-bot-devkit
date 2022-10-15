import asyncio, os
from dotenv import load_dotenv
from kit import *

def get_prefix(bot, message):
    return ["."]

bot = Bot(prefix=get_prefix)


@bot.slash_command(name="sh")
async def slash(ctx):
    await ctx.respond("hi")


@bot.command(name="t")
async def test(ctx):
    root = await createRootMessage(ctx)

    embed = await Embed(root, title="Hiii").update()

    await asyncio.sleep(5)

    await embed.edit(title = "Mooo")


    

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
