from __future__ import annotations
import discord
from discord.ext import commands
from app.ui.embeds import error_embed
from typing import Optional


async def check_target(
    ctx: commands.Context, target: discord.Member) -> Optional[discord.Embed]:
    guild = ctx.guild
    author = ctx.author
    bot_member = guild.me

    if not isinstance(target, discord.Member):
        return error_embed("This member isn’t available.")

    if target.id == ctx.bot.user.id:
        return error_embed("This action isn’t supported.")

    if target.id == guild.owner_id:
        return error_embed("This action isn’t available for the server owner.")

    if target.id == author.id:
        return error_embed("This action isn’t available for your own account.")

    if target.bot:
        return error_embed("This action isn’t available for bots.")

    bot_top = bot_member.top_role.position if bot_member.top_role else -1
    target_top = target.top_role.position if target.top_role else -1
    author_top = author.top_role.position if author.top_role else -1

    if target_top >= bot_top:
        return error_embed("My role must be higher to complete this action.")

    if target_top >= author_top and author.id != guild.owner_id:
        return error_embed("Your role isn’t high enough to complete this action.")

    return None
