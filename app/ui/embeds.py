import discord
from datetime import datetime, timezone
from app.core.constants.colors import RED, YELLOW, ORANGE, GREEN
from app.core.constants.emojis import CROSS, CHECK, INFO
from typing import Optional


def error_embed(
    message: Optional[str] = None, *, title: Optional[str] = None
) -> discord.Embed:
    embed = discord.Embed(color=RED, title=title or f"{CROSS} Action Failed")
    if message:
        embed.description = f"> {message}"
    return embed


def success_embed(message: str, title: Optional[str] = None) -> discord.Embed:
    embed = discord.Embed(
        color=GREEN,
        title=title or f"{CHECK} Action Completed",
        description=f"> {message}",
    )
    return embed


def dm_embed(
    guild: discord.Guild, title: str, action: str, reason: str
) -> discord.Embed:
    colors = {"ban": RED, "kick": RED, "warn": YELLOW, "timeout": ORANGE, "unban": GREEN}
    embed = discord.Embed(
        color=colors.get(action, RED),
        title=title,
        description=f"> **Reason:** {reason}",
    )
    now = datetime.now().strftime("Today at %H:%M")
    embed.set_footer(text=f"Sent from {guild.name} | {now}")

    return embed


def lock_embed(user: discord.Member, action: str) -> discord.Embed:
    colors = {"locked": YELLOW, "unlocked": GREEN}
    embed = discord.Embed(
        color=colors.get(action, GREEN), title=f"{INFO} Channel {action.capitalize()}"
    )
    now = datetime.now().strftime("Today at %H:%M")
    embed.set_footer(icon_url=user.display_avatar.url, text=f"{user.name} | {now}")
    return embed


def log_embed(
    target: discord.Member, mod: discord.Member, action: str, reason: str
) -> discord.Embed:
    colors = {"ban": RED, "kick": RED, "warn": YELLOW, "timeout": ORANGE, "unban": GREEN}
    embed = discord.Embed(
        color=colors.get(action, YELLOW),
        title=action.capitalize(),
        description=f"> **User:** {target.name} ({target.mention})\n > **Reason:** {reason}",
    )
    now = datetime.now(timezone.utc).strftime("%d %b %Y • %I:%M %p UTC")
    embed.set_footer(text=f"{mod.name} | {now}", icon_url=mod.display_avatar.url)
    embed.set_thumbnail(url=target.display_avatar.url)

    return embed
