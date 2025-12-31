'''
Cogs for Discord Bot

HOW TO CREATE NEW COGS:
==============================

To create a feature, add a new cog in the cogs/ directory.
Each cog should be a separate .py file and must contain a setup function to add the cog to the bot.
For example, to create a cog named "example", create a file cogs/example.py with the following structure:

    ```python
    import discord
    from discord import app_commands
    from discord.ext import commands

    class ExampleCog(commands.Cog):
        def __init__(self, bot: commands.Bot):
            self.bot = bot

        @commands.command(name="example")
        async def example_command(self, ctx: commands.Context):
            await ctx.send("This is an example command!")

    async def setup(bot: commands.Bot):
        await bot.add_cog(ExampleCog(bot))
    ```

ADMIN-ONLY COMMANDS:
==============================
For any admin-only commands, add checks, and use:

    ```python
    from config import ADMIN_ROLES
    ```
ADMIN_ROLES is located in config.py


NOTES
=====

- Cogs are auto-loaded from main.py
- Files starting with _ are ignored (e.g., __init__.py)
- Each cog MUST have an async setup() function

'''