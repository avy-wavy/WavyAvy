import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents (you can expand as needed)
intents = discord.Intents.default()
intents.message_content = True

# Create the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# This runs when the bot is ready
@bot.event
async def on_ready():
    print(f"WavyAvy is online as {bot.user}!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Slash command: /hello
@bot.tree.command(name="hello", description="Say hello to WavyAvy!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}, WavyAvy is here!")

# Run the bot
bot.run(TOKEN)
