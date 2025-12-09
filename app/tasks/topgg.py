import aiohttp
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from app.helpers.logging import logger


load_dotenv()
TOPGG_TOKEN = os.getenv('TOPGG_TOKEN')
BOT_ID = "1133741199505760266"


class TopGG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_topgg.start()

    def cog_unload(self):
        self.update_topgg.cancel()

    async def post_stats(self):
        url = f"https://top.gg/api/bots/{BOT_ID}/stats"
        payload = {"server_count": len(self.bot.guilds)}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=payload, headers={"Authorization": TOPGG_TOKEN}
            ) as resp:
                text = await resp.text()
                logger.info(f"[Top.gg] Status: {resp.status} | Response: {text}")

    @tasks.loop(hours=3)
    async def update_topgg(self):
        await self.post_stats()

    @update_topgg.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(TopGG(bot))
