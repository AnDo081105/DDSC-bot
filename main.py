import discord
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


# ---2. Events & Commands---

admin_roles = ["Discord Programmer", "Executive", "Committee", "Admin"]

# test
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# !signup
@bot.command()
@commands.has_any_role(*admin_roles)
async def signup(ctx, channel: discord.TextChannel = None):
    siggnup_message = [
        "# 👨‍💻 **Sign up for DDSC!!!**", 
        "If you haven't signed up to be a member of the **Deakin Data Science Club** yet, please do so by clicking the link below!",
        "## 🤔 **Why Sign Up?**",
        "- Access to exclusive events and workshops.",
        "- Connect with like-minded individuals passionate about data science.",
        "- Enhance your skills and knowledge through our resources and community.",
        "# 📌 **Sign Up Now!**",
        "[**Click here to sign up!**](https://www.dusa.org.au/clubs/deakin-data-science-club-burwood-ddsc)"

    ]

    
    target = channel or ctx.channel  # Use mentioned channel or current
    if channel:
        await ctx.send(f"Signup message sent to {channel.mention}")
    await target.send("\n".join(siggnup_message))

# !introduction 
@bot.command()
@commands.has_any_role(*admin_roles)
async def introduction(ctx, channel: discord.TextChannel = None):
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

    target = channel or ctx.channel  # Use mentioned channel or current
    if channel:
        await ctx.send(f"Introduction message sent to {channel.mention}")
    await target.send("# 👨‍💻 **Welcome to Deakin Data Science Club!!**")
    await target.send(embed=who_embed, file=logo_file)
    await target.send(embed=vision_embed)
    await target.send(embed=objectives_embed)
    await target.send(embed=introduction_link_embed)

    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.message.delete()
        await ctx.send(f"Hey {ctx.author.mention}, you don't have the required role!", delete_after=10)
    
    # if the bot does not have permissions to do something
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have the required permissions to do that!")


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