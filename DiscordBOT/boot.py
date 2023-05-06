import discord
from discord import Intents
import os
from dotenv import load_dotenv
import mysql.connector
from discord.ext import commands
from pathlib import Path

intents = discord.Intents().all()

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def hello(ctx):
    channel = discord.utils.get(ctx.guild.text_channels, name="commands")
    await channel.send("Hello, world!")

env_path = Path('C:/Users/redko/OneDrive/Изображения/Рабочий стол/DiscordBOT/guard.env')
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv('TOKEN')

client.run(TOKEN)