import discord
from discord.ext import commands

from app.database.queries import get_or_create_guild
from app.helpers.logging import logger
from app.helpers.constants import BLUE
from app.ui.views.setup import Setup


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        chan = guild.system_channel
        if not chan or not chan.permissions_for(guild.me).send_messages:
            chan = next(
                (
                    c
                    for c in guild.text_channels
                    if c.permissions_for(guild.me).send_messages
                ),
                None,
            )
        if chan:
            embed = discord.Embed(
                color=BLUE,
                description="## 👋 Welcome to Privilix!\nYou are only a few steps away from getting started.",
            )
            embed.add_field(
                name="Quick Setup",
                value="Click the button below to start a quick setup",
            )
            embed.add_field(
                name="More Info", value="Use </help:1449369826303676438> for more info"
            )
            await chan.send(embed=embed, view=Setup(self.bot))
        try:
            await get_or_create_guild(guild.id, guild.name)
            self.bot.prefix_cache[guild.id] = "."
            self.bot.guild_settings_cache[guild.id] = {
                "language": "en",
                "modlogs_channelid": None,
                "suggestion_channelid": None,
                "appeals_channelid": None,
            }
        except Exception as e:
            logger.error(f"Error in guild join log {e}")


async def setup(bot):
    await bot.add_cog(Join(bot))
