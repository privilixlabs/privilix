import discord
from discord.ext import commands
from app.helpers.logging import logger
from app.services.database.queries import get_or_create_guild


class Connection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        for guild in self.bot.guilds:
          await get_or_create_guild(guild.id, guild.name)
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help • privilix.xyz")
        )
        # commands = await self.bot.tree.fetch_commands()
        # for cmd in commands:
        #   print(cmd.name, cmd.id)
        logger.info(f"Logged in as {self.bot.user}")

    @commands.Cog.listener()
    async def on_connect(self):
      logger.info("Connected to discord")
      
    @commands.Cog.listener()
    async def on_disconnect(self):
      logger.info("Disconnected from Discord")
      
    @commands.Cog.listener()
    async def on_resumed(self):
      logger.info("Session resumed")


async def setup(bot):
    await bot.add_cog(Connection(bot))
