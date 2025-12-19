import discord
from discord.ext import commands
from datetime import datetime
from app.helpers.logging import logger
from app.core.constants.colors import BLUE
from app.services.database.queries import delete_guild_data

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            await delete_guild_data(guild.id)
            self.bot.prefix_cache.pop(guild.id,None)
            self.bot.guild_settings_cache.pop(guild.id, None)
            await channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in guild join log {e}")


async def setup(bot):
  await bot.add_cog(Leave(bot))