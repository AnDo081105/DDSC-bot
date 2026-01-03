import discord
from discord import app_commands
from discord.ext import commands
from config import ADMIN_ROLES
import os


class InfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="introduction", description="Send the club introduction message to a channel (Admin only)")
    @app_commands.checks.has_any_role(*ADMIN_ROLES)
    @app_commands.describe(channel="The channel to send the introduction to (optional)")
    async def introduction(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        logo_path = os.path.join("assets", "DDSC_logo.jpg")
        logo_file = discord.File(logo_path, filename="DDSC_logo.jpg")
        
        who_embed = discord.Embed(
            title="👋 **Who Are We?**",
            description="We are **Deakin Data Science Club (DDSC)**, Deakin University's representative student society for **data science, AI and analytics**! We are here to support you on your journey to explore, collaborate with others, and maximise your potential in this rapidly growing field.",
            color=discord.Color.blue()
        )
        who_embed.set_thumbnail(url="attachment://DDSC_logo.jpg")

        vision_embed = discord.Embed(
            title="🌟 **Vision, Mission, and Values**",
            description="**Vision:** To be the most impactful and engaging student-run data science organisation in Australia, inspiring the next generation of AI and data leaders.\n\n**Mission:** To equip students with the practical skills, professional networks and community support needed to thrive in data science, AI and analytics.\n\n**Values:** Commitment, Communication, Curiosity, Competence.",
            color=discord.Color.blue()
        )
        
        objectives_embed = discord.Embed(
            title="🎯 **Objectives and Goals**",
            description="🔥 To promote interest in data science, AI and analytics among Deakin students by creating a platform for knowledge exchange and engagement.\n\n🔥 To provide employability resources and guidance for students interested in data science, AI, and computing fields, including networking events, hackathons, and job opportunity notices.\n\n🔥 To support the development of programming skills from beginner to intermediate levels through workshops, classes, and resources.\n\n🔥 To create collaborative opportunities among students working on data science, AI, and computing projects, encouraging peer learning and teamwork.",
            color=discord.Color.blue()
        )

        introduction_link_embed = discord.Embed(
            title="🔗 **Learn More About Us!**",
            description="🌲 [**Our Linktree**](https://linktr.ee/deakindatascienceclub)\n🌐 [**Our Website**](https://ddsclub.org/)\n📷 [**Our Instagram**](https://www.instagram.com/deakin_dsc/)",
            color=discord.Color.blue()
        )

        target = channel or interaction.channel
        await target.send("# 👨‍💻 **Welcome to Deakin Data Science Club!!**")
        await target.send(embed=who_embed, file=logo_file)
        await target.send(embed=vision_embed)
        await target.send(embed=objectives_embed)
        await target.send(embed=introduction_link_embed)

        if channel:
            await interaction.response.send_message(f"Introduction message sent to {channel.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("Introduction message sent!", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(InfoCog(bot))