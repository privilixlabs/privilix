import discord
from discord.ext import commands
from discord import ui

from datetime import datetime

from app.core.constants.emojis import LOGO
from app.core.constants.colors import BLUE
from app.ui.views.helpView import HelpView


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Check the bot's response time to Discord.")
    @commands.guild_only()
    async def _ping(self, ctx):
        ws_latency = round(self.bot.latency * 1000)
        embed = discord.Embed(color=BLUE)
        embed.add_field(name="Bot latency", value=f"{ws_latency}ms")
        now = datetime.now().strftime("Today at %H:%M")
        embed.set_footer(text=f"Privilix | {now}")
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="help", help="Get a list of all my commands.")
    @commands.guild_only()
    async def help_command(self, ctx, command: str = None):
        prefix = self.bot.prefix_cache[ctx.guild.id]
        if command:
            cmd = self.bot.get_command(command)
            if not cmd:
                return await ctx.reply("Command not found.")

            embed = discord.Embed(title="Command Information", color=BLUE)
            embed.add_field(
                name="Description",
                value=f"> {cmd.help}" or "No description.",
                inline=False,
            )
            aliases = []
            for alias in cmd.aliases:
              aliases.append(f"{prefix}{alias}")
            if aliases:
              others = f"> `{", ".join(aliases)}`"
              embed.add_field(name = "Aliases", value = others)
            params = []
            for name, param in cmd.clean_params.items():
                if param.default is param.empty:
                    params.append(f"<{name}>")
                else:
                    params.append(f"[{name}]")

            usage = f"> `.{command} {' '.join(params)}`"
            embed.add_field(name="Usage", value=usage)
            return await ctx.reply(embed=embed)
        view = HelpView(self.bot, prefix)
        embed = discord.Embed(
            title="📚 Help Menu",
            description=f"Use `{prefix}help <command>` to show information about a command.",
            color=BLUE,
        )
        embed.set_footer(text="Pick a category to browse available commands")
        await ctx.send(embed=embed, view=view)

    @commands.command(name="vote", help="Vote for Priviliix.")
    @commands.guild_only()
    async def _vote(self, ctx):
        view = discord.ui.View()
        link_btn = discord.ui.Button(
            label="Vote",
            style=discord.ButtonStyle.link,
            url="https://top.gg/bot/1133741199505760266/vote",
        )
        view.add_item(link_btn)
        embed = discord.Embed(
            color=BLUE,
            title="Vote for Privilix",
            description="> Your vote helps us grow. Tap the button below and vote to make your support count.",
        )
        now = datetime.now().strftime("Today at %H:%M")
        embed.set_footer(text=now)

        await ctx.reply(embed=embed, view=view)

    @commands.command(name="info", help="Learn more about Privilix Bot.")
    @commands.guild_only()
    async def _info(self, ctx):
        view = ui.View()
        link_btn = ui.Button(
            label="Invite",
            style=discord.ButtonStyle.link,
            url="https://discord.com/oauth2/authorize?client_id=1133741199505760266&permissions=8&integration_type=0&scope=bot",
        )
        view.add_item(link_btn)
        support_btn = ui.Button(
            label="Support Server",
            style=discord.ButtonStyle.link,
            url="https://discord.gg/K6EDkaVERk",
        )
        view.add_item(support_btn)
        embed = discord.Embed(
            color=BLUE,
            description=f"## {LOGO} Hi, I'm {self.bot.user}\n-# Less stress. More community.",
        )
        now = datetime.now().strftime("Today at %H:%M")
        embed.add_field(
            name="Bot statistics",
            value=f"**Server Count:** {len(self.bot.guilds)}\n**User Count:** {len(self.bot.users)}",
        )
        embed.add_field(
            name="Links",
            value="[Invite](https://discord.com/oauth2/authorize?client_id=1133741199505760266&permissions=8&integration_type=0&scope=bot)\n[Website](https://privilix.xyz)\n[Support](https://discord.gg/K6EDkaVERk)",
        )
        embed.set_footer(text=now)
        await ctx.reply(embed=embed, view=view)

    @commands.command(name="invite", help="Get an invite link for Privilix.")
    @commands.guild_only()
    async def _invite(self, ctx: commands.Context):
        view = ui.View()
        link_btn = ui.Button(
            label="Invite",
            style=discord.ButtonStyle.link,
            url="https://discord.com/oauth2/authorize?client_id=1133741199505760266&permissions=8&integration_type=0&scope=bot",
        )
        view.add_item(link_btn)
        embed = discord.Embed(
            color=BLUE,
            title="Thanks for your interest in Privilix!",
            description="> Click the button to invite the bot to your server!",
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text=f"Requested by {ctx.author.name} | {datetime.now().strftime('Today at %H:%M')}",
            icon_url=ctx.author.display_avatar.url,
        )

        await ctx.reply(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Misc(bot))
