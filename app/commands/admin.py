import discord
from discord.ext import commands
from app.helpers.constants import BLUE
from app.helpers.logging import logger
from app.database.queries import (
    set_prefix,
    set_modlog_channel,
    set_suggestion_channel,
    set_appeal_channel,
)
from app.ui.embeds import error_embed, success_embed


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prefix", help="Change bot prefix for server.")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def _set_prefix(self, ctx, *, prefix: str) -> None:
        if len(prefix) > 5:
            await ctx.reply(
                embed=error_embed("Prefix cannot have more than 5 characters")
            )
            return
        try:
            await set_prefix(ctx.guild.id, prefix)
            self.bot.prefix_cache[ctx.guild.id] = prefix
            await ctx.reply(
                embed=success_embed(f"Prefix changed to `{prefix}`"),
                mention_author=False,
            )
        except Exception as e:
            logger.error(f"Set prefix command failed: {e}")
            await ctx.reply(embed=error_embed("Something went wrong."))

    @commands.command(name="setmodlogs", help="Set a channel to receive modlogs.")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def _setmodlogchan(self, ctx, channel: discord.TextChannel | None) -> None:
        channel = channel or ctx.channel

        try:
            await set_modlog_channel(ctx.guild.id, channel.id)
            self.bot.guild_settings_cache[ctx.guild.id]["modlogs_channelid"] = (
                channel.id
            )
            await ctx.reply(
                embed=success_embed(f"Modlogs channel set to {channel.mention}"),
                mention_author=False,
            )
        except Exception as e:
            logger.error(f"Set mod log failed: {e}")
            await ctx.reply(embed=error_embed("Something went wrong."))


    @commands.command(
        name="setappeals", help="Set a channel to receive appeal submissions."
    )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def _appealer(
        self, ctx: commands.Context, channel: discord.TextChannel | None = None
    ) -> None:
        assert isinstance(ctx.channel, discord.TextChannel)
        channel = channel or ctx.channel
        assert channel is not None
        guild = ctx.guild
        assert guild is not None
        try:
            await set_appeal_channel(guild.id, channel.id)
            self.bot.guild_settings_cache[guild.id]["appeals_channelid"] = channel.id
            await ctx.reply(
                embed=success_embed(
                    f"Appeal submissions channel set to {channel.mention}"
                )
            )
        except Exception as e:
            await ctx.reply(embed=error_embed("Something went wrong."))
            logger.error(f"Set appeal channel command failed: {e}")

    @commands.command(name="say", help="Say something via Privilix.")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _say(self, ctx, *, message: str) -> None:
        await ctx.message.delete()
        embed = discord.Embed(color=BLUE, description=message)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
