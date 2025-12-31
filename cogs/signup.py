import discord
from discord import app_commands
from discord.ext import commands
from config import ADMIN_ROLES
import os


class InfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="signup", description="Send the club signup message to a channel (Admin only)")
    @app_commands.checks.has_any_role(*ADMIN_ROLES)
    @app_commands.default_permissions(administrator=True)  # Only admins can see this
    @app_commands.describe(channel="The channel to send the signup message to (optional)")
    async def signup(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        signup_message = [
            "# 👨‍💻 **Sign up for DDSC!!!**",
            "If you haven't signed up to be a member of the **Deakin Data Science Club** yet, please do so by clicking the link below!",
            "## 🤔 **Why Sign Up?**",
            "- Access to exclusive events and workshops.",
            "- Connect with like-minded individuals passionate about data science.",
            "- Enhance your skills and knowledge through our resources and community.",
            "# 📌 **Sign Up Now!**",
            "[**Click here to sign up!**](https://www.dusa.org.au/clubs/deakin-data-science-club-burwood-ddsc)"
        ]

        target = channel or interaction.channel
        await target.send("\n".join(signup_message))
        
        if channel:
            await interaction.response.send_message(f"Signup message sent to {channel.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("Signup message sent!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(InfoCog(bot))