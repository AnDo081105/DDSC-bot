import discord
from discord import app_commands
from discord.ext import commands
from config import ADMIN_ROLES


class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="setevent", description="Set the event registration link (Admin only)")
    @app_commands.checks.has_any_role(*ADMIN_ROLES)
    @app_commands.default_permissions(administrator=True)  # Only admins can see this

    async def setevent(self, interaction: discord.Interaction, link: str):
        self.bot.event_link = link
        await interaction.response.send_message(f"Event registration link has been set to: {link}")

    @app_commands.command(name="register", description="Get the event registration link via DM")
    async def register(self, interaction: discord.Interaction):
        if self.bot.event_link is None:
            await interaction.response.send_message("No event link has been set yet.", ephemeral=True, delete_after=300, delete_after=5)
            return
        
        register_message = [
            "# 📝 **Register for DDSC Events!**",
            "Thank you for joining our events, we are excited to have you on board!",
            "# 📌 **Register Now!**",
            f"[**Click here to register!**]({self.bot.event_link})"
        ]
        try:
            await interaction.user.send("\n".join(register_message))
            await interaction.response.send_message("I've sent you the registration link via DM!", ephemeral=True, delete_after=300)
        except discord.Forbidden:
            await interaction.response.send_message("I couldn't DM you. Please check your privacy settings.", ephemeral=True, delete_after=300)


async def setup(bot: commands.Bot):
    await bot.add_cog(EventsCog(bot))