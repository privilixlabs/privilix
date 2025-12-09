import discord
from discord.ext import commands
from app.core.constants.colors import BLUE
from app.core.constants.emojis import LOGO


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gldlist")
    @commands.is_owner()
    @commands.guild_only()
    async def _gldlist(self, ctx):
        embed = discord.Embed(color=BLUE, title=f"{LOGO} Guilds List", description="")

        for guild in self.bot.guilds:
            embed.description += f"{guild.name} ({guild.member_count} members)\n"

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Owner(bot))
