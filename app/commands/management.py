import discord
from discord.ext import commands
from app.ui.embeds import error_embed, success_embed
from app.helpers.logging import logger
from app.ui.views.warningView import WarningViewer
from app.ui.views.modlogView import Modlogs
from app.services.database.queries import fetch_modlogs, fetch_warnings
from app.helpers.time_converter import time_converter
from typing import Optional


class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="clear", help="Remove several messages instantly in this channel."
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx, count: int):
        if not ctx.guild.me.guild_permissions.manage_messages:
            await ctx.reply(embed=error_embed("Missing permission to manage messages."))
            return

        if not 1 <= count <= 50:
            await ctx.reply(
                embed=error_embed(
                    "You can only remove between 1 and 50 messages at a time."
                )
            )
            return

        try:
            deleted = await ctx.channel.purge(limit=count)
            embed = success_embed(f"Deleted {len(deleted)} messages.")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.reply(embed=error_embed("Something went wrong."))
            logger.error(f"Purge command failed: {e}")

    @commands.command(name="setnick", help="Set nickname for a user.")
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def _setnick(
        self,
        ctx,
        user: discord.Member,
        *,
        nickname: str,
    ):
        if not ctx.guild.me.guild_permissions.manage_nicknames:
            await ctx.reply(embed=e("Missing permission to manage nicknames."))
            return

        try:
            await user.edit(
                nick=nickname, reason=f"Changed by {ctx.author.display_name}"
            )
            await ctx.reply(
                embed=success_embed(
                    f"Updated the nickname for {user.mention} to {nickname}."
                )
            )
        except Exception as e:
            logger.Error(f"Nickname command failed: {e}")
            await ctx.reply(embed=error_embed("Something went wrong."))

    @commands.command(name="warnings", help="Get complete warning history for a user.")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def _warnings(self, ctx, member: discord.Member):
        warnings = await fetch_warnings(ctx.guild.id, member.id)

        if not warnings:
            return await ctx.reply(embed=error_embed("User has no warnings"))

        view = WarningViewer(warnings, member)
        await ctx.reply(embed=view.get_embed(), view=view)

    @commands.command(
        name="modlogs", help="Get complete moderation history for a user."
    )
    @commands.guild_only()
    @commands.has_permissions(
        ban_members=True, kick_members=True, moderate_members=True, manage_messages=True
    )
    async def _modlogs(self, ctx, member: discord.Member):
        modlogs = await fetch_modlogs(ctx.guild.id, member.id)

        if not modlogs:
            return await ctx.reply(embed=error_embed("User has a clean history"))

        view = Modlogs(modlogs, member)
        await ctx.reply(embed=view.get_embed(), view=view)

    @commands.command(name="slowmode", help="Set a slowmode for a channel.")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def _slowmode(
        self,
        ctx: commands.Context,
        time: str,
        channel: Optional[discord.TextChannel] = None,
    ):
        seconds = time_converter(time)
        if seconds == None or seconds == 0:
            await ctx.reply(
                embed=error_embed(
                    "Invalid duration. Use formats like 5m, 2h, or 2h30m."
                )
            )
            return
        if seconds > 21600:
            await ctx.reply(
                embed=error_embed(
                    "The duration for slowmode cannot be more than 6 hours."
                )
            )
            return

        channel = channel or ctx.channel
        try:
            await channel.edit(slowmode_delay=seconds)
        except Exception as e:
            await ctx.reply(embed=error_embed("Something went wrong."))
            logger.error(f"Slowmode command failed {e}")
            return

        await ctx.reply(
            embed=success_embed(
                f"The slowmode of the channel {channel.mention} has been set to {seconds} seconds"
            )
        )


async def setup(bot):
    await bot.add_cog(Management(bot))
