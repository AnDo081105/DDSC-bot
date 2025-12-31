import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ROLES = ["Discord Programmer", "Executive", "Committee", "Admin"]