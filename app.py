# Entry point for RENDER deployment (with health check server)
# ---Health Check Server for Render---
import asyncio
import os
from aiohttp import web

# Import shared bot instance and utilities from main
from main import bot, load_cogs
from config import TOKEN


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
    """Entry point for Render - starts health server + bot"""
    await start_health_server()
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


# Entry point for RENDER
if __name__ == "__main__":
    print("Starting bot on Render with health check server...")
    asyncio.run(main())