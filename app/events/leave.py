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
        channel = self.bot.get_channel(1441177924224159856)

        name = guild.name
        member_count = guild.member_count
        joined_at = datetime.utcnow().strftime("%d %b %Y • %I:%M %p UTC")

        embed = discord.Embed(
            color=BLUE,
            title="New Server Left",
            description=f"> **Name:** {name}\n> **Member Count:** {member_count}\n> **Joined At:** {joined_at}",
        )
        try:
            await delete_guild_data(guild.id)
            self.bot.prefix_cache.pop(guild.id,None)
            self.bot.guild_settings_cache.pop(guild.id, None)
            await channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in guild join log {e}")


async def setup(bot):
  await bot.add_cog(Leave(bot))