import discord
from discord.ext import commands

from app.ui.embeds import error_embed, success_embed
from app.core.constants.colors import BLUE
from app.core.constants.emojis import HAMMER, CROSS, LOGO
from app.helpers.logging import logger
from app.ui.views.warningView import WarningViewer
from app.ui.views.modlogView import Modlogs
from  app.ui.views.setup import Setup
from app.services.database.queries import fetch_modlogs, fetch_warnings, mod_stats
from app.helpers.time_converter import time_converter

from datetime import datetime
from typing import Optional
import asyncio


class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="setup", help="A quick and easy setup to configure all my features."
    )
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: commands.Context):
        embed = discord.Embed(
            color=BLUE,
            title=f"{LOGO} Thank you for choosing Privilix",
            description="> Click the button below to get started.",
        )

        await ctx.reply(embed=embed, view = Setup(self.bot))

    @commands.command(
        name="nickname", aliases=["nick"], help="Set nickname for a user."
    )
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

    @commands.command(
        name="slowmode", aliases=["sm"], help="Set a slowmode for a channel."
    )
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

    @commands.command(name="addrole", aliases=["ar"], help="Add a role to a user")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _addrole(
        self,
        ctx: commands.Context,
        target: discord.Member,
        role: discord.Role,
        *,
        reason: str = "No reason provided",
    ):
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.reply(
                embed=error_embed("Missing permission to manage roles."),
                mention_author=False,
            )
            return

        if role.position >= ctx.guild.me.top_role.position:
            await ctx.reply(
                embed=error_embed("That role is higher than my highest role."),
                mention_author=False,
            )
            return

        if (
            target.top_role >= ctx.author.top_role
            and ctx.author.id != ctx.guild.owner_id
        ):
            await ctx.reply(
                embed=error_embed("You can’t modify roles for this member."),
                mention_author=False,
            )
            return

        if (
            role.position >= ctx.author.top_role.position
            and ctx.author.id != ctx.guild.owner_id
        ):
            await ctx.reply(
                embed=error_embed("You can’t assign a role higher than your own."),
                mention_author=False,
            )
            return

        if role in target.roles:
            await ctx.reply(
                embed=error_embed(f"{target.mention} already has that role."),
                mention_author=False,
            )
            return

        try:
            await target.add_roles(role, reason=f"{ctx.author}: {reason}")
        except Exception as e:
            logger.error(f"Addrole command failed: {e}")
            await ctx.reply(
                embed=error_embed("Something went wrong."),
                mention_author=False,
            )
            return

        await ctx.reply(
            embed=success_embed(f"Added **{role.name}** to {target.mention}."),
            mention_author=False,
        )

    @commands.command(
        name="removerole", aliases=["rr"], help="Remove a role from a user"
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _removerole(
        self,
        ctx: commands.Context,
        target: discord.Member,
        role: discord.Role,
        *,
        reason: str = "No reason provided",
    ):
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.reply(
                embed=error_embed("Missing permission to manage roles."),
                mention_author=False,
            )
            return

        if role.position >= ctx.guild.me.top_role.position:
            await ctx.reply(
                embed=error_embed("That role is higher than my highest role."),
                mention_author=False,
            )
            return

        if (
            target.top_role >= ctx.author.top_role
            and ctx.author.id != ctx.guild.owner_id
        ):
            await ctx.reply(
                embed=error_embed("You can’t modify roles for this member."),
                mention_author=False,
            )
            return

        if (
            role.position >= ctx.author.top_role.position
            and ctx.author.id != ctx.guild.owner_id
        ):
            await ctx.reply(
                embed=error_embed("You can’t remove a role higher than your own."),
                mention_author=False,
            )
            return

        if role not in target.roles:
            await ctx.reply(
                embed=error_embed(f"{target.mention} doesn’t have that role."),
                mention_author=False,
            )
            return

        try:
            await target.remove_roles(role, reason=f"{ctx.author}: {reason}")
        except Exception as e:
            logger.error(f"Removerole command failed: {e}")
            await ctx.reply(
                embed=error_embed("Something went wrong."),
                mention_author=False,
            )
            return

        await ctx.reply(
            embed=success_embed(f"Removed **{role.name}** from {target.mention}."),
            mention_author=False,
        )

    @commands.command(
        name="modstats", aliases=["ms"], help="Get moderation stats of a mod"
    )
    @commands.guild_only()
    @commands.has_permissions(view_audit_log=True)
    async def _modstats(
        self, ctx: commands.Context, mod: Optional[discord.Member] = None
    ):
        mod = mod or ctx.author
        stats = await mod_stats(ctx.guild.id, mod.id)

        if stats["total_actions"] == 0:
            await ctx.reply(
                embed=error_embed(
                    f"No moderation actions found for **{mod.display_name}**."
                )
            )
            return

        embed = discord.Embed(
            title=f"{HAMMER} Moderator Statistics",
            description=f"-# Stats for {mod.display_name}",
            color=BLUE,
        )

        embed.add_field(
            name="Total Actions", value=str(stats["total_actions"]), inline=False
        )

        for action, count in stats["actions"].items():
            embed.add_field(name=action.capitalize(), value=str(count), inline=True)

        embed.set_thumbnail(url=mod.display_avatar.url)
        embed.set_footer(text=datetime.now().strftime("Today at %H:%M"))
        await ctx.reply(embed=embed)

    @commands.command(
        name="massrole",
        aliases=["mr"],
        help="Add or remove a role to all human members.",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _massrole(self, ctx: commands.Context, action: str, role: discord.Role):
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.reply(
                embed=error_embed("Missing permission to manage roles."),
                mention_author=False,
            )
            return

        if role >= ctx.guild.me.top_role:
            await ctx.reply(embed=error_embed("That role is higher than my top role"))

        action = action.lower()

        if not action in ("add", "remove"):
            embed = error_embed(
                "**Usage:** `.massrole add @role` or `.massrole remove @role`",
                title=f"{CROSS} Wrong Usage",
            )
            await ctx.reply(embed=embed)
            return

        success = 0
        failed = 0

        for member in ctx.guild.members:
            if member.bot:
                continue
            try:
                if action == "add" and role not in member.roles:
                    await member.add_roles(role, reason=f"Massrole by {ctx.author}")
                    success += 1

                elif action == "remove" and role in member.roles:
                    await member.remove_roles(role, reason=f"Massrole by {ctx.author}")
                    success += 1

                await asyncio.sleep(0.3)
            except Exception:
                failed += 1

        await ctx.reply(
            embed=success_embed(
                f"The role {role.mention} has been {'added to' if action == 'add' else 'removed from'} {success}/{success + failed} members"
            )
        )


async def setup(bot):
    await bot.add_cog(Management(bot))
