import asyncio
from kit import *

bot = Bot(prefix=".")


@bot.slash_command(name="sh")
async def slash(ctx):
    await ctx.respond("hi")


@bot.command(name="t")
async def test(ctx):
    root = await createRootMessage(ctx)

    embed = Embed(root, title="Hiii")
    await embed.update()

    await asyncio.sleep(5)

    embed.title = "Mooo"
    await embed.update()


bot.run("MTAyODc2ODc0Mjc3NzMxMTM0NA.GXYYto.CTXHkbNZ_DrbBfWT_IcDLznknAPlwK_SvzMhus")
