import discord
from discord import app_commands
import os
import asyncio
from aiohttp import web
from dotenv import load_dotenv
from discord.ext import commands
import logging

# ---1. Connection Stuff---
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up handler for logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# ---Set up intents---
# For the bot to be able to perform certain actions, we need to specify intents in both
# the code and the Discord Developer Portal.
# For now, all intents are set to True in the Developer Portal.
# ---------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.event_link = None

# ---2. Events & Commands---

admin_roles = ["Discord Programmer", "Executive", "Committee", "Admin"]

# test
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands to Discord
    print(f'We have logged in as {bot.user}')


# /setevent
@bot.tree.command(name="setevent", description="Set the event registration link (Admin only)")
@app_commands.checks.has_any_role(*admin_roles)
async def setevent(interaction: discord.Interaction, link: str):
    bot.event_link = link
    await interaction.response.send_message(f"Event registration link has been set to: {bot.event_link}")

# /register
@bot.tree.command(name="register", description="Get the event registration link via DM")
async def register(interaction: discord.Interaction):
    if bot.event_link is None:
        await interaction.response.send_message("No event link has been set yet.", ephemeral=True)
        return
    event_link = bot.event_link
    register_message = [
        "# 📝 **Register for DDSC Events!**", 
        "Thank you for joining our events, we are excited to have you on board!",
        "# 📌 **Register Now!**",
        f"[**Click here to register!**]({event_link})"
    ]
    try:
        await interaction.user.send("\n".join(register_message))
        await interaction.response.send_message("I've sent you the registration link via DM!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I couldn't DM you. Please check your privacy settings.", ephemeral=True)

# /signup
@bot.tree.command(name="signup", description="Send the club signup message to a channel (Admin only)")
@app_commands.checks.has_any_role(*admin_roles)
@app_commands.describe(channel="The channel to send the signup message to (optional)")
async def signup(interaction: discord.Interaction, channel: discord.TextChannel = None):
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

# /introduction 
@bot.tree.command(name="introduction", description="Send the club introduction message to a channel (Admin only)")
@app_commands.checks.has_any_role(*admin_roles)
@app_commands.describe(channel="The channel to send the introduction to (optional)")
async def introduction(interaction: discord.Interaction, channel: discord.TextChannel = None):
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

    
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingAnyRole):
        await interaction.response.send_message("You don't have the required role to use this command!", ephemeral=True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message("I don't have the required permissions to do that!", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

# ---3. Health Check Server for Render---
async def health_check(request):
    return web.Response(text="OK", status=200)

async def start_health_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    port = int(os.getenv("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Health check server running on port {port}")

async def main():
    await start_health_server()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())