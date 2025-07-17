import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"WavyAvy is online as {bot.user}!")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hey {ctx.author.mention}, WavyAvy is here!")

async def main():
    async with bot:
        await bot.load_extension("cogs.notes")
        await bot.start(TOKEN)

asyncio.run(main())
