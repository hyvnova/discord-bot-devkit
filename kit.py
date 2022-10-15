import discord
from discord.ext import commands

# local modules
from kit_modules import *


ui = discord.ui

class Bot(commands.Bot):
    def __init__(self, prefix: str = ".", intents: discord.Intents = discord.Intents.default(), **kwargs):
        intents.message_content = True
        super().__init__(command_prefix=prefix, intents=intents, **kwargs)


    async def on_ready(self):
        print(f"Logged in as {self.user}")


