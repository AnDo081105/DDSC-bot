import asyncio
import discord
from discord import app_commands
import os
from pathlib import Path
from bot import create_bot
from config import TOKEN

# Create a single bot instance to be shared
bot = create_bot()


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingAnyRole):
        await interaction.response.send_message("You don't have the required role to use this command!", ephemeral=True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message("I don't have the required permissions to do that!", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)


async def load_cogs():
    """
    Automatically load all cogs from the cogs directory
    """
    cogs_path = os.path.join(os.path.dirname(__file__), 'cogs')
    for filename in os.listdir(cogs_path):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = filename[:-3]  # Remove .py extension
            await bot.load_extension(f'cogs.{cog_name}')
            print(f'Loaded cog: {cog_name}')


async def run_bot():
    """Run the bot with cogs loaded - can be called from other entry points"""
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


# Entry point for LOCAL development
if __name__ == "__main__":
    print("Starting bot locally...")
    asyncio.run(run_bot())