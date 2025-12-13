import discord
from discord.ext import commands
from datetime import datetime
from app.services.database.queries import get_or_create_guild
from app.helpers.logging import logger
from app.core.constants.colors import BLUE


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(1441167455040049384)
        name = guild.name
        member_count = guild.member_count
        joined_at = datetime.utcnow().strftime("%d %b %Y • %I:%M %p UTC")

        embed = discord.Embed(
            color=BLUE,
            title="New Server Joined",
            description=f"> **Name:** {name}\n> **Member Count:** {member_count}\n> **Joined At:** {joined_at}",
        )
        try:
            await get_or_create_guild(str(guild.id), name)
            self.bot.prefix_cache[guild.id] = "."
            self.bot.guild_settings_cache[guild.id]["language"] = "en"
            await channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in guild join log {e}")


async def setup(bot):
    await bot.add_cog(Join(bot))
