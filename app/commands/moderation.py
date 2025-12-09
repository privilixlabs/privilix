import discord
from discord.ext import commands
from datetime import datetime, timezone
from app.helpers.logging import logger
from app.services.moderation.checks import check_target
from app.ui.embeds import error_embed, success_embed, dm_embed, log_embed, lock_embed
from app.core.constants.emojis import CHECK
from app.services.database.queries import (
    insert_modlog,
    get_modlog_channel,
    get_appeal_channel,
)
from app.helpers.time_parser import time_parser
from app.ui.views.appealDmView import AppealDMView


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", help="Kick a user.")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def _kick(
        self,
        ctx: commands.Context,
        target: discord.Member,
        *,
        reason: str = "No reason provided",
    ):
        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.reply(
                embed=error_embed("Missing permission to remove members."),
            )
            return

        fail = await check_target(ctx, target)
        if fail:
            await ctx.reply(
                embed=fail,
            )
            return
        name = target.name
        try:
            await target.kick(reason=f"@{ctx.author.name}: {reason}")
        except Exception as e:
            await ctx.reply(
                embed=error_embed("Something went wrong."),
            )
            return

        embed = success_embed(f"**@{name} kicked.**")

        try:
            try:
                await target.send(
                    embed=dm_embed(ctx.guild, "You were kicked", "kick", reason)
                )
            except Exception as e:
                logger.error(f"DM for kick command failed: {e}")
                embed.add_field(name="Notice", value="The user did not receive a DM.")

            log_id = await get_modlog_channel(ctx.guild.id)
            if log_id:
                log_channel = await ctx.guild.fetch_channel(int(log_id))
                await log_channel.send(
                    embed=log_embed(target, ctx.author, "kick", reason)
                )
            await insert_modlog(ctx.guild.id, target.id, ctx.author.id, "kick", reason)
        except Exception as e:
            logger.error(f"Kick logging failed: {e}")
        await ctx.reply(
            embed=embed,
        )

    @commands.command(name="ban", help="Ban a user.")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def _ban(
        self,
        ctx: commands.Context,
        target: discord.Member,
        *,
        reason: str = "No reason provided",
    ):
        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.reply(
                embed=error_embed("Missing permission to ban members."),
            )
            return

        fail = await check_target(ctx, target)
        if fail:
            await ctx.reply(
                embed=fail,
            )
            return

        try:
            await target.ban(reason=f"{ctx.author.name}: {reason}")
        except Exception:
            await ctx.reply(
                embed=error_embed("Something went wrong."),
            )
            return

        embed = success_embed(f"**{target.name} banned.**")

        try:
            log_id = await get_modlog_channel(ctx.guild.id)
            if log_id:
                log_channel = await ctx.guild.fetch_channel(int(log_id))
                await log_channel.send(
                    embed=log_embed(target, ctx.author, "ban", reason)
                )

            case_id = await insert_modlog(
                ctx.guild.id, target.id, ctx.author.id, "ban", reason
            )
            try:
                chnl_id = await get_appeal_channel(ctx.guild.id)
                appeal_view = None
                if chnl_id:
                    appeal_view = AppealDMView(self.bot, ctx.guild.id, case_id, "ban")

                await target.send(
                    embed=dm_embed(ctx.guild, "You were banned", "ban", reason),
                    view=appeal_view,
                )
            except Exception as e:
                logger.error(f"Ban DM failed: {e}")
                embed.add_field(name="Notice", value="The user did not receive a DM.")

        except Exception as e:
            logger.error(f"Ban logging failed: {e}")

        await ctx.reply(
            embed=embed,
        )

    @commands.command(name="unban", help="Unban a user.")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def _unban(
        self,
        ctx: commands.Context,
        user_id: str,
        *,
        reason: str = "No reason provided",
    ):
        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.reply(
                embed=error_embed("Missing permission to unban members."),
            )
            return

        try:
            user_id = int(user_id)
        except ValueError:
            await ctx.reply(
                embed=error_embed("Invalid User Id"),
            )
            return

        try:
            user = await ctx.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=f"@{ctx.author.name}: {reason}")
        except Exception as e:
            logger.error(f"Unban command failed: {e}")
            await ctx.reply(
                embed=error_embed("Something went wrong."),
            )
            return

        embed = success_embed(f"**@{user.name} unbanned.**")

        try:
            try:
                await user.send(
                    embed=dm_embed(ctx.guild, "You were unbanned", "unban", reason),
                )
            except Exception as e:
                logger.error(f"Unban dm failed {e}")
                embed.add_field(name="Notice", value="The user did not receive a DM.")

            log_id = await get_modlog_channel(ctx.guild.id)
            if log_id:
                log_channel = await ctx.guild.fetch_channel(int(log_id))
                await log_channel.send(
                    embed=log_embed(user, ctx.author, "unban", reason)
                )
            await insert_modlog(ctx.guild.id, user_id, ctx.author.id, "unban", reason)
        except Exception as e:
            logger.error(f"Log failed: {e}")

        await ctx.reply(
            embed=embed,
        )

    @commands.command(name="timeout", help="Timeout a member.")
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    async def _timeout(
        self,
        ctx: commands.Context,
        target: discord.Member,
        duration: str,
        *,
        reason: str = "No reason provided",
    ):
        if not ctx.guild.me.guild_permissions.moderate_members:
            await ctx.reply(
                embed=error_embed("Missing permission to manage timeouts."),
            )
            return

        fail = await check_target(ctx, target)
        if fail:
            await ctx.reply(
                embed=fail,
            )
            return

        delta = time_parser(duration)
        if not delta:
            await ctx.reply(
                embed=error_embed(
                    "Invalid duration. Use formats like 5m, 2h, 7d, or 2h30m."
                ),
            )
            return

        until = datetime.now(timezone.utc) + delta

        try:
            await target.timeout(until, reason=f"@{ctx.author.name}: {reason}")
        except Exception as e:
            await ctx.reply(
                embed=error_embed("Something went wrong."),
            )
            return

        embed = success_embed(f"**@{target.name} timed out.**\n> **Duration:** {delta}")

        try:
            try:
                dembed = dm_embed(ctx.guild, "You were timed out", "timeout", reason)
                dembed.add_field(name="Duration:", value=delta)
                await target.send(
                    embed=dembed,
                )
            except Exception as e:
                logger.error(f"timeout dm failed {e}")
                embed.add_field(name="Notice", value="The user did not receive a DM.")
            await insert_modlog(
                ctx.guild.id, target.id, ctx.author.id, "timeout", reason
            )
            log_id = await get_modlog_channel(ctx.guild.id)
            if log_id:
                log_channel = await ctx.guild.fetch_channel(int(log_id))
                lembed = log_embed(target, ctx.author, "timeout", reason)
                lembed.add_field(name="Duration", value=delta)
                await log_channel.send(embed=lembed)
        except Exception as e:
            logger.error(f"Timeout logging failed: {e}")

        await ctx.reply(
            embed=embed,
        )

    @commands.command(name="warn", help="Warn a user.")
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def _warn(
        self,
        ctx: commands.Context,
        target: discord.Member,
        *,
        reason: str = "No reason provided.",
    ):
        if not ctx.guild.me.guild_permissions.manage_messages:
            await ctx.reply(
                embed=error_embed("Missing permission to manage warnings."),
            )
            return
        fail = await check_target(ctx, target)
        if fail:
            await ctx.reply(
                embed=fail,
            )
            return

        try:
            case_id = await insert_modlog(ctx.guild.id, target.id, ctx.author.id, "warn", reason)
            view = AppealDMView(self.bot, ctx.guild.id, case_id, "warn")
        except Exception as e:
            await ctx.reply(
                embed=error_embed("Something went wrong."),
            )
            return

        embed = success_embed(f"**@{target.name} warned.**")

        try:
            try:
                await target.send(
                    embed=dm_embed(ctx.guild, "You were warned", "warn", reason), view = view
                )
            except Exception as e:
                logger.error(f"warn dm failed {e}")
                embed.add_field(name="Notice", value="The user did not receive a DM.")
            log_id = await get_modlog_channel(ctx.guild.id)
            if log_id:
                log_channel = await ctx.guild.fetch_channel(int(log_id))
                await log_channel.send(
                    embed=log_embed(target, ctx.author, "warn", reason)
                )
        except Exception as e:
            pass

        await ctx.reply(
            embed=embed,
        )

    @commands.command(name="lock", help="Lock a channel.")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _lock(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel = None,
        *,
        reason="No reason provided.",
    ):
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.reply(embed=error_embed("Missing permissions to manage roles."))
            return

        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)

        if overwrite.send_messages is False:
            await ctx.reply(
                embed=error_embed("Channel is already locked."),
            )
            return

        try:
            await channel.set_permissions(ctx.guild.me, send_messages=True)
            await channel.set_permissions(
                ctx.guild.default_role,
                send_messages=False,
                reason=f"@{ctx.author.name}: {reason}",
            )
            if channel == ctx.channel:
                await channel.send(embed=lock_embed(ctx.author, "locked"))
            else:
                await channel.send(embed=lock_embed(ctx.author, "locked"))
                await ctx.reply(
                    embed=success_embed(
                        "Channel Locked \n Use `@Privilix unlock` to unlock it."
                    )
                )
        except Exception as e:
            logger.error(f"Lock command Error: {e}")
            await ctx.reply(
                embed=error_embed("Something went wrong."),
            )
            return

    @commands.command(name="unlock", help="Unlock a previously locked channel.")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def _unlock(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel = None,
        *,
        reason="No reason provided.",
    ):
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.reply(embed=error_embed("Missing permissions to manage roles."))
            return

        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)

        if overwrite.send_messages is True:
            await ctx.reply(
                embed=error_embed("Channel is not locked."),
            )
            return

        try:
            await channel.set_permissions(ctx.guild.me, overwrite=None)
            await channel.set_permissions(
                ctx.guild.default_role,
                overwrite=None,
                reason=f"@{ctx.author.name}: {reason}",
            )
            embed = lock_embed(ctx.author, "unlocked")
            embed.title = f"{CHECK} Channel Unlocked"
            if channel == ctx.channel:
                await channel.send(embed=embed)
            else:
                await ctx.reply(
                    embed=success_embed("Channel unlocked."),
                )
                await channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Lock command Error: {e}")
            await ctx.reply(
                embed=error_embed("Something went wrong."),
            )
            return


async def setup(bot):
    await bot.add_cog(Moderation(bot))
