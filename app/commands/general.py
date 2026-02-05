import discord
from discord.ext import commands
from datetime import datetime
from app.helpers.logging import logger
from app.ui.embeds import error_embed, success_embed
from app.core.constants.colors import BLUE
from app.core.constants.emojis import CHECK, CROSS, NEUTRAL


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", help="Get the avatar of a user.")
    @commands.guild_only()
    async def _avatar(self, ctx, user: discord.Member = None):
        user = user or ctx.author

        avatar = user.display_avatar.replace(size=4096)

        embed = discord.Embed(color=BLUE)
        embed.set_author(name=f"{user.name}'s Avatar", icon_url=avatar.url)
        embed.set_image(url=avatar.url)

        embed.set_footer(text=datetime.now().strftime("Today at %H:%M"))

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="serverinfo", help="Get information about this server.")
    @commands.guild_only()
    async def _serverinfo(self, ctx):
        created = ctx.guild.created_at
        ts = int(created.timestamp())
        relative = f"<t:{ts}:R>"

        guild = ctx.guild
        info = discord.Embed(color=BLUE)
        if guild.icon:
            info.set_author(name=guild.name, icon_url=guild.icon.url)
            info.set_thumbnail(url=guild.icon.url)
        else:
            info.set_author(name=guild.name)
        owner = await guild.fetch_member(guild.owner_id)
        info.add_field(name="Owned By ", value=str(owner.mention))
        info.add_field(name="Member Count", value=guild.member_count)
        info.add_field(
            name="Created At",
            value=f"{guild.created_at.strftime('%a, %b %d, %Y %I:%M %p')} ({relative})",
        )
        info.add_field(
            name="Channels",
            value=f"Text: **{len(guild.text_channels)}** \nVoice: **{len(guild.voice_channels)}**",
        )
        info.add_field(name="Roles", value=len(guild.roles))
        info.set_footer(text=f"ID: {guild.id}")
        await ctx.reply(embed=info, mention_author=False)

    @commands.command(name="whois", help="Get user information.")
    @commands.guild_only()
    async def _whois(self, ctx, user: discord.Member = None):
        member = user or ctx.author
        now = datetime.now().strftime("Today at %H:%M")
        whois = discord.Embed(color=BLUE, description=member.mention)
        whois.set_author(name=member.name, icon_url=member.display_avatar.url)
        whois.set_thumbnail(url=member.display_avatar.url)
        whois.set_footer(text=f"ID: {member.id} | {now}")
        joined = member.joined_at.strftime("%a, %b %d, %Y %I:%M %p")
        created = member.created_at.strftime("%a, %b %d, %Y %I:%M %p")
        whois.add_field(name="Joined", value=joined)
        whois.add_field(name="Registered", value=created)

        roles = [role.name for role in member.roles[1:]]
        if roles:
            role_list = ", ".join(roles)
        else:
            role_list = "No roles"

        whois.add_field(name=f"Roles [{len(member.roles) - 1}]", value=role_list)

        perms = member.guild_permissions
        mapping = {
            "administrator": "Administrator",
            "manage_guild": "Manage Server",
            "manage_roles": "Manage Roles",
            "manage_channels": "Manage Channels",
            "manage_messages": "Manage Messages",
            "manage_webhooks": "Manage Webhooks",
            "manage_nicknames": "Manage Nicknames",
            "manage_emojis_and_stickers": "Manage Emojis and Stickers",
            "kick_members": "Kick Members",
            "ban_members": "Ban Members",
            "mention_everyone": "Mention Everyone",
            "moderate_members": "Timeout Members",
        }

        key_perms = [name for attr, name in mapping.items() if getattr(perms, attr)]
        if not key_perms:
            key_perms = ["None"]

        whois.add_field(
            name="Key Permissions", value=", ".join(key_perms), inline=False
        )

        await ctx.reply(embed=whois, mention_author=False)

    @commands.command(name="suggest", help="Give a suggestion for this server.")
    @commands.guild_only()
    async def _suggest(self, ctx, *, suggestion: str):
        suggestion_id = self.bot.guild_settings_cache[ctx.guild.id][
            "suggestion_channelid"
        ]

        if not suggestion_id:
            await ctx.reply(
                embed=error_embed(
                    "This server hasn’t configured a suggestions channel yet."
                ),
                mention_author=False,
            )
            return

        suggestion_channel = await ctx.guild.fetch_channel(int(suggestion_id))
        try:
            suggester = discord.Embed(
                color=BLUE,
                title=f"Suggestion from @{ctx.author.name}",
                description=f"> {suggestion}",
            )
            now = datetime.now().strftime("Today at %H:%M")
            suggester.set_footer(text=now)
            suggester.set_thumbnail(url=ctx.author.display_avatar.url)
            msg = await suggestion_channel.send(embed=suggester, mention_author=False)
            await msg.add_reaction(CHECK)
            await msg.add_reaction(NEUTRAL)
            await msg.add_reaction(CROSS)
            await ctx.reply(embed=success_embed("Your suggestion has been submitted."))
        except Exception as e:
            await ctx.reply(embed=error_embed("Something went wrong."))
            logger.error(f"Suggest command failed: {e}")


async def setup(bot):
    await bot.add_cog(General(bot))
