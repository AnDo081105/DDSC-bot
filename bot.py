import discord
from discord.ext import commands
import logging

def create_bot():
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    
    '''
    ---Set up intents---
    For the bot to be able to perform certain actions, we need to specify intents in both
    the code and the Discord Developer Portal.
    For now, all intents are set to True in the Developer Portal.
    '''
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.event_link = None  # Shared state
    bot.log_handler = handler
    
    return bot