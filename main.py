import discord
from discord.ext import commands

from ctypes.util import find_library

import os
import asyncio

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')


intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX, description='This is music player bot!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged on as {bot.user.name}')
    
    if not discord.opus.is_loaded():
        discord.opus.load_opus(find_library('opus'))

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())