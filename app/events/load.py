import discord
from discord.ext import commands
from app.helpers.logging import logger
from app.core.constants.emojis import LOADER


class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            ctx._loading_message = ctx.message
            await ctx._loading_message.add_reaction(LOADER)
        except Exception as e:
            logger.error(f"Add load reaction error : {e}")

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        try:
            await ctx._loading_message.remove_reaction(
                LOADER, self.bot.user
            )
        except Exception as e:
            logger.error(f"Remove reaction on command completion failed: {e}")


async def setup(bot):
    await bot.add_cog(Load(bot))
