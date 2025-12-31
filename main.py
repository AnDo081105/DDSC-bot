import asyncio
import discord
from discord import app_commands
from bot import create_bot
from config import TOKEN

bot = create_bot()

# List of cogs to load
COGS = [
    "cogs.events",
    "cogs.info",
]


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


async def main():
    async with bot:
        for cog in COGS:
            await bot.load_extension(cog)
            print(f"Loaded {cog}")
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())